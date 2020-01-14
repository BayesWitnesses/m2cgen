FROM ubuntu:xenial

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN apt-get update && \
    apt-get install -y software-properties-common wget apt-transport-https && \
    add-apt-repository ppa:deadsnakes/ppa && \
    wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        gcc \
        libc-dev \
        libgomp1 \
        python3.7 \
        python3-setuptools \
        python3-pip \
        openjdk-8-jdk \
        golang-go \
        dotnet-sdk-3.0 \
        powershell \
        r-base && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /m2cgen

COPY requirements-test.txt ./
RUN pip3 install --no-cache-dir -r requirements-test.txt

CMD python3 setup.py develop && pytest -v -x --fast
