FROM python:3.10.11

WORKDIR /src

RUN pip3 install --upgrade pip

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y wget

RUN wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz \
    && tar xvf ffmpeg-release-amd64-static.tar.xz \
    && rm ffmpeg-release-amd64-static.tar.xz \
    && mv ffmpeg-*-static/ffmpeg /usr/local/bin \
    && rm -r ffmpeg-*-static

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--forwarded-allow-ips", "'*'"]
