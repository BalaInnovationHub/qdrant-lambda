FROM python:3.10-slim
WORKDIR /app
COPY . /app
RUN pip install qdrant_client
RUN pip install sentence_transformers
#EXPOSE 80
#CMD [ "python3","app.py", "--host", "0.0.0.0", "--port", "80" ]
