FROM python:3.10-slim

RUN mkdir /wb_bot

WORKDIR /wb_bot

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .
