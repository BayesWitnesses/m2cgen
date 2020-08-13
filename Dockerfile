FROM ubuntu:bionic

ARG python=3.8

ENV JAVA_HOME /usr/lib/jvm/zulu-8-amd64
ENV LC_ALL en_US.UTF-8
ENV TZ Etc/UTC

RUN apt-get update && \
    apt-get install --no-install-recommends -y \
        gpg-agent \
        dirmngr \
        locales \
        software-properties-common \
        wget \
        apt-transport-https && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    locale-gen $LC_ALL && \
    update-locale && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    wget -qO- https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9 && \
    add-apt-repository "deb http://repos.azulsystems.com/ubuntu stable main" -y && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        git \
        gcc \
        g++ \
        libc-dev \
        libgomp1 \
        python${python}-dev \
        python3-setuptools \
        python3-pip \
        zulu-8 \
        golang-go \
        dotnet-sdk-3.1 \
        powershell \
        r-base \
        php \
        dart \
        haskell-platform \
        ruby-full && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /m2cgen

COPY requirements-test.txt ./
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${python} 1 && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir Cython numpy && \
    pip install --no-cache-dir -r requirements-test.txt
