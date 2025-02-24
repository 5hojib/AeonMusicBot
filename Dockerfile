FROM 5hojib/audiobot:beta

WORKDIR /usr/src/app

RUN uv venv -p python3.13-nogil
COPY requirements.txt .
RUN uv pip install --no-cache-dir -r requirements.txt

ENV PYTHON_GIL=0
EMV PYTHON_JIT=1

COPY . .

CMD ["bash", "start.sh"]
