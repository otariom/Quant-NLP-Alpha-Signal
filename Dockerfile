# Use full Python image (faster for torch)
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy only requirements first
COPY requirements.txt .

# Install dependencies (optimized)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0"]