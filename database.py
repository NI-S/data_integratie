"""Noah Scheffer

This is a database class.
It creates the connection with the database.
With this class queries can be executed and results can be fetched.
The class is also used to close the database connection.
Last time updated: 09-06-2021
"""
import psycopg2     # Used to the create connection with the postgresql database


class Database_connection:
    """This class is used to create the connection with the database.
    It can be used to execute queries and retrieve the results.
    """
    def __init__(self):
        self.conn = None


    def postgre_connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(host='145.74.104.145', port='5432', database='postgres', user='j3_g4', password='Blaat1234')
            self.conn.autocommit = True     # Used to automatically commit to the database

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def postgre_excute_query(self, sql):
        """Execute the query that is given.
        It prints worked, if the execution was succesful.
        :param sql:the query to be executed.
        :return:Nothing. But execute the query.
        """
        # create a cursor
        self.cur = self.conn.cursor()
        try:
            # execute a statement
            self.cur.execute(sql)
            print("worked")
        except:
            print("Could not execute the statement")


    def postgre_fetch_results(self):
        """Fetch the results.
        :return:Nothing.
        """
        # display the PostgreSQL database server version
        try:
            output = self.cur.fetchall()
            for row in output:
                print(row)
        except:
            print("No results found")

        # close the communication with the PostgreSQL
        self.cur.close()


    def postgre_discconnect(self):
        """Close the connection.
        :return:Nothing
        """
        self.conn.close()
        print('Database connection closed.')






