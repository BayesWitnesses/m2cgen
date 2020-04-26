FROM ubuntu:xenial

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN apt-get update && \
    apt-get install -y software-properties-common wget apt-transport-https && \
    add-apt-repository ppa:deadsnakes/ppa && \
    wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    wget -qO- https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        git \
        gcc \
        g++ \
        libc-dev \
        libgomp1 \
        python3.7 \
        python3-setuptools \
        python3-pip \
        python3.7-dev \
        openjdk-8-jdk \
        golang-go \
        dotnet-sdk-3.0 \
        powershell \
        r-base \
        php \
        dart \
        haskell-platform && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /m2cgen

COPY requirements-test.txt ./
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1 && \
    pip3 install --upgrade pip && \
    pip3 install --no-cache-dir Cython numpy && \
    pip3 install --no-cache-dir -r requirements-test.txt

CMD python3 setup.py develop && pytest -v -x --fast
