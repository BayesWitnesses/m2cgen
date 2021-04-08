FROM ubuntu:focal

ARG python=3.8

ENV JAVA_HOME=/usr/lib/jvm/zulu-8-amd64 \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    TZ=Etc/UTC \
    MKL_NUM_THREADS=2 \
    NUMEXPR_NUM_THREADS=2 \
    OMP_NUM_THREADS=2 \
    OPENBLAS_NUM_THREADS=2 \
    VECLIB_MAXIMUM_THREADS=2 \
    BLIS_NUM_THREADS=2

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    echo '* soft memlock unlimited' >> /etc/security/limits.conf && \
    echo '* hard memlock unlimited' >> /etc/security/limits.conf && \
    echo '* soft stack unlimited' >> /etc/security/limits.conf && \
    echo '* hard stack unlimited' >> /etc/security/limits.conf && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        apt-transport-https \
        curl \
        dirmngr \
        dpkg-dev \
        gpg-agent \
        locales \
        software-properties-common \
        wget && \
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
        dart \
        dotnet-sdk-5.0 \
        g++ \
        gcc \
        git \
        golang-go \
        haskell-platform \
        php \
        powershell \
        python${python}-dev \
        python3-pip \
        python3-setuptools \
        r-base \
        ruby-full \
        zulu-8 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /m2cgen

COPY requirements-test.txt ./
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${python} 1 && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir Cython "numpy==1.19.2" && \
    pip install --no-cache-dir -r requirements-test.txt
