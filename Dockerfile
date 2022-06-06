FROM python:3.9.13-slim
EXPOSE 8082
COPY requirements.txt app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt
COPY . /app
WORKDIR /app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8082", "--server.address=0.0.0.0"]