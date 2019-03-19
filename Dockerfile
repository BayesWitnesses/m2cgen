FROM python:3.7

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN apt-get update && \
    apt-get install --no-install-recommends -y openjdk-8-jdk golang-go && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /m2cgen

COPY requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements-test.txt

CMD python setup.py develop && pytest -v -x --fast
