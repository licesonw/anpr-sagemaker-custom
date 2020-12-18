FROM ubuntu:latest

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3.6 \
         nginx \
         python3-pip \
         ca-certificates \
         ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://bootstrap.pypa.io/get-pip.py && \
    pip3 install h5py==2.10.0 keras tensorflow numpy scikit-learn uvicorn gunicorn flask gevent opencv-python && \
        rm -rf /root/.cache

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image
COPY ./src /opt/program
COPY ./models /opt/ml/model

RUN chmod +x /opt/program/serve

WORKDIR /opt/program