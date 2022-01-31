# start by pulling the python image
FROM python:3.8-alpine

ENV PYTHONUNBUFFERED True
ENV PORT 8080

# copy the requirements file into the image
COPY "./requirements.txt" "/flask-swiftdoc-1.0/requirements.txt"

# switch working directory
ENV APP_HOME "/flask-swiftdoc-1.0"
WORKDIR $APP_HOME
COPY . ./


RUN apk --no-cache add \
    build-base \
    python3 \
    python3-dev \
    openssl \
    bash \
    git \
    py3-pip \
    sudo \
    freetype-dev \
    fribidi-dev \
    harfbuzz-dev \
    jpeg-dev \
    lcms2-dev \
    openjpeg-dev \
    tcl-dev \
    tiff-dev \
    tk-dev \
    zlib-dev

# install the dependencies and packages in the requirements file
RUN #pip install --upgrade google-api-python-client

RUN #pip install --upgrade google-cloud-storage

RUN pip install -r requirements.txt

# copy every content from the local file to the image
#COPY . /app

# configure the container to run in an executed manner
#ENTRYPOINT [ "python" ]

#CMD ["app.py" ]
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app