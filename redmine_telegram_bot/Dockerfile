FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . ./
RUN chmod +x ./server-entrypoint.sh
RUN chmod +x ./worker-entrypoint.sh
RUN chmod +x ./beat-entrypoint.sh