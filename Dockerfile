# $DEL_BEGIN

# ####### 👇 SIMPLE SOLUTION (x86 and M1) 👇 ########
# FROM python:3.8.12-buster
# WORKDIR /prod
# COPY taxifare taxifare
# COPY requirements.txt requirements.txt
# COPY setup.py setup.py
# RUN pip install .
# CMD uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT

####### 👇 OPTIMIZED SOLUTION (x86)👇  (May be too advanced for ML-Ops module but useful for the project weeks) #######

# tensorflow base-images are optimized: lighter than python-buster + pip install tensorflow
#FROM tensorflow/tensorflow:2.10.0

# KHD: 05.12.2022
# Use this image to work with FB Prophet
#FROM python:3.8.13
FROM python:3.8.12-buster

# OR for apple silicon, use this base image instead
# FROM armswdev/tensorflow-arm-neoverse:r22.09-tf-2.10.0-eigen

WORKDIR /prod

# KHD start
#RUN apt update
#RUN apt-get install -y --no-install-recommends g++ build-essential git python3-dev gcc libc-dev wget rpm
#RUN pip3 install --upgrade pip


RUN apt-get -y update  && apt-get install -y \
  python3-dev \
  apt-utils \
  python-dev \
  build-essential \
&& rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade setuptools
RUN pip install cython
RUN pip install numpy
RUN pip install matplotlib
RUN pip install pystan
RUN pip install prophet

# KHD end

#COPY go /usr/local/go
#COPY tiniworld_core tiniworld_timeseries/tiniworld_core
#COPY webapp tiniworld_timeseries/webapp
COPY tiniworld_core tiniworld_core
COPY webapp webapp
COPY raw_data raw_data

# For testing/dev purpose but not in production
COPY raw_data /root/.tiniworld_timeseries/mlops/data
COPY training_outputs /root/.tiniworld_timeseries/mlops/training_outputs
COPY raw_data /home/.tiniworld_timeseries/mlops/data
COPY training_outputs /home/.tiniworld_timeseries/mlops/training_outputs

#RUN mkdir -p /root/.tiniworld_timeseries/mlops/training_outputs


# We strip the requirements from useless packages like `ipykernel`, `matplotlib` etc...
COPY requirements_prod.txt requirements.txt
COPY setup.py setup.py
RUN pip install .
#RUN pip install -r ./requirements.txt

# Copy .env with DATA_SOURCE=local and MODEL_TARGET=mlflow
#COPY .env .env

# A build time, download the model from the MLflow server and copy it once for all inside of the image
#RUN python -c 'from dotenv import load_dotenv, find_dotenv; load_dotenv(find_dotenv()); \
#    from taxifare.ml_logic.registry import load_model; load_model(save_copy_locally=True)'

# Then, at run time, load the model locally from the container instead of querying the MLflow server, thanks to "MODEL_TARGET=local"
# This avoids to download the heavy model from the Internet every time an API request is performed
#CMD MODEL_TARGET=local uvicorn taxifare.api.fast:app --host 0.0.0.0 --port $PORT

# Run the Streamlit app (default port is 8501)
EXPOSE 8080
#CMD streamlit run webapp/Home.py --server.port 8080
CMD streamlit run webapp/0_🏠_Home.py --server.port 8080

# $DEL_END
