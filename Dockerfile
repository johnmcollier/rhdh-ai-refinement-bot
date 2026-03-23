FROM registry.access.redhat.com/ubi9/python-312:latest

WORKDIR /app

# Install dependencies as root before switching to non-root user
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY app/ ./app/
COPY static/ ./static/

# UBI images run as user 1001 by default
USER 1001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
