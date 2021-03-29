#!/usr/bin/env python3.8

from pandas import DataFrame, read_sql_query
from sqlalchemy import create_engine, text
import os
import psycopg2


REDSHIFT_ENDPOINT=os.getenv("REDSHIFT_ENDPOINT")
PORT=os.getenv("PORT")
REDSHIFT_USER=os.getenv("REDSHIFT_USER")
REDSHIFT_PASS=os.getenv("REDSHIFT_PASS")


class Redshift(object):
    """
    -----------
    DESCRIPTION
    -----------
    Use this class to explore a specific database in a Redshift cluster
    associated with LeafLink. The sql engine and table name objects can be
    accessed once the class has been initialized. These objects are named
    'engine' and 'tables', respectively.
    -----------
    ARGS
    -----------
    DBNAME (str): database name. no default value.
    REDSHIFT_ENDPOINT (str): AWS cluster endpoint name.
    PORT (int): AWS cluster port number.
    REDSHIFT_USER (str): AWS username.
    REDSHIFT_PASS (str): AWS password.
    """

    def __init__(
        self,
        DBNAME,
        REDSHIFT_ENDPOINT=REDSHIFT_ENDPOINT,
        PORT=PORT,
        REDSHIFT_USER=REDSHIFT_USER,
        REDSHIFT_PASS=REDSHIFT_PASS
    ):
        self.REDSHIFT_ENDPOINT = REDSHIFT_ENDPOINT
        self.REDSHIFT_USER = REDSHIFT_USER
        self.REDSHIFT_PASS = REDSHIFT_PASS
        self.PORT = PORT
        self.DBNAME = DBNAME
        self.engine = self.createEngine()
        self.tables = self.dbTableNames()

    def createEngine(self):
        engine_string = \
            f"postgresql+psycopg2://{self.REDSHIFT_USER}:{self.REDSHIFT_PASS}@{self.REDSHIFT_ENDPOINT}:{self.PORT}/{self.DBNAME}"
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
        tables = [
            {"dataset": __[0], "table": __[1]} for __ in self.engine.execute(sql)
        ]
        return tables

    def printDbTableNames(self):
        print(*self.tables, sep="\n")

    def dbTableNamesDataFrame(self):
        df = DataFrame(self.tables)
        return df

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


        rs = sl.Redshift(DBNAME="db_name")
        sql = '''select schemaname from pg_tables'''
        df = rs.query(sql)
        """
        df = read_sql_query(text(sql), self.engine)
        return df
