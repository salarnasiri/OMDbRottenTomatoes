FROM python:3.9-alpine

COPY requirements.pip .
RUN pip install -r requirements.pip

COPY main.py .

ENTRYPOINT ["python", "main.py"]

