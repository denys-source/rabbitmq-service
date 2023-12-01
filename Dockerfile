FROM python:3.11.3-alpine

WORKDIR /code/

COPY . .

RUN pip install -r ./requirements.txt

ENV PYTHONUNBUFFERED=1

CMD [ "python3", "main.py" ]
