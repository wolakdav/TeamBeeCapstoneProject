FROM python:3.7.7
RUN python -m pip install \
        pipenv \
        parse \
        realpython-reader \
        pandas \
        sqlalchemy \
        psycopg2
WORKDIR "/StopSpot_Data_Pipeline"
CMD python3 main.py --help