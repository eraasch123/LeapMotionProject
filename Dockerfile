FROM python:3.5
ADD Sample.py ./
ADD Makefile ./
RUN apt-get update && apt-get install -y \
    sudo \
    wget \
	patch \
	swig \
	libpython3-dev \
	g++ \
	build-essential\
	gcc
RUN sudo apt-get install -y python3-dev
RUN sudo make
RUN sudo make install
CMD [ "python", "Sample.py" ]