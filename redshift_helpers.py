#!/usr/bin/env python3.8

from itertools import groupby
from pandas import DataFrame, read_sql_query
from sqlalchemy import create_engine, text
import os
import psycopg2


REDSHIFT_ENDPOINT = os.environ.get("REDSHIFT_ENDPOINT")
PORT = os.environ.get("PORT")
REDSHIFT_USER = os.environ.get("REDSHIFT_USER")
REDSHIFT_PASSWORD = os.environ.get("REDSHIFT_PASSWORD")


class Redshift(object):
    """
    -----------
    DESCRIPTION
    -----------
    Use this class to explore a specific database in a Redshift cluster
    associated with LeafLink. The sql engine, schema, and table name objects can
    be accessed once the class has been initialized. These objects are named
    'engine', 'schemas', and 'tables', respectively.
    -----------
    ARGS
    -----------
    dbname (str): database name. no default value.
    host (str): AWS cluster endpoint name.
    port (int): AWS cluster port number.
    username (str): AWS username.
    password (str): AWS password.
    """

    def __init__(
        self,
        dbname,
        host=REDSHIFT_ENDPOINT,
        port=PORT,
        username=REDSHIFT_USER,
        password=REDSHIFT_PASSWORD
    ):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.dbname = dbname
        self.engine = self.createEngine()
        self.tables = self.dbTableNames()
        self.schemas = {key: len(list(group)) for key, group in self.tables.items()}

    def createEngine(self):
        engine_string = \
            f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        engine = create_engine(engine_string)
        print(f"Successfully created engine via {engine_string}")
        return engine

    def dbTableNames(self):
        sql = """
        select
            schemaname,
            tablename
        from pg_tables
        order by 1, 2
        """
        tables = {}
        for dataset, table in self.engine.execute(sql):
            try:
                tables[dataset].append(table)
            except KeyError:
                tables[dataset] = [table]

        return tables

    def query(self, sql):
        """
        -----------
        DESCRIPTION:
        -----------
        You can use this function to query Redshift.
        The results are returned as a pandas dataframe for your convenience.
        To use this function, just enter a valid query in a docstring.
        Then, pass this docstring to the function as an arg (i.e. sql).
        -----------
        ARGS:
        -----------
        sql (docstring): query.
        -----------
        EXAMPLE:
        -----------
        import stalelettuce as sl


        rs = sl.Redshift(dbname="db_name")
        sql = '''select distinct schemaname from pg_tables'''
        df = rs.query(sql)
        """
        df = read_sql_query(text(sql), self.engine)
        return df
