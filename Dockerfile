FROM ubuntu:focal

ARG python=3.10

ENV JAVA_HOME=/usr/lib/jvm/zulu-8-amd64 \
    PATH="/root/.cargo/bin:$PATH" \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    TZ=Etc/UTC \
    BLIS_NUM_THREADS=2 \
    MKL_NUM_THREADS=2 \
    NUMBA_NUM_THREADS=2 \
    NUMEXPR_NUM_THREADS=2 \
    OMP_NUM_THREADS=2 \
    OPENBLAS_NUM_THREADS=2 \
    VECLIB_MAXIMUM_THREADS=2

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        apt-transport-https \
        dirmngr \
        dpkg-dev \
        gpg-agent \
        locales \
        software-properties-common \
        gnupg2 \
        wget && \
    locale-gen $LC_ALL && \
    update-locale && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb && \
    wget -q https://packages.erlang-solutions.com/erlang-solutions_2.0_all.deb -O erlang-solutions_2.0_all.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    dpkg -i erlang-solutions_2.0_all.deb && \
    wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    wget -qO- https://storage.googleapis.com/download.dartlang.org/linux/debian/dart_stable.list > /etc/apt/sources.list.d/dart_stable.list && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9 && \
    add-apt-repository "deb http://repos.azulsystems.com/ubuntu stable main" -y && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9 && \
    add-apt-repository "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" -y && \
    wget -qO- https://sh.rustup.rs | sh -s -- --no-modify-path --default-toolchain stable -y && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        dart \
        dotnet-sdk-6.0 \
        g++ \
        gcc \
        git \
        golang-go \
        haskell-platform \
        php \
        powershell \
        python${python}-dev \
        python${python}-distutils \
        python3-setuptools \
        r-base \
        ruby-full \
        zulu-8 \
        erlang-solutions \
        esl-erlang \
        elixir && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /m2cgen

COPY requirements-test.txt ./
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${python} 1 && \
    wget -qO- https://bootstrap.pypa.io/get-pip.py | python && \
    pip install --no-cache-dir -r requirements-test.txt
