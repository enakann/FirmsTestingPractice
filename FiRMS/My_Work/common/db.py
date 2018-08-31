import cx_Oracle as Database

class DBUtils(object):
    """
    A class for handling DB operations
    
    def __init__(self,user,password,host,port,sid):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.sid  = sid
    """
    def __init__(self,tnsname):
        self.tnsname = tnsname

    def connect(self):
        """
        Create connection
        """
        #constring = '{}/{}@{}:{}/{}'.format(self.user,self.password,self.host,self.port,self.sid)
        constring = '/@{}'.format(self.tnsname)
        try:
            self.conn = Database.connect(constring)
        except (Database.OperationalError, Database.DatabaseError, Database.InterfaceError) as e:
            raise Exception(e)

        self.conn.autocommit=False
        self.cursor = self.conn.cursor()
   
    def fetchall(self):
        """
        fetch all at once
        """
        data_list = self.cursor.fetchall()
        return data_list 

    def fetchmany(self, num_rows):
        """
        Iterator based fetchmany call to keep memory usage low
        """
        while True:
            results = self.cursor.fetchmany(num_rows)
            if not results:
                break
            yield results
            #for result in results:
            #    yield [result]
    
    def fetchone(self):
        """
        fetch the first row only
        """
        data=None
        d = self.cursor.fetchone()
        if d is not None:
            (data,) = d
        return data

    def prepare(self,query):
        """
        prepare query
        """
        self.cursor.prepare(query)

    def insertrows(self, sql, record_list):
        """
        prepare query and insert rows
        """
        self.prepare(sql)
        # execute
        try:
            for rec in record_list:
                try:
                    self.cursor.execute(None, rec)
                except Database.DatabaseError as e:
                    x = e.args[0]
                    # Message:ORA-00001: unique constraint
                    if hasattr(x, 'code') and hasattr(x, 'message') and x.code == 1 and 'ORA-00001' in x.message:
                        print 'Integrity error: unique constraint violated'
                        pass
                    else:
                        raise
            #self.conn.commit()
        except:
            raise

    def rollback(self):
        self.conn.rollback()

    def commit(self):
        self.conn.commit()

    def execute(self, sql, bind_values=None):
        if bind_values is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql,bind_values)

    def close(self):
        self.cursor.close()
        self.conn.close()
