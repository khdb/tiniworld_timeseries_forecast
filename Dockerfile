
FROM python:3.8.12-buster

WORKDIR /prod

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


COPY tiniworld_core tiniworld_core
COPY webapp webapp


COPY setup.py setup.py
RUN pip3 install -r requirements.txt


COPY raw_data /root/.tiniworld_timeseries/mlops/data
#COPY training_outputs /root/.tiniworld_timeseries/mlops/training_outputs
COPY raw_data /home/.tiniworld_timeseries/mlops/data
#COPY training_outputs /home/.tiniworld_timeseries/mlops/training_outputs

# Run the Streamlit app (default port is 8501)
EXPOSE 8501

CMD streamlit run webapp/0_🏠_Home.py --server.port 8501
