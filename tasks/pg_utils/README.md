[![Known Vulnerabilities](https://snyk.io/test/github/nasa/cumulus-orca/badge.svg?targetFile=tasks/pg_utils/requirements.txt)](https://snyk.io/test/github/nasa/cumulus-orca?targetFile=tasks/pg_utils/requirements.txt)

Visit the [Developer Guide](https://nasa.github.io/cumulus-orca/docs/developer/development-guide/code/contrib-code-intro) for information on environment setup and testing.

**Shared code to access a postgres database**

- [Deployment](#deployment)
- [pydoc database](#pydoc-database)

<a name="development"></a>
# Development

## Deployment
```
https://www.oreilly.com/library/view/head-first-python/9781491919521/ch04.html
Create the distribution file:
    (podr) λ cd C:\devpy\poswotdr\tasks\pg_utils
    (podr) λ python setup.py sdist
    (podr) λ cd dist
    (podr) λ pip install pg_utils-1.0.tar.gz
 
```
<a name="pydoc-database"></a>
## pydoc database
```
HNAME
    database

DESCRIPTION
    This module exists to keep all database specific code in a single place. The
    cursor and connection objects can be imported and used directly, but for most
    queries, simply using the "query()" function will likely suffice.

CLASSES
    builtins.Exception(builtins.BaseException)
        DbError
            ResourceExists
    
    class DbError(builtins.Exception)
     |  Exception to be raised if there is a database error.
     |  
     |  Method resolution order:
     |      DbError
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |  
     |  Data descriptors defined here:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.Exception:
     |  
     |  __init__(self, /, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.Exception:
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |  
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __reduce__(...)
     |      Helper for pickle.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |  
     |  __setstate__(...)
     |  
     |  __str__(self, /)
     |      Return str(self).
     |  
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |  
     |  __cause__
     |      exception cause
     |  
     |  __context__
     |      exception context
     |  
     |  __dict__
     |  
     |  __suppress_context__
     |  
     |  __traceback__
     |  
     |  args
    
    class ResourceExists(DbError)
     |  Exception to be raised if there is an existing database resource.
     |  
     |  Method resolution order:
     |      ResourceExists
     |      DbError
     |      builtins.Exception
     |      builtins.BaseException
     |      builtins.object
     |  
     |  Data descriptors inherited from DbError:
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.Exception:
     |  
     |  __init__(self, /, *args, **kwargs)
     |      Initialize self.  See help(type(self)) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Static methods inherited from builtins.Exception:
     |  
     |  __new__(*args, **kwargs) from builtins.type
     |      Create and return a new object.  See help(type) for accurate signature.
     |  
     |  ----------------------------------------------------------------------
     |  Methods inherited from builtins.BaseException:
     |  
     |  __delattr__(self, name, /)
     |      Implement delattr(self, name).
     |  
     |  __getattribute__(self, name, /)
     |      Return getattr(self, name).
     |  
     |  __reduce__(...)
     |      Helper for pickle.
     |  
     |  __repr__(self, /)
     |      Return repr(self).
     |  
     |  __setattr__(self, name, value, /)
     |      Implement setattr(self, name, value).
     |  
     |  __setstate__(...)
     |  
     |  __str__(self, /)
     |      Return str(self).
     |  
     |  with_traceback(...)
     |      Exception.with_traceback(tb) --
     |      set self.__traceback__ to tb and return self.
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors inherited from builtins.BaseException:
     |  
     |  __cause__
     |      exception cause
     |  
     |  __context__
     |      exception context
     |  
     |  __dict__
     |  
     |  __suppress_context__
     |  
     |  __traceback__
     |  
     |  args

FUNCTIONS
    get_connection(dbconnect_info: Dict[str, Union[str, int]]) -> psycopg2.extensions.connection
        Retrieves a connection from the connection pool and yields it.
        
        Args:
            dbconnect_info: A dictionary with the following keys:
                db_port (str): The database port. Default is 5432.
                db_host (str): The database host.
                db_name (str): The database name.
                db_user (str): The username to connect to the database with.
                db_pw (str): The password to connect to the database with.
    
    get_cursor(dbconnect_info: Dict[str, Union[str, int]]) -> psycopg2.extensions.cursor
        Retrieves the cursor from the connection and yields it. Automatically
        commits the transaction if no exception occurred.
        
        Args:
            dbconnect_info: A dictionary with the following keys:
                db_port (str): The database port. Default is 5432.
                db_host (str): The database host.
                db_name (str): The database name.
                db_user (str): The username to connect to the database with.
                db_pw (str): The password to connect to the database with.
    
    get_db_connect_info(env_or_secretsmanager: str, param_name: str) -> str
    
    get_utc_now_iso() -> str
        Takes the current utc timestamp and returns it an isoformat string.
        
        Returns:
            An isoformat string.
            ex. '2019-07-17T17:36:38.494918'
    
    multi_query(sql_stmt: str, params, db_cursor: psycopg2.extensions.cursor) -> List
        This function will use the provided cursor to run the query instead of
        retrieving one itself. This is intended to be used when the caller wants
        to make a query that doesn't automatically commit and close the cursor.
        Like single_query(), this will return the rows as a list.
        
        This function should be used within a context made by get_cursor().
        
        Args:
            sql_stmt: The SQL statement to execute against the database.
            params: The parameters for the {sql_stmt}.
            db_cursor: The cursor to the database to run the command against.
    
    query_from_file(db_cursor: psycopg2.extensions.cursor, sql_file) -> str
        This function will execute the sql in the given file.
        
        Args:
            db_cursor: The cursor to the target database.
            sql_file: The path to the file containing the SQL statement to execute against the database.
        
        Raises:
            ResourceExists: Error message from DB claims that the resource already exists.
            DbError: Something went wrong while executing the statement.
        
        Returns:
            A string indicating that the statement has been executed.
    
    query_no_params(db_cursor: psycopg2.extensions.cursor, sql_stmt) -> str
    
    read_db_connect_info(param_source: Dict) -> Dict[str, Union[str, int]]
        This function will retrieve database connection parameters from
        the parameter store and/or env vars.
        
            Args:
                param_source (dict): A dict containing
                    "db_host": {env_or_secretsmanager, param_name},
                    "db_port": {env_or_secretsmanager, param_name},
                    "db_name": {env_or_secretsmanager, param_name},
                    "db_user": {env_or_secretsmanager, param_name},
                    "db_pw": {env_or_secretsmanager, param_name}
                    where the value of env_or_secretsmanager is: "env" to read env var,
                                                      "secretsmanager" to read parameter store
        
        
            Returns:
                dbconnect_info: A dict containing
                    "db_host": value,
                    "db_port": value,
                    "db_name": value,
                    "db_user": value,
                    "db_pw": value
    
    return_connection(dbconnect_info) -> psycopg2.extensions.connection
        Retrieves a connection from the connection pool.
    
    return_cursor(conn: psycopg2.extensions.connection) -> psycopg2.extensions.cursor
    
    single_query(sql_stmt: str, dbconnect_info: Dict[str, Union[str, int]], params=None) -> List
        # todo: Rework query function naming to clearly define which give results and which do not.
        # todo: Look at reducing duplicated code.
    
    uuid_generator() -> str
        Generates a unique UUID.
        
        Returns:
            A string representing a UUID.
            ex. '0000a0a0-a000-00a0-00a0-0000a0000000'

DATA
    Dict = typing.Dict
    LOGGER = <Logger database (WARNING)>
    List = typing.List
    Union = typing.Union
```
