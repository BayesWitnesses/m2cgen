FROM python:3.7

ENV JAVA_HOME /java

WORKDIR /tmp
RUN wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz && \
    tar xvf openjdk-11*_bin.tar.gz && \
    mv jdk-11* ${JAVA_HOME} && \
    rm openjdk-11*_bin.tar.gz

WORKDIR /m2cgen
COPY Pipfile* ./

RUN pip install pipenv
RUN pipenv sync --dev

CMD pipenv run pip install . && pipenv run pytest -v -x --fast
