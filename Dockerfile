FROM python

WORKDIR /app

COPY . /app

CMD [  "app.py" ]