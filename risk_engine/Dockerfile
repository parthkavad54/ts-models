FROM python:3.11-slim

WORKDIR /app

# Install system utilities if needed
RUN apt-get update && apt-get install -y --no-install-recommends build-essential && rm -rf /var/lib/apt/lists/*

# Copy strictly the requirements file to install dependencies first securely
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire risk_engine project
COPY . /app/risk_engine

# Ensure Python knows where to find the module
ENV PYTHONPATH=/app

EXPOSE 8000

# The standard deployment hook used natively by PAAS and Serverless Platforms
CMD ["uvicorn", "risk_engine.main:app", "--host", "0.0.0.0", "--port", "8000"]
