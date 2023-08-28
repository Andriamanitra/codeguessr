FROM python:3.11-alpine
RUN mkdir /app
WORKDIR /app
RUN pip3 install sanic[ext]
COPY server.py /app/
CMD python3 server.py
