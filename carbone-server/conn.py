import os
import sys
import logging  # type: ignore
from autologging import logged, traced, TRACE  # type: ignore
from flask import Flask
from flask_restful import Resource, Api
from sqlalchemy import create_engine, insert, Table, Column, Integer, String, MetaData, text, select
from sqlalchemy.dialects.mysql import DATETIME, INTEGER, TINYINT, BIGINT, DATE
from prometheus_client import Summary, Counter

logging.basicConfig(level=TRACE, stream=sys.stdout,
                    format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")

meta = MetaData()

###
### Had to remove tables for anonymity 
###



global paycheck
paycheck = Table(
    'PAYCHECK', meta,
    Column('PAYCHECK_ID', BIGINT(unsigned=True), primary_key=True),
 
)

global company
company = Table(
    'COMPANY', meta,
    Column('COMPANY_NAME', String(100)),

)


global table_data_gets
check_gets = Counter('table_data_gets', 'Num of table_data get requests') 

global report_data_gets
user_data_gets = Counter('report_data_gets', 'Num of report_data get requests') 

global user_count_gets
user_count_gets = Counter('user_count_gets', 'Num of user_count get requests')

global table_data_errors
check_gets = Counter('table_data_errors', 'Num of table_data error requests') 

global report_data_errors
user_data_gets = Counter('report_data_errors', 'Num of report_data error requests') 

global user_count_errors
user_count_gets = Counter('user_count_errors', 'Num of user_count errors requests') 

'''MARIDB_HOST = os.environ.get('MARIDB_HOST', 'mysql+pymysql://')

engine = create_engine(MARIDB_HOST,
                       pool_pre_ping=True,
                       pool_recycle=3600,
                       echo=True,
                       query_cache_size=0,
                       execution_options={"isolation_level": "READ COMMITTED"})'''

engine = create_engine('mysql+pymysql://') #local
global connection
connection = engine.connect()
