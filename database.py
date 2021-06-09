import psycopg2


class Database_connection:

    def __init__(self):
        self.conn = None

    def postgre_connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.conn = psycopg2.connect(host='145.74.104.145', port='5432', database='postgres', user='j3_g4', password='Blaat1234')
            self.conn.autocommit = True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def postgre_excute_query(self, sql):
        # create a cursor
        self.cur = self.conn.cursor()
        # execute a statement
        self.cur.execute(sql)
        print("worked")

    def postgre_fetch_results(self):
        # display the PostgreSQL database server version
        output = self.cur.fetchall()
        for row in output:
            print(row)

        # close the communication with the PostgreSQL
        self.cur.close()

    def postgre_discconnect(self):
        self.conn.close()
        print('Database connection closed.')






