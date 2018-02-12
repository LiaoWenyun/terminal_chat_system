import psycopg2
from User import User
from DBHandler import *


class DBHandlerImpl(DBHandler):
    def __init__(self):
        try:
            self.con = self.get_connection()

        except IOError as err:
            raise DBException

    def get_connection(self):
        return psycopg2.connect(
            database="dbv6rg1957d22o",
            user="seafjzirwmfqen",
            password="3ce155ae9f16047147026e121207bb84c1946902b303509c54fe723ac5e9fafa",
            host="ec2-54-225-199-107.compute-1.amazonaws.com",
            port=5432
        )

    def close(self):
        self.con.close()

    """insert user name and password into db, return id"""

    def insert(self, username, password):

        this_user = self.findByName(username)
        if this_user != None:
            raise DuplicateNameException
        else:
            cur = self.con.cursor()
            cmd_1 = "INSERT INTO log_in(username, password) VALUES(%s,%s);"
            cmd_2 = "SELECT ID FROM log_in WHERE username =%s and password=%s;"
            self.cur.execute(cmd_1, (username, password))
            self.cur.execute(cmd_2, (username, password))
            a = self.cur.fetchone()
            user_id = int(a[0])
            self.con.commit()

            return user_id

    """take id as input, return an instance of User"""

    def findByID(self, user_id):

        self.cur = self.con.cursor()
        cmd = "SELECT username, password FROM log_in WHERE id=%s;"
        self.cur.execute(cmd, ([user_id]))
        properties = self.cur.fetchone()
        if properties is None:
            return None
        else:
            the_user = User(properties[0], user_id, properties[1])
            return the_user

    """take username as input, return an instance of User"""

    def findByName(self, username):

        self.cur = self.con.cursor()
        cmd = "SELECT id, password FROM log_in WHERE username=%s;"
        self.cur.execute(cmd, [username])
        properties = self.cur.fetchone()
        if properties is None:
            return None
        else:
            the_user = User(username, properties[0], properties[1])
            return the_user

    """ take id, new_username, new_password as input, no return """

    def updateUser(self, user_id, new_username, new_password):
        self.cur = self.con.cursor()
        this_user1 = self.findByName(new_username)
        this_user2 = self.findByID(user_id)
        if this_user1:
            raise DuplicateNameException
        elif this_user2 is None:
            raise IDNotExistException
        else:
            cmd = "UPDATE log_in SET username=%s, password=%s WHERE id=%s;"
            self.cur.execute(cmd, (new_username, new_password, user_id))
            self.con.commit()


