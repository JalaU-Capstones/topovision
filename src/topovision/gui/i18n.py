"""
Internationalization (i18n) support for TopoVision.

This module provides a simple framework for translating UI strings.
It is designed to be easily extensible with new languages.

To add a new language, create a new dictionary with the language's
ISO 639-1 code as its name (e.g., 'fr' for French) and add it to the
`LANGUAGES` dictionary.

The `get_translator` function provides a convenient way to get a translation
function for a specific language, with a fallback to the default language (English).
"""

from typing import Any, Callable, Dict, Protocol

# Default language
DEFAULT_LANG = "en"

# English translations
en = {
    "app_title": "TopoVision - 3D Topographic Analysis",
    "analysis_controls_title": "Analysis Controls",
    "calculation_parameters_title": "Calculation Parameters",
    "z_factor_label": "Z-Factor:",
    "z_factor_info": "Height values scale\n1.0 = normal, >1.0 = more sensitive",
    "analysis_actions_title": "Analysis Actions",
    "gradient_button": "Calculate Gradient",
    "volume_button": "Calculate Volume",
    "arc_length_button": "Calculate Arc Length",
    "visualization_title": "Visualization",
    "toggle_view_button": "Toggle View",
    "clear_selection_button": "Clear Selection",
    "status_ready": "System ready. Select a region.",
    "open_camera_button": "Open Camera",
    "pause_camera_button": "Pause Camera",
    "resume_camera_button": "Resume Camera",
    "exit_button": "Exit",
    "open_3d_plot_button": "Open 3D Plot Window",
    "camera_error": "Could not connect to the camera. Check if it is connected "
    "and not in use. Error: {error}",
    "region_error": "Please select a rectangular region first.",
    "z_factor_error": "The Z-Factor must be a positive number (e.g., 1.0, 2.5)",
    "analysis_completed": "Calculation completed. Showing results.",
    "camera_started": "Camera started successfully.",
    "camera_paused": "Camera paused.",
    "calculating_gradient": "Calculated gradient: dx={dx:.2f}, dy={dy:.2f}",
    "calculating_volume": "Calculated volume: {volume:.2f}",
    "calculating_arc_length": "Calculated arc length: {length:.2f}",
    "selection_cleared": "Selection cleared.",
    "view_changed_to_analysis": "View changed to: Analysis",
    "view_changed_to_camera": "View changed to: Live Camera",
    "no_analysis_to_show": "No analysis results to show.",
    "click_to_start": "Click 'Open Camera' to begin",
    "closing_app": "Closing application...",
    "selection_made": "Region selected: {width}×{height} pixels",
    "selection_too_small": "Selection too small. Minimum {min_size}×{min_size} pixels.",
    "no_frame_to_analyze": "No frame available to analyze.",
    "calculating": "Calculating {method}...",
    "calculation_error": "Error during calculation: {error}",
    "3d_plot_window_title": "3D Topographic Analysis - Live Surface Viewer",  # Updated title
    "no_3d_plot_yet": "No 3d plot generated yet. Select a region in the main window "
    "to see a live 3D surface.",  # Updated message
    "3d_plot_window_opened": "3D Live Surface window opened.",  # Updated message
    "3d_surface_plot_title": "Live 3D Surface Plot of Selected Region",  # Updated title
    "3d_surface_plot_generated": "Live 3D Surface Plot initialized.",  # Updated message
    # Tutorial Messages
    "tutorial_gradient_title": "Gradient Analysis Tutorial",
    "tutorial_gradient": "The Gradient Analysis calculates the rate of change of height "
    "in both X and Y directions within the selected region. This helps visualize "
    "slopes and steepness. A heatmap will be overlaid on your image.",
    "tutorial_volume_title": "Volume Calculation Tutorial",
    "tutorial_volume": "The Volume Calculation estimates the volume under the surface "
    "defined by the selected region. The 'Z-Factor' scales the height values, "
    "allowing you to adjust the perceived depth.",
    "tutorial_arc_length_title": "Arc Length Calculation Tutorial",
    "tutorial_arc_length": "Arc Length estimates the length of a curve. For image "
    "analysis, it typically calculates the length of a cross-section (e.g., a "
    "middle row) within your selected region.",
    "tutorial_plot3d_title": "3D Live Surface Plot Tutorial",
    "tutorial_plot3d": "The 3D Live Surface Plot visualizes the selected region as a "
    "dynamic 3D topographic map. Brighter areas in the original image correspond "
    "to higher elevations. You can adjust colormap, shading, and resolution using "
    "the controls on the left. Select a region in the main window to see it in 3D.",
    # 3D Plot Controls
    "plot_controls_title": "Plot Controls",
    "colormap_label": "Colormap:",
    "shading_label": "Sading",
    "wireframe_label": "Wireframe",
    "resolution_label": "Resolution Factor (1=High, 10=Low)",  # New
}

# Spanish translations
es = {
    "app_title": "TopoVision - Análisis Topográfico 3D",
    "analysis_controls_title": "Controles de Análisis",
    "calculation_parameters_title": "Parámetros de Cálculo",
    "z_factor_label": "Factor Z:",
    "z_factor_info": "Escala valores de altura\n1.0 = normal, >1.0 = más sensible",
    "analysis_actions_title": "Acciones de Análisis",
    "gradient_button": "Calcular Gradiente",
    "volume_button": "Calcular Volumen",
    "arc_length_button": "Calcular Longitud de Arco",
    "visualization_title": "Visualización",
    "toggle_view_button": "Alternar Vista",
    "clear_selection_button": "Borrar Selección",
    "status_ready": "Sistema listo. Selecciona una región.",
    "open_camera_button": "Abrir Cámara",
    "pause_camera_button": "Pausar Cámara",
    "resume_camera_button": "Reanudar Cámara",
    "exit_button": "Salir",
    "open_3d_plot_button": "Abrir Ventana de Gráficos 3D",
    "camera_error": "No se pudo conectar con la cámara. Verifica que esté conectada "
    "y no esté en uso. Error: {error}",
    "region_error": "Por favor, selecciona una región rectangular primero.",
    "z_factor_error": "El Factor Z debe ser un número positivo (ej. 1.0, 2.5)",
    "analysis_completed": "Cálculo completado. Mostrando resultados.",
    "camera_started": "Cámara iniciada correctamente.",
    "camera_paused": "Cámara pausada.",
    "calculating_gradient": "Gradiente calculado: dx={dx:.2f}, dy={dy:.2f}",
    "calculating_volume": "Volumen calculado: {volume:.2f}",
    "calculating_arc_length": "Longitud de arco calculada: {length:.2f}",
    "selection_cleared": "Selección borrada.",
    "view_changed_to_analysis": "Vista cambiada a: Análisis",
    "view_changed_to_camera": "Vista cambiada a: Cámara en Vivo",
    "no_analysis_to_show": "No hay resultados de análisis para mostrar.",
    "click_to_start": "Haz clic en 'Abrir Cámara' para comenzar",
    "closing_app": "Cerrando aplicación...",
    "selection_made": "Región seleccionada: {width}×{height} píxeles",
    "selection_too_small": "Selección muy pequeña. Mínimo {min_size}×{min_size} píxeles.",
    "no_frame_to_analyze": "No hay ningún fotograma disponible para analizar.",
    "calculating": "Calculando {method}...",
    "calculation_error": "Error en el cálculo: {error}",
    "3d_plot_window_title": "Visor de Superficie 3D en Vivo",  # Updated title
    "no_3d_plot_yet": "Aún no se ha generado ningún gráfico 3D. Selecciona una región "
    "en la ventana principal para ver una superficie 3D en vivo.",  # Updated message
    "3d_plot_window_opened": "Ventana de Superficie 3D en Vivo abierta.",  # Updated message
    "3d_surface_plot_title": "Gráfico de Superficie 3D en Vivo de la Región Seleccionada",  # Updated title
    "3d_surface_plot_generated": "Gráfico de Superficie 3D en Vivo inicializado.",  # Updated message
    # Tutorial Messages
    "tutorial_gradient_title": "Tutorial de Análisis de Gradiente",
    "tutorial_gradient": "El Análisis de Gradiente calcula la tasa de cambio de altura "
    "en las direcciones X e Y dentro de la región seleccionada. Esto ayuda a "
    "visualizar pendientes e inclinaciones. Se superpondrá un mapa de calor en "
    "tu imagen.",
    "tutorial_volume_title": "Tutorial de Cálculo de Volumen",
    "tutorial_volume": "El Cálculo de Volumen estima el volumen bajo la superficie "
    "definida por la región seleccionada. El 'Factor Z' escala los valores de "
    "altura, permitiéndote ajustar la profundidad percibida.",
    "tutorial_arc_length_title": "Tutorial de Cálculo de Longitud de Arco",
    "tutorial_arc_length": "La Longitud de Arco estima la longitud de una curva. Para "
    "el análisis de imágenes, típicamente calcula la longitud de una sección "
    "transversal (por ejemplo, una fila central) dentro de tu región seleccionada.",
    "tutorial_plot3d_title": "Tutorial de Gráfico de Superficie 3D en Vivo",
    "tutorial_plot3d": "El Gráfico de Superficie 3D en Vivo visualiza la región "
    "seleccionada como un mapa topográfico 3D dinámico. Las áreas más brillantes "
    "en la imagen original corresponden a elevaciones más altas. Puedes ajustar "
    "el mapa de colores, el sombreado y la resolución usando los controles de la "
    "izquierda. Selecciona una región en la ventana principal para verla en 3D.",
    # 3D Plot Controls
    "plot_controls_title": "Plot Controls",
    "colormap_label": "Mapa de Colores:",
    "shading_label": "Sombreado",
    "wireframe_label": "Malla de Alambre",
    "resolution_label": "Factor de Resolución (1=Alto, 10=Bajo)",  # New
}

# Add all languages to a central dictionary
LANGUAGES: Dict[str, Dict[str, str]] = {
    "en": en,
    "es": es,
}


class Translator(Protocol):
    def __call__(self, key: str, **kwargs: Any) -> str: ...


def get_translator(lang: str) -> Translator:
    """
    Returns a translation function for the given language.

    The returned function takes a key and optional format arguments,
    and returns the translated string. It falls back to the default
    language if a translation is not found in the specified language.

    Args:
        lang (str): The desired language code (e.g., 'es').

    Returns:
        function: A translator function.
    """
    translations = LANGUAGES.get(lang, LANGUAGES[DEFAULT_LANG])
    default_translations = LANGUAGES[DEFAULT_LANG]

    def translate(key: str, **kwargs: Any) -> str:
        """
        Translates the given key.
        """
        message = translations.get(key, default_translations.get(key, key))
        if kwargs:
            return message.format(**kwargs)
        return message

    return translate
