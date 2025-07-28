FROM debian:bookworm
LABEL author="tkimhofer@gmail.com"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update -y
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN pip3 install --break-system-packages -r requirements.txt


COPY . .
RUN chmod 777 /app/bconvert1.py

ENTRYPOINT ["python3", "bconvert.py"]

