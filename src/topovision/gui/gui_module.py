"""
Módulo de Interfaz Gráfica para TopoVision
"""

import tkinter as tk
from tkinter import Canvas, Tk, ttk, messagebox
from typing import Optional, Tuple, Callable, Any

import cv2
import numpy as np
from PIL import Image, ImageTk

try:
    from topovision.core.interfaces import ICamera
    Camera = ICamera
except ImportError:
    class ICamera:
        def start(self): pass
        def pause(self): pass
        def stop(self): pass
        def get_frame(self): return None
    Camera = ICamera


class MainWindow(Tk):

    def __init__(self, camera: ICamera, calculation_callback: Optional[Callable] = None) -> None:
        super().__init__()

        self.title("TopoVision - Análisis Topográfico 3D")
        self.geometry("1200x800")  
        self.configure(bg="#111214")  
        self.minsize(1000, 700)
        self.calculation_callback = calculation_callback 

        # ---- Camera & Analysis State ----
        self.camera: Camera = camera
        self.is_camera_running: bool = False
        self.photo: Optional[ImageTk.PhotoImage] = None
        self._analysis_result_photo: Optional[ImageTk.PhotoImage] = None
        self.is_showing_analysis: bool = False 

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass

        self._setup_styles(style)  
        
        # Frame principal que contiene todo
        main_container = ttk.Frame(self)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Configurar grid: 2 columnas (canvas + panel)
        main_container.grid_columnconfigure(0, weight=3)  # Canvas (más ancho)
        main_container.grid_columnconfigure(1, weight=1)  # Panel lateral
        main_container.grid_rowconfigure(0, weight=1)     # Fila única

        # 1. Canvas principal a la IZQUIERDA (Video/Heatmap Area)
        self.canvas: Canvas = tk.Canvas(
            main_container,
            bg="#0E0F11",  # Color de fondo del canvas 
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew", padx=(0, 15))

        # 2. Panel de análisis 
        self.analysis_frame = ttk.Frame(main_container, style="TFrame", width=250)
        self.analysis_frame.grid(row=0, column=1, sticky="nsew")
        self.analysis_frame.grid_propagate(False)  # Mantener ancho fijo
        
        # Configurar controles en el panel derecho
        self._setup_analysis_controls()

        # 3. Frame para botones inferiores (debajo del canvas y panel)
        self.buttons_frame: ttk.Frame = ttk.Frame(self)
        self.buttons_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=50, pady=15)
        
        # Botón 'Open Camera' (izquierda)
        self.btn_toggle_camera: ttk.Button = ttk.Button(
            self.buttons_frame, text="Open Camera", command=self.toggle_camera
        )
        self.btn_toggle_camera.pack(side=tk.LEFT, padx=10, pady=5)

        # Botón 'Exit' (derecha) - FIX: Cambiar self.on_exit a self._on_exit
        self.btn_exit: ttk.Button = ttk.Button(
            self.buttons_frame, text="Exit", command=self._on_exit
        )
        self.btn_exit.pack(side=tk.RIGHT, padx=10, pady=5)

        # ---- Selection State (Fase 3: Eventos de Usuario) ----
        self.selection_start: Optional[Tuple[int, int]] = None
        self.selection_rect_id: Optional[int] = None
        self.selected_region: Optional[Tuple[int, int, int, int]] = None
        
        # ---- Event Bindings ----
        self.canvas.bind("<ButtonPress-1>", self._on_click)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)
        self._canvas_image_id = None

        # Window close protocol - FIX: Cambiar self.on_exit a self._on_exit
        self.protocol("WM_DELETE_WINDOW", self._on_exit)

    def _setup_styles(self, style: ttk.Style) -> None:
        """Configura los estilos Ttk para el tema oscuro - Fase 4"""
        style.configure("TFrame", background="#111214")
        style.configure("TLabel", background="#111214", foreground="#E6E6E6", font=("Arial", 10))
        style.configure(
            "TButton",
            background="#1C1D20",
            foreground="#E6E6E6",
            padding=6,
            borderwidth=0,
            relief="flat"
        )
        style.map(
            "TButton",
            background=[("active", "#2C2D30")],
            foreground=[("active", "white")]
        )
        style.configure("Heading.TLabel", font=("Arial", 12, "bold"), foreground="#4DA6FF")
        
    def _setup_analysis_controls(self) -> None:
        """Crea el panel lateral con controles de cálculo - Fase 2"""
        
        # Título del panel
        ttk.Label(self.analysis_frame, text="Controles de Análisis", style="Heading.TLabel").pack(pady=(10, 5))
        ttk.Separator(self.analysis_frame).pack(fill=tk.X, padx=5, pady=5)
        
        # 1. Parámetros de Cálculo
        ttk.Label(self.analysis_frame, text="Parámetros de Cálculo").pack(anchor=tk.W, padx=5, pady=(10, 0))
        
        param_frame = ttk.Frame(self.analysis_frame)
        param_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(param_frame, text="Factor Z:").pack(side=tk.LEFT, padx=(0, 5))
        self.z_factor_entry = ttk.Entry(param_frame, width=8)
        self.z_factor_entry.insert(0, "1.0")
        self.z_factor_entry.pack(side=tk.LEFT)
        
        # Información sobre Factor Z
        info_label = ttk.Label(
            self.analysis_frame,
            text="Escala valores de altura\n1.0 = normal, >1.0 = más sensible",
            font=("Arial", 8),
            foreground="#8B949E"
        )
        info_label.pack(anchor=tk.W, padx=5, pady=(0, 10))
        
        ttk.Separator(self.analysis_frame).pack(fill=tk.X, padx=5, pady=5)

        # 2. Botones de Acción
        ttk.Label(self.analysis_frame, text="Acciones de Análisis").pack(anchor=tk.W, padx=5, pady=(10, 0))

        # Botón para calcular gradiente
        gradient_btn = ttk.Button(
            self.analysis_frame, 
            text="Calcular Gradiente", 
            command=lambda: self._trigger_analysis("gradient"),
            style="TButton"
        )
        gradient_btn.pack(fill=tk.X, padx=10, pady=5)

        # Botón para calcular volumen
        volume_btn = ttk.Button(
            self.analysis_frame, 
            text="Calcular Volumen", 
            command=lambda: self._trigger_analysis("volume"),
            style="TButton"
        )
        volume_btn.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Separator(self.analysis_frame).pack(fill=tk.X, padx=5, pady=10)

        # 3. Control de Visualización
        ttk.Label(self.analysis_frame, text="Visualización").pack(anchor=tk.W, padx=5, pady=(10, 0))

        # Botón para alternar vista
        toggle_btn = ttk.Button(
            self.analysis_frame, 
            text="Alternar Vista", 
            command=lambda: self.toggle_view(),
            style="TButton"
        )
        toggle_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Botón para limpiar selección
        clear_btn = ttk.Button(
            self.analysis_frame, 
            text="Borrar Selección", 
            command=lambda: self.clear_selection(),
            style="TButton"
        )
        clear_btn.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Separator(self.analysis_frame).pack(fill=tk.X, padx=5, pady=10)

        # 4. Status/Feedback 
        self.status_label_var = tk.StringVar(value="Sistema listo. Selecciona una región.")
        self.status_label = ttk.Label(
            self.analysis_frame, 
            textvariable=self.status_label_var, 
            wraplength=200,
            font=("Arial", 9)
        )
        self.status_label.pack(fill=tk.X, padx=5, pady=5)

    def set_status(self, message: str, is_error: bool = False) -> None:
        """Actualiza la etiqueta de estado con mensajes amigables - Fase 4"""
        color = "#FF6B6B" if is_error else "#E6E6E6"  # Rojo para errores 
        self.status_label.config(foreground=color)
        
        # Mensajes de error
        if is_error:
            if "camera" in message.lower():
                friendly_message = "No se pudo conectar con la cámara. Verifica que esté conectada y no esté en uso."
            elif "region" in message.lower():
                friendly_message = "Por favor, selecciona una región rectangular primero."
            elif "z factor" in message.lower():
                friendly_message = "El Factor Z debe ser un número positivo (ej. 1.0, 2.5)"
            else:
                friendly_message = message
            
            self.status_label_var.set(f"{friendly_message}")
            # Solo mostrar messagebox para errores críticos
            if "camera" in message.lower() or "error" in message.lower():
                messagebox.showerror("Error de TopoVision", friendly_message)
        else:
            self.status_label_var.set(f"✅ {message}")
    
    def _trigger_analysis(self, method: str) -> None:
        """Maneja la lógica de inicio de cálculo """
        if self.selected_region is None:
            self.set_status("Por favor, selecciona una región en la imagen primero.", is_error=True)
            return
        
        if not self.is_camera_running and self._analysis_result_photo is None:
            self.set_status("La cámara debe estar activa o debe haber un resultado previo.", is_error=True)
            return
    
        # Leer el valor del Factor Z
        try:
            z_factor = float(self.z_factor_entry.get())
        except ValueError:
            self.set_status("'Factor Z' debe ser un número válido (ej. 1.0, 54).", is_error=True)
            return

        # Llamar al callback
        if self.calculation_callback:
            try:
                self.calculation_callback(method, self.selected_region, z_factor) 
                self.set_status(f"Calculando {method} con Factor Z: {z_factor}...")
            except Exception as e:
                self.set_status(f"Error al iniciar el cálculo: {e}", is_error=True)
        else:
            # Si no hay callback, mensaje demo
            self.set_status(f"Demo: {method} en región {self.selected_region}. Factor Z: {z_factor}")

    def clear_selection(self) -> None:
        """Borra la región seleccionada"""
        self.selected_region = None
        self.canvas.delete("selection")
        self.set_status("Selección borrada.")
        
    def toggle_view(self) -> None:
        """Alterna entre la vista de la cámara en vivo y la vista de análisis"""
        if self._analysis_result_photo is None:
            self.set_status("No hay resultados de análisis para mostrar.", is_error=True)
            return
        
        self.is_showing_analysis = not self.is_showing_analysis
        view_state = "Análisis" if self.is_showing_analysis else "Cámara en Vivo"
        self.set_status(f"Vista cambiada a: {view_state}")
        self._update_frame()

    def display_result_image(self, pil_image: Image.Image) -> None:
        """Muestra una imagen de resultado en el canvas - Integración"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w > 1 and h > 1:
            resized_img = pil_image.resize((w, h), Image.Resampling.LANCZOS)
            self._analysis_result_photo = ImageTk.PhotoImage(image=resized_img)
            
            self.is_showing_analysis = True
            self.set_status("Cálculo completado. Mostrando resultados.")
            self._update_frame()

    def toggle_camera(self) -> None:
        if not self.is_camera_running:
            self.start_capture()
        else:
            self.pause_capture()

    def start_capture(self) -> None:
        if not self.is_camera_running:
            try:
                self.camera.start()
                self.is_camera_running = True
                self.is_showing_analysis = False 
                self.btn_toggle_camera.config(text="Pause Camera")
                self.set_status("Cámara iniciada correctamente.")
                self._update_frame()
            except Exception as e:
                self.set_status(f"Error al iniciar la cámara: {e}", is_error=True)
                
    def pause_capture(self) -> None:
        if self.is_camera_running:
            try:
                self.camera.pause()
            except Exception:
                pass
            self.is_camera_running = False
            self.btn_toggle_camera.config(text="Resume Camera")
            self.set_status("Cámara pausada.")

    def stop_capture(self) -> None:
        if self.is_camera_running:
            self.pause_capture()
        try:
            self.camera.stop()
        except Exception:
            pass
    
    def _update_frame(self) -> None:
        """Actualiza el contenido del canvas"""
        
        # Mostrar Resultado de Análisis
        if self.is_showing_analysis and self._analysis_result_photo:
            self.canvas.delete("camera_frame") 
            if self._canvas_image_id is None:
                self._canvas_image_id = self.canvas.create_image(
                    0, 0, 
                    image=self._analysis_result_photo, 
                    anchor=tk.NW, 
                    tags="analysis_result"
                )
            else:
                self.canvas.itemconfig(
                    self._canvas_image_id, 
                    image=self._analysis_result_photo, 
                    tags="analysis_result"
                )
            self.canvas.delete("selection")

        # Mostrar Cámara en Vivo
        elif self.is_camera_running:
            frame = self.camera.get_frame()
            if frame is not None:
                try:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                except Exception:
                    pass

                w = max(1, self.canvas.winfo_width())
                h = max(1, self.canvas.winfo_height())
                
                resized = cv2.resize(frame, (w, h), interpolation=cv2.INTER_AREA)
                img = Image.fromarray(resized)
                self.photo = ImageTk.PhotoImage(image=img)

                self.canvas.delete("analysis_result") 
                if self._canvas_image_id is None:
                    self._canvas_image_id = self.canvas.create_image(
                        0, 0, image=self.photo, anchor=tk.NW, tags="camera_frame"
                    )
                else:
                    self.canvas.itemconfig(self._canvas_image_id, image=self.photo, tags="camera_frame")
                
                # Redibujar la selección
                self.canvas.delete("selection")
                if self.selected_region:
                    x1, y1, x2, y2 = self.selected_region
                    # Color de selección mejorado 
                    self.canvas.create_rectangle(
                        x1, y1, x2, y2,
                        outline="#FFD34D",  
                        width=2,
                        dash=(4, 2),
                        tags="selection",
                    )
        
        # Reprogramar la actualización
        if self.is_camera_running or self.is_showing_analysis:
            self.after(15, self._update_frame)
        else:
            # Pantalla de inicio/inactiva
            self.canvas.delete(tk.ALL)
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            
            if w > 100 and h > 100:
                self.canvas.create_text(
                    w/2, h/2, 
                    text="Haz clic en 'Open Camera' para comenzar",
                    fill="#E6E6E6",  
                    font=("Arial", 16),
                    justify="center",
                    width=w-40
                )

    # ==================== EVENTOS DEL MOUSE ====================

    def _on_click(self, event):
        if not self.is_camera_running and not self.is_showing_analysis:
            self.set_status("Inicia la cámara primero o carga un análisis previo.", is_error=True)
            return
        
        self.selection_start = (event.x, event.y)
        self.canvas.delete("selection")
        self.set_status(f"Clic en: ({event.x}, {event.y}). Arrastra para seleccionar.")

    def _on_drag(self, event):
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = event.x, event.y
            
            # Eliminar selección anterior
            self.canvas.delete("selection")
            
            # Dibujar nueva selección
            self.selection_rect_id = self.canvas.create_rectangle(
                x1, y1, x2, y2,
                outline="#FFD34D",  
                width=2,
                dash=(3, 2),
                tags="selection",
            )

    def _on_release(self, event):
        """Manejador para liberación del mouse - Fase 3"""
        if self.selection_start:
            x1, y1 = self.selection_start
            x2, y2 = event.x, event.y
            
            # Ordenar coordenadas
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            
            # Validar tamaño mínimo 
            min_size = 10
            if (x2 - x1) < min_size or (y2 - y1) < min_size:
                self.set_status(
                    f"Selección muy pequeña. Mínimo {min_size}×{min_size} píxeles.",
                    is_error=True
                )
                self.canvas.delete("selection")
                self.selection_start = None
                return
            
            self.selected_region = (x1, y1, x2, y2)
            self.selection_start = None
            
            # Feedback visual mejorado
            width = x2 - x1
            height = y2 - y1
            self.set_status(f"✅ Región seleccionada: {width}×{height} píxeles")

    def _on_exit(self) -> None:
        """Maneja el cierre seguro de la ventana - FIX: Cambiado de on_exit a _on_exit"""
        self.set_status("Cerrando aplicación...")
        self.stop_capture()
        self.destroy()

    def run(self) -> None:
        """Inicia el loop principal de la aplicación"""
        self.mainloop()