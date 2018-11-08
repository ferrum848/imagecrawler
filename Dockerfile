FROM ubuntu:16.04

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential=12.1ubuntu2 \
        cmake=3.5.1-1ubuntu3 \
        nano=2.5.3-2ubuntu2 \
        ca-certificates=20170717~16.04.1 \
        libjpeg-dev=8c-2ubuntu8 \
        libpng-dev \
        software-properties-common=0.96.20.7 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log

RUN apt-get update && \ 
	apt-get install -y curl

##############################################################################
# Miniconda & python 3.6
##############################################################################
RUN curl -sSL https://repo.continuum.io/miniconda/Miniconda3-4.5.4-Linux-x86_64.sh -o /tmp/miniconda.sh \
    && bash /tmp/miniconda.sh -bfp /usr/local \
    && rm -rf /tmp/miniconda.sh \
    && conda install -y python=3.6.5 \
    && conda clean --all --yes

ENV PATH /opt/conda/bin:$PATH


##############################################################################
# Java to run Pycharm
##############################################################################
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        default-jre=2:1.8-56ubuntu2 \
        default-jdk=2:1.8-56ubuntu2 \
    && apt-get -qq -y autoremove \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    && ln -s /usr/lib/jvm/java-7-openjdk-amd64 /jre

ENV JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
############################



RUN apt-get install -y libffi-dev
RUN apt-get install -y libssl-dev
RUN apt-get install -y libxml2-dev libxslt1-dev


RUN pip install pillow
RUN pip install scrapy





