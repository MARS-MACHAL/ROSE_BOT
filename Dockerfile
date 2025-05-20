FROM python:3.9
WORKDIR /app
COPY . .
RUN pip install -U -r requirements.txt
CMD ["python3", "main.py"]
