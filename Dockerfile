FROM python:3.11

RUN mkdir /bot

WORKDIR /bot

RUN pip install --upgrade pip

COPY requirements.txt /bot/requirements.txt

RUN pip install -r requirements.txt

COPY src /bot/src

ENTRYPOINT ["python", "src/bot.py"]