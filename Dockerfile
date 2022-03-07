# build environment
FROM ubuntu:devel

ENV PYTHONUNBUFFERED True
ENV PORT 8080
ENV DEBIAN_FRONTEND=noninteractive

# copy the requirements file into the image
COPY "./requirements.txt" "/ps-swiftdoc-2.0/requirements.txt"

# switch working directory
ENV APP_HOME "/ps-swiftdoc-2.0"
WORKDIR $APP_HOME
COPY . ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    apt-utils \
    build-essential \
    python3 \
    python3-dev \
    openssl \
    bash \
    git \
    python3-pip \
	python3-setuptools \
	python3-wheel \
    sudo \
    libfreetype6-dev \
    libfribidi-dev \
    libharfbuzz-dev \
    libjpeg8-dev \
    liblcms2-dev \
	libwebp-dev \
	libtiff5-dev \
	zlib1g-dev \
    tcl8.6-dev \
    tk8.6-dev \
	python3-tk

# install the dependencies and packages in the requirements file
#RUN pip install --upgrade google-api-python-client


RUN pip3 install -r requirements.txt

RUN pip3 install numpy

#CMD ["/usr/bin/python3", "app.py" ]

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app
