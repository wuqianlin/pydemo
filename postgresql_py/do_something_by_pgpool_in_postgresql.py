#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import uuid
import logging
import psycopg2

logger = logging.getLogger('cmpp')
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
fmt = '[%(asctime)s][line:%(lineno)d]: %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(fmt, datefmt)
ch.setFormatter(formatter)
logger.addHandler(ch)

uid = uuid.uuid4()
uid = str(uuid.uuid4())
suid = ''.join(uid.split('-'))
table_name = "student_{}".format(suid)


PGPOOL_POSTGRESQL = {
    "host": "192.168.0.6",
    "port": "9999",
    "user": "postgres",
    "password": "postgres",
    "database": "test",
}

POSTGRESQL01_POSTGRESQL = {
    "host": "192.168.0.4",
    "port": "5432",
    "user": "postgres",
    "password": "postgres",
    "database": "test",
}

POSTGRESQL02_POSTGRESQL = {
    "host": "192.168.0.5",
    "port": "5432",
    "user": "postgres",
    "password": "postgres",
    "database": "test",
}

# create connection
conn = psycopg2.connect(**PGPOOL_POSTGRESQL)
cur = conn.cursor()  # create cursor

# create table
create_table_sql = "CREATE TABLE {}(id integer,name varchar,sex varchar);".format(table_name)
cur.execute(create_table_sql)
logger.info("{} execute: ".format(PGPOOL_POSTGRESQL['host']) + create_table_sql)

# insert data
insert_sql = [
    ("INSERT INTO {}(id,name,sex)VALUES(%s,%s,%s)".format(table_name), (1, 'Aspirin', 'M')),
    ("INSERT INTO {}(id,name,sex)VALUES(%s,%s,%s)".format(table_name), (2, 'Taxol', 'F')),
    ("INSERT INTO {}(id,name,sex)VALUES(%s,%s,%s)".format(table_name), (3, 'Dixheral', 'M'))
]
for s in insert_sql:
    cur.execute(*s)
    logger.info("{} execute: ".format(PGPOOL_POSTGRESQL['host']) + str(s))


# get the result
select_sql = 'SELECT * FROM {}'.format(table_name)

cur.execute(select_sql)
logger.info("{} execute: ".format(PGPOOL_POSTGRESQL['host']) + select_sql)
results = cur.fetchall()
print(results)

# close the connection
conn.commit()
cur.close()
conn.close()

postgresql01_conn = psycopg2.connect(**POSTGRESQL01_POSTGRESQL)
postgresql01_cur = postgresql01_conn.cursor()
postgresql01_cur.execute(select_sql)
logger.info("{} execute: ".format(POSTGRESQL01_POSTGRESQL['host']) + select_sql)
results = postgresql01_cur.fetchall()
logger.info("result: {}".format(results))
postgresql01_cur.close()
postgresql01_conn.close()

postgresql02_conn = psycopg2.connect(**POSTGRESQL02_POSTGRESQL)
postgresql02_cur = postgresql02_conn.cursor()
postgresql02_cur.execute(select_sql)
logger.info("{} execute: ".format(POSTGRESQL02_POSTGRESQL["host"]) + select_sql)
results = postgresql02_cur.fetchall()
logger.info("result: {}".format(results))
postgresql02_cur.close()
postgresql02_conn.close()
