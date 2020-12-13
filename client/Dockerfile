FROM python:3.9.0-buster

WORKDIR /opt/app
ENV PYTHONPATH=/opt/app:${PYTHONPATH}


COPY ./ .

EXPOSE 8080

RUN python -m pip install -r requirements.txt
CMD ["python3", "main.py"]
