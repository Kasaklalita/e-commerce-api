FROM python:3.10
WORKDIR /fastapi-app
COPY requirements.txt ./fastapi-app
RUN pip install -r ./fastapi-app/requirements.txt
COPY . ./fastapi-app
CMD ["python", "./main.py"]