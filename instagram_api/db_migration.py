import mysql.connector
from msyql.connector import errorcode

import settings as st

TABLES = {}

TABLES['user'] = (
        "CREATE TABLE 'user'("
        "    'id' int(4) NOT NULL AUTO_INCREMENT,"
        "    'user_id' int(4) NOT NULL,"
        "    'username' char(30) NOT NULL,"
        "    PRIMARY KEY ('user_id')"
        "    ) ENGINE=InnoBD")

TABLES['user_info'] = (
        "CREATE TABLE 'user_info'("
        "    'user_id' int(4) NOT NULL,"
        "    'follower' int(4) NOT NULL,"
        "    'following' int(4) NOT NULL,"
        "    'media_count' int(4) NOT NULL,"
        "    'counted_time' date NOT NULL,"
        "    PRIMARY KEY ('user_id') KEY ('user_id'),"
        "     REFERENCES 'user' ('user_id') ON DELETE CASCADE"
        "    ) ENGINE=InnoBD")

TABLES['post_info'] = (
        "CREATE TABLE 'pot_info'("
        "    'user_id' int(4) NOT NULL,"
        "    'post_id' int(4) NOT NULL,"
        "    'comments_count' int(4) NOT NULL,"
        "    'caption' varchar(max) NOT NULL,"
        "    'posted_time' date NOT NULL,"
        "    PRIMARY KEY ('user_id', 'post_id'),"
        "           KEY ('user_id'),"
        "    CONSTRAINT 'post_info_ibdk_1' FOREIGN KEY ('user_id'),"
        "     REFERENCES 'user' ('user_id') ON DELETE CASCADE"
        "    ) ENGINE=InnoBD")

TABLES['like_variation'] = (
        "CREATE TABLE 'like_variation'("
        "   'post_id NOT NULL,"
        "    'like_count' int(4) NOT NULL,"
        "    'counted_time' date NOT NULL,"
        "    PRIMARY KEY ('post_id'), KEY ('post_id'),"
        "    CONSTRAINT 'tags_ibfk_1' FOREIGN KEY ('post_id'),"
        "     REFERENCES 'post_info' ('post_id') ON DELETE CASCADE"
        "     ) ENGINE=InnoBD")

TABLES['tags'] = (
        "CREATE TABLE 'tags'("
        "    'post_id' NOT NULL,"
        "    'tag_1' varchar(600) DEFAULT NULL,"
        "    'tag_2' varchar(600) DEFAULT NULL,"
        "    'tag_3' varchar(600) DEFAULT NULL,"
        "    'tag_4' varchar(600) DEFAULT NULL,"
        "    'tag_5' varchar(600) DEFAULT NULL,"
        "    'tag_6' varchar(600) DEFAULT NULL,"
        "    'tag_7' varchar(600) DEFAULT NULL,"
        "    'tag_8' varchar(600) DEFAULT NULL,"
        "    'tag_9' varchar(600) DEFAULT NULL,"
        "    'tag_10' varchar(600) DEFAULT NULL,"
        "    'tag_11' varchar(600) DEFAULT NULL,"
        "    'tag_12' varchar(600) DEFAULT NULL,"
        "    'tag_13' varchar(600) DEFAULT NULL,"
        "    'tag_14' varchar(600) DEFAULT NULL,"
        "    'tag_15' varchar(600) DEFAULT NULL,"
        "    'tag_16' varchar(600) DEFAULT NULL,"
        "    'tag_17' varchar(600) DEFAULT NULL,"
        "    'tag_18' varchar(600) DEFAULT NULL,"
        "    'tag_19' varchar(600) DEFAULT NULL,"
        "    'tag_20' varchar(600) DEFAULT NULL,"
        "    'tag_21' varchar(600) DEFAULT NULL,"
        "    'tag_22' varchar(600) DEFAULT NULL,"
        "    'tag_23' varchar(600) DEFAULT NULL,"
        "    'tag_24' varchar(600) DEFAULT NULL,"
        "    'tag_25' varchar(600) DEFAULT NULL,"
        "    'tag_26' varchar(600) DEFAULT NULL,"
        "    'tag_27' varchar(600) DEFAULT NULL,"
        "    'tag_28' varchar(600) DEFAULT NULL,"
        "    'tag_29' varchar(600) DEFAULT NULL,"
        "    'tag_30' varchar(600) DEFAULT NULL,"
        "    PRIMARY KEY ('post_id'), KEY ('post_id'),"
        "    CONSTRAINT 'tags_ibfk_1' FOREIGN KEY ('post_id'),"
        "     REFERENCES 'post_info' ('post_id') ON DELETE CASCADE"
        "    ) ENGINE=InnoBD")


class DatabaseMigrate(object):

    def __init__(self):
        cnx = mysql.connector.connect(user=st.DB_USER,
                                      password=st.DB_PASS0,
                                      host='127.0.0.1',
                                      database=st.DB_NAME)

        self.cursor = cnx.cursor()

    def create_database(cursor=self.cursor):
        """
        """
        try:
            self.cursor.execute(
                f"CREATE DATABASE {st.DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print(f"Failed creating database: {err}")
            exit(1)

    try:
        self.cursor.execute(f"USE {st.DB_NAME}")
    except mysql.connector.Error as err:
        print(f"Database {st.DB_NAME} does not exists.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(self.cursor)
            print("Database {st.DB_NAME} created successfully.")
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    def create_tables(self):
        """
        """
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print(f"Creating table {table_name}: ", end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

        self.cursor.close()
        cnx.close()


