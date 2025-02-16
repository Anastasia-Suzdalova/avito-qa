FROM python:3.13

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip python3.11-venv

COPY requirements.txt /requirements.txt

RUN python3 -m venv venv
RUN . venv/bin/activate && pip install pytest && pip install -r /requirements.txt

COPY . /tests

RUN chmod +x /tests/tests.sh

CMD ["/tests/tests.sh"]
