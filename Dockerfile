FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4000
# start the flask app with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:${PORT}", "-w", "3", "--timeout", "120", "app:app"]
