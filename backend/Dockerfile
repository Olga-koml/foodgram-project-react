FROM python:3.10.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r /app/requirements.txt --no-cache-dir

# RUN pip3 install --upgrade pip

COPY foodgram/ .

COPY ../data/ .

COPY ../data/ingredients.json .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]