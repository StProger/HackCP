FROM python:3.12

RUN mkdir /rutube_app

WORKDIR /rutube_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /rutube_app/docker/*.sh

ENV PYTHONPATH=./

CMD ["gunicorn", "main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]