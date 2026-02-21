# OS Selection Criteria: Using slim-buster for a lightweight Linux distribution
#
FROM python:3.12-slim

WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/code

# Required: Expose port 5477
EXPOSE 5477

# Update the port in the startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5477"]