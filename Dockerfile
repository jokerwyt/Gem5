FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Shanghai


RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y build-essential git m4 scons zlib1g 
RUN apt-get install -y zlib1g-dev libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev
RUN apt-get install -y python3-dev python-is-python3 libboost-all-dev pkg-config

CMD ["/bin/bash"]

