FROM python:3.10.4

LABEL org.opencontainers.image.source=https://github.com/apinanyogaratnam/akms

WORKDIR /app

# Copy source code
COPY . .

# Install dependencies
RUN pip install pipenv
RUN pipenv install

# Run the application
CMD ["pipenv", "run", "uvicorn", "api.main:app" "--port 8000", "--host 0.0.0.0"]
