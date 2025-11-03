# 1️⃣ Clone repository
git clone https://github.com/JalaU-Capstones/topovision.git  
cd topovision

# 2️⃣ Create a virtual environment
python3.11 -m venv .venv  
source .venv/bin/activate   # (Linux/Mac)  
# or  
.venv\Scripts\activate      # (Windows)  

# 3️⃣ Install runtime dependencies
pip install -r requirements.txt

# 4️⃣ Install development dependencies
pip install -r requirements-dev.txt

# 5️⃣ Initialize pre-commit hooks
pre-commit install

# 6️⃣ Run tests to verify everything works
pytest --cov
