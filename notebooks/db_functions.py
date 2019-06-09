from config import USERNAME, PASSWORD, HOST_IP, HOST_PORT, DB_NAME
import psycopg2

# function to test connection to Postgres DB in Docker
def test_dbconnect():
    try:
        # connect to database with defined parameters
        connection = psycopg2.connect(
                                    user = USERNAME,
                                    password = PASSWORD,
                                    host = HOST_IP,
                                    port = HOST_PORT,
                                    database = DB_NAME)

        # create a cursor to execute commands in the connection
        curs = connection.cursor()

        # Print PostgreSQL Connection properties
        print (connection.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        curs.execute("SELECT version();")
        record = curs.fetchone()
        print("You are connected to - ", record,"\n")

    except (Exception, psycopg2.Error) as error :
        # print error
        print ("Error while connecting to PostgreSQL", error)

    finally:
            #closing database connection.
            if(connection):
                curs.close()
                connection.close()
                print("PostgreSQL connection is closed")

# function to create tables in db
def edit_db(query):
    try:
        # connect to database with defined parameters
        connection = psycopg2.connect(
                                    user = USERNAME,
                                    password = PASSWORD,
                                    host = HOST_IP,
                                    port = HOST_PORT,
                                    database = DB_NAME)
        
        # create a cursor to execute commands in the connection
        curs = connection.cursor()

        # execute query
        curs.execute(query)

        # commit transaction to database
        connection.commit()

        # print confirmation of success
        print("Successful edit in PostgreSQL.")

    except (Exception, psycopg2.DatabaseError) as error:
        # print error
        print("Error while editing PostgreSQL database:", error)
    
    finally:
            # close database connection
            if (connection):
                curs.close()
                connection.close()
                print("PostgreSQL connection is closed.")

# function for search queries in Postgres
def search_db(query):
    try:
        # connect to database with defined parameters
        connection = psycopg2.connect(
                                    user = USERNAME,
                                    password = PASSWORD,
                                    host = HOST_IP,
                                    port = HOST_PORT,
                                    database = DB_NAME)

        # create a cursor to execute commands in the connection
        curs = connection.cursor()

        # print results of search query
        curs.execute(query)

        record = curs.fetchone()
        print(record,"\n")

    except (Exception, psycopg2.Error) as error :
        # print error
        print ("Error while connecting to PostgreSQL", error)

    finally:
            #closing database connection.
            if(connection):
                curs.close()
                connection.close()
                print("PostgreSQL connection is closed")


if __name__ == "__main__":

    # test connection to
    print(test_dbconnect())