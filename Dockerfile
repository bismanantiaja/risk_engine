FROM continuumio/anaconda3:2019.10

RUN apt-get -y update --fix-missing
RUN apt-get -y install python3-pip
RUN conda update conda
RUN conda install numpy
RUN conda install pandas
RUN conda install -c conda-forge glmnet
RUN conda install scikit-learn
RUN conda install geopandas
RUN pip install xgboost
RUN pip install google-auth
RUN pip install pyopenSSL
RUN pip install gspread

WORKDIR /project
ADD . /project
CMD ["python","app.py"]
