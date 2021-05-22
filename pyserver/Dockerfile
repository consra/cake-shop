FROM python:3.6

EXPOSE 5000

WORKDIR /pyserver

COPY requirements.txt /pyserver
RUN pip install -r requirements.txt

COPY server.py /pyserver
CMD python server.py