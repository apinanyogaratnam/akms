FROM python:3.10.4

LABEL org.opencontainers.image.source=https://github.com/apinanyogaratnam/akms

WORKDIR /app

# copy all files
COPY . .

# install dependencies
RUN pip install pipenv==2022.11.5
RUN pipenv install --system --deploy --ignore-pipfile

CMD ["python", "main.py"]
