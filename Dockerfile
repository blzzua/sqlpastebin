FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py logic.py ./
COPY highlighter ./highlighter
COPY templates ./templates
COPY upload ./upload
COPY uploader ./uploader
COPY static ./static

COPY Consolas-Regular.ttf DejaVuSansMono.ttf /usr/share/fonts/truetype/
RUN fc-cache -f -v


EXPOSE 11900

CMD ["gunicorn", "--bind", "0.0.0.0:11900", "app:app"]

