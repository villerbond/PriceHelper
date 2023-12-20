FROM python:3.8

RUN mkdir src
WORKDIR src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD ./PriceHelper/requirements.txt /src/
RUN pip install -r requirements.txt

ADD ./PriceHelper /src/

ENTRYPOINT ./entrypoint.sh