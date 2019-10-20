FROM python:3.7

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb && \
    dpkg -i packages-microsoft-prod.deb && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        openjdk-8-jdk \
        golang-go \
        dotnet-sdk-3.0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /m2cgen

COPY requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements-test.txt

CMD python setup.py develop && pytest -v -x --fast
