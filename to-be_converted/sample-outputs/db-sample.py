def update_db():
    try:
        connection = psycopg2.connect(user = "username",
                                        password = "pw",
                                        host = "localhost",
                                        port = "port",
                                        database = "databasename")
        cursor = connection.cursor()
        # Update affected tables
        cursor.execute("Update <table> set <column>='value' where <column>='value';")
        cursor.execute("Update <table> set <column>='value' where <column>='value';")
        cursor.execute("Update <table> set <column>='value' where <column>='value';")
        connection.commit()

    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
    return None
	

def check_db():
    try:
        connection = psycopg2.connect(user = "username",
                                        password = "pw",
                                        host = "localhost",
                                        port = "port",
                                        database = "databasename")
        cursor = connection.cursor()
        # Update affected tables
		cursor.execute("select <column>, <column2> from <table> where <column>='<value>';")
        value = cursor.fetchall()
		# Probably further handling on thevalue needed
		
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
    return None
