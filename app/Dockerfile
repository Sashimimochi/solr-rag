FROM nvidia/cuda:11.1.1-cudnn8-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

# mecabの導入
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y mecab libmecab-dev mecab-ipadic-utf8 \
    software-properties-common \
    git make curl xz-utils file sudo locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8

RUN add-apt-repository ppa:ubuntu-toolchain-r/test && \
    apt update && \
    apt install -y gcc-11 g++-11

RUN add-apt-repository ppa:deadsnakes/ppa && \
    apt update && \
    apt-get -y update && \
    apt-get -y upgrade && \
    apt-get remove -y --auto-remove python3 && \
    apt-get install -y python3.11 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1

WORKDIR /usr/local/src/mecab

# mecab-ipadic-NEologdのインストール
RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git && \
    cd mecab-ipadic-neologd && \
    ./bin/install-mecab-ipadic-neologd -n -y && \
    echo dicdir = `mecab-config --dicdir`"/mecab-ipadic-neologd">/etc/mecabrc && \
    sudo cp /etc/mecabrc /usr/local/etc

ENV LANG='ja_JP.UTF-8'
ENV LANGUAGE='ja_JP:ja'
ENV LC_ALL='ja_JP.UTF-8'
ENV TZ JST-9
ENV TERM xterm

WORKDIR /workspace/app

COPY requirements.txt .

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python get-pip.py && \
    python -m pip install --upgrade pip --no-cache-dir && \
    CXX=g++-11 CC=gcc-11 python -m pip install -r requirements.txt --no-cache-dir

RUN python -m pip install --no-cache-dir torch==2.0.0+cu117 torchvision==0.15.0+cu117 -f https://download.pytorch.org/whl/torch_stable.html
