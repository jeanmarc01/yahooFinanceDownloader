FROM python:2.7

#the main program
ADD yahooFinanceDownloader.py /

#Update
RUN apt-get update

#yahooFinance Library
ADD yahoo-finance /yahoo-finance
RUN cd /yahoo-finance && python setup.py install

#MariaDB connector
RUN pip install mysql-connector==2.1.4

#Download and install APScheduler
RUN pip install apscheduler

CMD ["python", "./yahooFinanceDownloader.py"]
