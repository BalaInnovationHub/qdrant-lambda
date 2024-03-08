FROM public.ecr.aws/lambda/python:3.10.2024.03.04.10-x86_64
#python:3.11.2-slim-bullseye
COPY . .
RUN pip install qdrant_client
RUN pip install boto3
RUN pip install --upgrade pip && pip install --no-cache-dir sentence-transformers
#EXPOSE 80
#CMD [ "python3","app.py", "--host", "0.0.0.0", "--port", "80" ]
# Use an official Python runtime as a parent image
