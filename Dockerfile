# 1. Base Image: Hum ek halka (slim) Python 3.10 environment le rahe hain
FROM python:3.10-slim

# 2. Container ke andar ek folder banayenge '/app' naam se
WORKDIR /app

# 3. Sirf requirements.txt ko pehle copy karenge (taaki installation fast ho)
COPY requirements.txt .

# 4. Saari libraries install karenge
RUN pip install --no-cache-dir -r requirements.txt

# 5. Ab apna baaki saara code (main.py, models.py, etc.) container mein copy karenge
COPY . .

# 6. Container start hote hi jo command chalegi (FastAPI server start karne ke liye)
# Note: "0.0.0.0" likhna zaroori hai taaki server bahar se access ho sake
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]