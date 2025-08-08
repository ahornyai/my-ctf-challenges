FROM debian

# Install sqlite3
RUN apt update -y && apt install -y sqlite3

# Set the working directory in the container
WORKDIR /chall

COPY init_db.sh .
COPY bitlock_app .
COPY static/ .
COPY templates/ .

RUN ./init_db.sh

EXPOSE 5858

CMD "/chall/bitlock_app"