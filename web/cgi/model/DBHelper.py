#coding=utf-8
import MySQLdb, MySQLdb.cursors
import web, sys, site_helper

# local variables for brief statement
DB_PASSWORD = site_helper.config.DB_PASSWORD
DB_DATABASE = site_helper.config.DB_DATABASE
DB_HOST = site_helper.config.DB_HOST
DB_USER = site_helper.config.DB_USER
DB_CHARSET = site_helper.config.DB_CHARSET

class DBHelper:

    def __init__(self):
        self.db_dict  = self.__createDictDB()
        self.db_tuple = self.__createTupleDB()

    def __createDictDB(self):
        return MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASSWORD,charset=DB_CHARSET,db=DB_DATABASE,cursorclass=MySQLdb.cursors.DictCursor)
        
    def __createTupleDB(self):
        return MySQLdb.connect(host=DB_HOST,user=DB_USER,passwd=DB_PASSWORD,charset=DB_CHARSET,db=DB_DATABASE)

    def fetchOne(self,query_string,argv=()):
        '''return a dict'''
        assert('select' in query_string.lower())
        cursor = self.db_dict.cursor()
        try:
            cursor.execute(query_string,argv)
        except:
            sys.stderr.write('query string is: '+query_string+'\n')
            sys.stderr.write('argv are: '+str(argv)+'\n')
            raise
        one = cursor.fetchone()
        if one is not None:
            one = self._toUtf8(one)
            one = web.Storage(one)
        return one

    def fetchSome(self,query_string,argv=()):
        '''return a list of dict'''
        assert('select' in query_string.lower())
        cursor = self.db_dict.cursor()
        try:
            cursor.execute(query_string,argv)
        except:
            sys.stderr.write('query string is: '+query_string+'\n')
            sys.stderr.write('argv are: '+str(argv)+'\n')
            raise
        retList = []
        for one in cursor.fetchall():
            one = self._toUtf8(one)
            one = web.Storage(one)
            try:
                assert(one is not None)
            except:
                print "==============ERROR INFO=============="
                print 'query_string:', query_string
                print 'argv:', argv
                raise
            retList.append(one)
        return retList

    def fetchFirst(self,query_string,argv=()):
        '''return a int or string(etc.) of the colume's first value in query.'''
        assert('select' in query_string.lower())
        cursor = self.db_tuple.cursor()
        try:
            cursor.execute(query_string,argv)
        except:
            sys.stderr.write('query string is: '+query_string+'\n')
            sys.stderr.write('argv are: '+str(argv)+'\n')
            raise
        one = cursor.fetchone()
        if one is not None:
            one = one[0]
            if type(one) is unicode:
                one = one.encode('utf-8')
        return one

    def fetchSomeFirst(self,query_string,argv=()):
        '''like fetchFirst, but return a list. '''
        assert('select' in query_string.lower())
        cursor = self.db_tuple.cursor()
        try:
            cursor.execute(query_string,argv)
        except:
            sys.stderr.write('query string is: '+query_string+'\n')
            sys.stderr.write('argv are: '+str(argv)+'\n')
            raise
        retList = []
        for one in cursor.fetchall():
            first = one[0]
            if type(first) is unicode:
                first = first.encode('utf-8')
            retList.append(first)
        return retList

    def insert(self,query_string,argv=()):
        assert('insert' in query_string.lower() or 'replace' in query_string.lower())
        cursor = self.db_tuple.cursor()
        try:
            cursor.execute(query_string,argv)
        except:
            sys.stderr.write('query string is: '+query_string+'\n')
            sys.stderr.write('argv are: '+str(argv)+'\n')
            raise
        self.db_tuple.commit()
        return cursor.lastrowid

    def delete(self,query_string,argv=()):
        assert('delete' in query_string.lower())
        cursor = self.db_tuple.cursor()
        try:
            cursor.execute(query_string,argv)
        except:
            sys.stderr.write('query string is: '+query_string+'\n')
            sys.stderr.write('argv are: '+str(argv)+'\n')
            raise
        self.db_tuple.commit()

    def update(self,query_string,argv=()):
        assert('update' in query_string.lower())
        assert('where' in query_string.lower())
        cursor = self.db_tuple.cursor()
        try:
            cursor.execute(query_string,argv)
        except:
            sys.stderr.write('query string is: '+query_string+'\n')
            sys.stderr.write('argv are: '+str(argv)+'\n')
            raise
        self.db_tuple.commit()

    def _toUtf8(self,row):
        newRow = {}
        for k,v in row.items():
            if v is not None:
                if type(v) is unicode:
                    newRow[k] = v.encode('utf-8')
                else:
                    newRow[k] = v
            else:
                newRow[k] = None
        return newRow

    def _getColumnNames(self):
        cursor = self.db_tuple.cursor()
        query_string = 'desc %s' % self.model.table_name
        cursor.execute(query_string)
        retList = []
        for one in cursor.fetchall():
            first = one[0]
            if type(first) is unicode:
                first = first.encode('utf-8')
            retList.append(first)
        return retList

    def isTableExists(self, table_name):
        cursor = self.db_tuple.cursor()
        cursor.execute("SHOW TABLES LIKE '%s';" % table_name)
        one = cursor.fetchone()
        return one is not None

    def getTableColumns(self, table_name):
        '''return a list of names'''
        cursor = self.db_tuple.cursor()
        query_string = 'desc %s' % table_name
        cursor.execute(query_string)
        retList = []
        for one in cursor.fetchall():
            first = one[0]
            if type(first) is unicode:
                first = first.encode('utf-8')
            retList.append(first)
        return retList

    def executeQuery(self, query):
        self.db_tuple.cursor().execute(query)
        self.db_tuple.commit()

