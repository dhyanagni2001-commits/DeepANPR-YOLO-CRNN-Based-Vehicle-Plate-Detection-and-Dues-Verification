FROM python:3.11

# Install OS packages needed for Tesseract
RUN apt-get clean && rm -rf /var/lib/apt/lists/* \
    && apt-get update -o Acquire::CompressionTypes::Order::=gz \
    && apt-get install -y --no-install-recommends \
       tesseract-ocr \
       libtesseract-dev \
    && rm -rf /var/lib/apt/lists/*


# Set work directory
WORKDIR /app

# Copy code
COPY ./ocr_service.py /app/

# Install Python packages
RUN pip install --no-cache-dir fastapi uvicorn pillow pytesseract

# Expose FastAPI port
EXPOSE 8000

# Run server
CMD ["uvicorn", "ocr_service:app", "--host", "0.0.0.0", "--port", "8000"]
