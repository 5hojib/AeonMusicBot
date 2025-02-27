FROM python:3.13-slim

WORKDIR /usr/src/app

# Install git and clean up to reduce image size
RUN apt update && apt install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "start.sh"]