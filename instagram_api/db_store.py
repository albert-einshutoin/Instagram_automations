import mysql.connector
from mysql.connector import errorcode

import settings as st

TABLES = {}

TABLES['user'] = (
        "CREATE TABLE `user` (\
                `id` bigint UNSIGNED NOT NULL,\
                `username` char(30) NOT NULL,\
                PRIMARY KEY (`id`)\
                )")

TABLES['user_info'] = (
        "CREATE TABLE `user_info` (\
                `user_id` bigint UNSIGNED NOT NULL,\
                `follower` int(11) UNSIGNED NOT NULL,\
                `following` int(11) UNSIGNED NOT NULL,\
                `media_count` int(11) UNSIGNED NOT NULL,\
                `counted_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,\
                PRIMARY KEY (`user_id`),\
                KEY (`user_id`),\
                CONSTRAINT `user_info_ibfk_1` FOREIGN KEY (`user_id`)\
                REFERENCES `user`(`id`) ON DELETE CASCADE\
                )")

TABLES['post_info'] = (
        "CREATE TABLE `post_info` (\
                `post_id` bigint UNSIGNED NOT NULL,\
                `user_id` bigint UNSIGNED NOT NULL,\
                `comments_count` int(11) UNSIGNED NOT NULL,\
                `caption` TEXT NOT NULL,\
                `posted_time` datetime NOT NULL,\
                PRIMARY KEY (`post_id`, `user_id`),\
                KEY (`user_id`),\
                CONSTRAINT `post_info_ibfk_1` FOREIGN KEY (`user_id`)\
                REFERENCES `user`(`id`) ON DELETE CASCADE\
                ) ")

TABLES['like_variation'] = (
        "CREATE TABLE `like_variation` (\
                `post_id` bigint UNSIGNED NOT NULL,\
                `like_count` int(4) UNSIGNED NOT NULL,\
                `counted_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,\
                PRIMARY KEY (`post_id`),\
                KEY (`post_id`),\
                CONSTRAINT `like_variation_ibfk_1` FOREIGN KEY (`post_id`)\
                REFERENCES `post_info` (`post_id`) ON DELETE CASCADE\
                ) ")

TABLES['tags'] = (
        "CREATE TABLE `tags` (\
                `post_id` bigint UNSIGNED NOT NULL,\
                `tag_1` TEXT DEFAULT NULL,\
                `tag_2` TEXT DEFAULT NULL,\
                `tag_3` TEXT DEFAULT NULL,\
                `tag_4` TEXT DEFAULT NULL,\
                `tag_5` TEXT DEFAULT NULL,\
                `tag_6` TEXT DEFAULT NULL,\
                `tag_7` TEXT DEFAULT NULL,\
                `tag_8` TEXT DEFAULT NULL,\
                `tag_9` TEXT DEFAULT NULL,\
                `tag_10` TEXT DEFAULT NULL,\
                `tag_11` TEXT DEFAULT NULL,\
                `tag_12` TEXT DEFAULT NULL,\
                `tag_13` TEXT DEFAULT NULL,\
                `tag_14` TEXT DEFAULT NULL,\
                `tag_15` TEXT DEFAULT NULL,\
                `tag_16` TEXT DEFAULT NULL,\
                `tag_17` TEXT DEFAULT NULL,\
                `tag_18` TEXT DEFAULT NULL,\
                `tag_19` TEXT DEFAULT NULL,\
                `tag_20` TEXT DEFAULT NULL,\
                `tag_21` TEXT DEFAULT NULL,\
                `tag_22` TEXT DEFAULT NULL,\
                `tag_23` TEXT DEFAULT NULL,\
                `tag_24` TEXT DEFAULT NULL,\
                `tag_25` TEXT DEFAULT NULL,\
                `tag_26` TEXT DEFAULT NULL,\
                `tag_27` TEXT DEFAULT NULL,\
                `tag_28` TEXT DEFAULT NULL,\
                `tag_29` TEXT DEFAULT NULL,\
                `tag_30` TEXT DEFAULT NULL,\
                PRIMARY KEY (`post_id`),\
                KEY (`post_id`),\
                CONSTRAINT `tags_ibfk_1` FOREIGN KEY (`post_id`)\
                REFERENCES `post_info` (`post_id`) ON DELETE CASCADE\
                ) ")


class DatabaseMigrate(object):

    def __init__(self):
        self.cnx = mysql.connector.connect(user=st.DB_USER,
                                           password=st.DB_PASS,
                                           host='127.0.0.1')

        self.cursor = self.cnx.cursor()

    def create_database(self):
        """
        """
        try:
            self.cursor.execute(
                f"CREATE DATABASE {st.DB_NAME} DEFAULT CHARACTER SET 'utf8mb4'")
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
        self.cnx.close()


migrate = DatabaseMigrate()
migrate.create_database()
migrate.create_tables()

