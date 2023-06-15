FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

# RUN pip3 install --upgrade pip

COPY . .

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]