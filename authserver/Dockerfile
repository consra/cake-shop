FROM python:3.6

EXPOSE 5555

WORKDIR /authserver

COPY requirements.txt /authserver
RUN pip install -r requirements.txt

COPY authserver.py /authserver
CMD python authserver.py