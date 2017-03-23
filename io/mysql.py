'''
Created on 27/06/2013

@author: Mads M. Pedersen (mmpe@dtu.dk)

usage:

with MySqlReader(server="10.40.20.10", database="poseidon", username='mmpe', password='password') as reader:
    print (reader.tables())

'''

from mmpe.functions.deep_coding import to_str
from mmpe.functions.timing import print_time
import warnings
import os


#import mysqlclient as MySQLdb
try:
    import MySQLdb
except:
    pass
try:
    import pymysql as MySQLdb
except:
    pass
import numpy as np
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import pandas as pd


#desc = {
#    'DECIMAL':       (0x00, 'DECIMAL'),
#    'TINY':          (0x01, 'TINY'),
#    'SHORT':         (0x02, 'SHORT'),
#    'LONG':          (0x03, 'LONG'),
#    'FLOAT':         (0x04, 'FLOAT'),
#    'DOUBLE':        (0x05, 'DOUBLE'),
#    'NULL':          (0x06, 'NULL'),
#    'TIMESTAMP':     (0x07, 'TIMESTAMP'),
#    'LONGLONG':      (0x08, 'LONGLONG'),
#    'INT24':         (0x09, 'INT24'),
#    'DATE':          (0x0a, 'DATE'),
#    'TIME':          (0x0b, 'TIME'),
#    'DATETIME':      (0x0c, 'DATETIME'),
#    'YEAR':          (0x0d, 'YEAR'),
#    'NEWDATE':       (0x0e, 'NEWDATE'),
#    'VARCHAR':       (0x0f, 'VARCHAR'),
#    'BIT':           (0x10, 'BIT'),
#    'NEWDECIMAL':    (0xf6, 'NEWDECIMAL'),
#    'ENUM':          (0xf7, 'ENUM'),
#    'SET':           (0xf8, 'SET'),
#    'TINY_BLOB':     (0xf9, 'TINY_BLOB'),
#    'MEDIUM_BLOB':   (0xfa, 'MEDIUM_BLOB'),
#    'LONG_BLOB':     (0xfb, 'LONG_BLOB'),
#    'BLOB':          (0xfc, 'BLOB'),
#    'VAR_STRING':    (0xfd, 'VAR_STRING'),
#    'STRING':        (0xfe, 'STRING'),
#    'GEOMETRY':      (0xff, 'GEOMETRY'),
#}

#class Cursor(object):
#    def __init__(self, mySqlBase):
#        self.mySqlBase = mySqlBase
#
#    @print_time
#    def __enter__(self):
#        self.db = MySQLdb.connect(host=self.mySqlBase.server,
#                             user=self.mySqlBase.username,
#                             passwd=self.mySqlBase.password,
#                             db=self.mySqlBase.database)
#        self.cursor = self.db.cursor()
#        return self.cursor
#
#    def __exit__(self, type, value, traceback):
#        self.cursor.close()
#        self.db.close()

no_connections = 0

class MySqlBase(object):
    def __init__(self, server, database, username="", password=None, port=3306):
        self.server = server
        if hasattr(username, "__call__"):
            username = username()
        if hasattr(password, "__call__"):
            password = password()
        self.username = username
        self.password = password
        self.database = database
        self.port = port
        #self.tables()
        self.mysql40 = server in ['ri-veadbs03']

    def __enter__(self):
        #global no_connections
        #no_connections += 1
        #print ("connect", no_connections)
        if not self.mysql40:
            self.db = MySQLdb.connect(host=self.server,
                         user=self.username,
                         passwd=self.password,
                         db=self.database, port=self.port)
            self.cursor = self.db.cursor()
        return self

    def __exit__(self, type, value, traceback):
        #global no_connections
        if not self.mysql40:
            self.cursor.close()
            delattr(self, "cursor")
            self.db.close()
            delattr(self, "db")
        #no_connections -= 1
        #print ("close", no_connections)

    def open(self):
        return self.__enter__()

    def close(self):
        self.__exit__(None, None, None)


class MySqlReader(MySqlBase):

    def __init__(self, server, database, username="", password=None, port=3306):
        MySqlBase.__init__(self, server, database, username=username, password=password, port=port)

    def read(self, query):
        if self.mysql40:
            exe = os.path.join(os.path.dirname(__file__), 'mysql40reader.exe')
            #print ("""%s %s %s %s %s "%s" tmp.h5"""%(exe, self.server, self.username, "xxx", self.port, query))
            os.system("""%s %s %s %s %s %s "%s" tmp.h5"""%(exe, self.server, self.database, self.username, self.password, self.port, query))
            data = pd.read_hdf("tmp.h5", 'data')
            return data
        else:
            try:
                return pd.read_sql(query, self.db)
            except Exception as e:
                e.args = e.args + (query,)
                raise e

    
    def read_txt(self, query):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            description = self.cursor.description
            return result, description
        except Exception as e:
            e.args = e.args + (query,)
            raise e

    

    def tables(self):
        return self.read("SHOW TABLES").iloc[:,0].tolist()

    def table_exists(self, table):
        return table in self.tables()

    def fields(self, table, column_lst="*"):
        columns, _ = self.read("SHOW COLUMNS FROM %s" % table)
        if column_lst != "*":
            columns = [c for c in columns if to_str(c[0]) in column_lst]
        return columns

    def shape(self, table, sensor_list="*", first_row=0, last_row=10 ** 100, where="True"):
        sql = "SELECT COUNT(*) as rows FROM (select * FROM %s as t1 WHERE %s limit %d,%d) as t2" % (table, where, first_row, last_row - first_row)
        no_rows, _ = self.read(sql)
        return (no_rows[0][0], len(self.fields(table, sensor_list)))

    def __str__(self):
        return "MySqlReader('%s', '%s', '%s', None)" % (self.server, self.database, self.username)


class MySqlWriter(MySqlReader):
    def insert(self, table, values, fields=None):
        if fields is None:
            fields = ""
        elif isinstance(fields, (list, tuple)):
            fields = "(%s)" % ", ".join(fields)
        else:
            fields = "(%s)" % fields

        if isinstance(values, (list, tuple, np.ndarray, pd.DataFrame)) and len(values) > 0:
            df = pd.DataFrame(values)
            df = df.where(pd.notnull(df), None)
            values = [row[1:] for row in df.itertuples()]


        if isinstance(values, (list, tuple)) and len(values) > 0:
            if isinstance(values[0], (list, tuple)):
                # list of list => execute many
                sql = "INSERT INTO %s %s Values (%s)" % (table, fields, ", ".join(["%s"] * len(values[0])))
                self.cursor.executemany(sql, values)
            else:
                sql = "INSERT INTO %s %s Values (%s)" % (table, fields, ", ".join(["%s"] * len(values)))
                self.cursor.execute(sql, values)
        else:
            sql = "INSERT INTO %s %s Values(%s)" % (table, fields, values)
            self.cursor.execute(sql)

    #@print_time
    def update(self, table, field, values, condition_fields, conditions, verbose=False):
        import pandas as pd
        values = pd.DataFrame(np.atleast_1d(values))
        if not isinstance(conditions, (list, tuple, np.ndarray)):
            conditions = [conditions]
        conditions = pd.DataFrame(conditions)

        condition_fields = np.atleast_1d(condition_fields)
        where = " AND ".join(["%s=%%s" % cf for cf in condition_fields])
        sql = "UPDATE %s SET %s=%%s WHERE %s" % (table, field, where)


        assert values.shape[0] == conditions.shape[0]
        assert condition_fields.shape[0] == conditions.shape[1]

        args = pd.concat([values, conditions], 1)
        args = [[f for f in row] for _, row in args.iterrows()]
        if verbose:
            print (sql)
            print (args)

        self.cursor.executemany(sql, args)

    #@print_time
    def execute(self, sql, args=None):
        return self.cursor.execute(sql, self.replace_nan(args))

    def replace_nan(self, args):
        def fmt(arg):
            if isinstance(arg, (list, tuple, np.ndarray)):
                return self.replace_nan(arg)
            if isinstance(arg, float):
                if np.isnan(arg):
                    return None
                else:
                    return float(arg)
            else:
                return arg
        if args is None:
            return args
        return list(map(fmt, args))


    def format_args(self, args):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            df = pd.DataFrame(args)
            df = df.where(pd.notnull(df), None)
            args = list(zip(*[df[k].values.tolist() for k in df.keys()]))
            return args

    #@print_time
    def executemany(self, sql, args):
        args = self.replace_nan(args)  #self.format_args(args)
        return self.cursor.executemany(sql, args)

