FROM python:3.10-slim
WORKDIR /opt/devman-chatbot/
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY main.py ./
CMD ["python", "main.py"]