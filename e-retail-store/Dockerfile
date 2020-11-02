FROM ubuntu:18.04

RUN apt-get -y update

RUN apt-get -y install python

RUN apt -y install python-pip

RUN pip install flask

RUN pip install lmdb

RUN pip install pillow

RUN apt-get -y install curl 

RUN pip install tabulate

WORKDIR /jay

COPY . /jay

EXPOSE 5000

ENTRYPOINT ["python"]

CMD ["app.py"]



