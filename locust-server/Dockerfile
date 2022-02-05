FROM locustio/locust

COPY requirements.txt .
COPY ./scripts/ /scripts/

RUN pip install -U pip && pip install -r requirements.txt

EXPOSE 8089
EXPOSE 5557
EXPOSE 5558