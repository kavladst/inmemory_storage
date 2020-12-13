FROM python:3.9.0-buster

WORKDIR /opt/app
ENV PYTHONPATH=/opt/app:${PYTHONPATH}


COPY ./ .

RUN python -m pip install -r requirements.txt
CMD ["pytest", "src"]
