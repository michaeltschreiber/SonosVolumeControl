FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN ls -la

EXPOSE 8501

CMD ["streamlit", "run", "sonos_control.py"]