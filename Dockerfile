FROM python:3.7.7
COPY . /StopSpot_Data_Pipeline
RUN python -m pip install \
        pipenv \
        parse \
        realpython-reader \
        pandas \
        sqlalchemy \
        psycopg2
WORKDIR "/StopSpot_Data_Pipeline"
CMD python3 main.py --daily