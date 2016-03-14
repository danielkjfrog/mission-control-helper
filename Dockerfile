FROM python:2.7

MAINTAINER Daniel Keler <danielk@jfrog.com>

RUN apt-get update && apt-get install -y python-pip

ADD requirements.txt /tmp/requirements.txt

RUN chmod +r /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

ADD populate.py /tmp/populate.py

RUN chmod +x /tmp/populate.py

WORKDIR /tmp/

CMD python /tmp/populate.py
