FROM python:3.8.10

COPY ./resources/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

WORKDIR /app

CMD ["python3", "main.py"]

#docker build -t game .
#docker run -it --rm --name game game
