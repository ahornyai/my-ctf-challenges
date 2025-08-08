# Use an official Python runtime as a parent image
FROM python:3.13-slim

RUN apt update -y
RUN apt install -y socat

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /chall

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY challenge.py .

EXPOSE 1234

CMD ["socat", "TCP-LISTEN:1234,reuseaddr,fork", "EXEC:'/chall/challenge.py'"]
