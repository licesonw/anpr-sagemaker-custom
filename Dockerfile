FROM ubuntu:latest

# Install system dependencies
RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3.6 \
         nginx \
         python3-pip \
         ca-certificates \
         ffmpeg libsm6 libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    pip3 install h5py==2.10.0 keras tensorflow numpy scikit-learn uvicorn gunicorn flask gevent opencv-python && \
        rm -rf /root/.cache

# Set python env variables and make sure the executable is added to the path
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# Set up the program in the image and add execution rights
COPY ./src /opt/program
RUN chmod +x /opt/program/serve

# For debugging we can copy the model artifacts directly into the folder, comment for using with SageMaker
#COPY ./models /opt/ml/model

WORKDIR /opt/program