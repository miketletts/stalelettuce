#!/usr/bin/env python3.8

from pandas import DataFrame, options, read_sql_query
from sqlalchemy import create_engine, text
import os
import psycopg2


options.display.max_columns = None


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

    schemas_query = """
        select
            t.table_schema,
            count(distinct t.table_name) num_tables
        from information_schema.tables t
        group by 1
        order by 1;
    """

    tables_query = """
        select
            t.table_schema,
            t.table_name
        from information_schema.tables t
        order by 1, 2;
    """

    def __init__(
        self,
        dbname,
        host=os.environ.get("REDSHIFT_ENDPOINT"),
        port=os.environ.get("PORT"),
        username=os.environ.get("REDSHIFT_USER"),
        password=os.environ.get("REDSHIFT_PASSWORD")
    ):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.dbname = dbname
        self.engine = self.createEngine()
        self.schemas = self.query(sql=Redshift.schemas_query)
        self.tables = self.query(sql=Redshift.tables_query)

    def createEngine(self):
        engine_string = \
            f"postgresql+psycopg2://{self.username}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        print(f"Successfully created engine via {engine_string}")
        return create_engine(engine_string)

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
        return read_sql_query(text(sql), self.engine)

    def columns(self, schema_name, table_name):
        """
        -----------
        DESCRIPTION:
        -----------
        Use this function to return the ordinal position, name, and data type
        of every column in a specific table. You must pass the schema and table
        names as args. If you are unsure what schema and tables exist, reference
        the 'tables' and 'schemas' attributes of the Redshift instance.
        -----------
        ARGS:
        -----------
        schema_name (str): schema name.
        table_name (str): table name.
        """
        sql = f"""
            select
                c.table_schema,
                c.table_name,
                c.ordinal_position as position,
                c.column_name,
                c.data_type
            from information_schema.columns c
            where
                c.table_name = '{table_name}'
                and c.table_schema = '{schema_name}'
            order by 3;
        """
        return self.query(sql=sql)
