import sqlite3
import API.CoreData

class DataHandler():

    def __init__(self):
        self.connection = sqlite3.connect("API/BotDb.db", check_same_thread=False)

    def setStateforUser(self, userid, state, username = "", password = ""):
        if(state == 0):
            API.CoreData.sessions[str(userid)] = {"state" : state}
            self.connection.execute(
                '''INSERT INTO user_states(userid, state) VALUES (:n_userid, :n_state)''',
                {"n_state" : state, "n_userid" : str(userid)})
            self.connection.commit()
            return "Set state 0 for user"
        elif(state == 1):
            if(not str(userid) in API.CoreData.sessions):
                API.CoreData.sessions[str(userid)] = {"state" : 1, "username" : username}
            else:
                API.CoreData.sessions[str(userid)]["state"] = state
                API.CoreData.sessions[str(userid)]["username"] = username
            self.connection.execute(
                '''UPDATE user_states SET state = :n_state, username = :n_username WHERE userid = :n_userid''',
                {"n_state" : state, "n_username" : str(username), "n_userid" : str(userid)}
            )
            self.connection.commit()
            return "set state 1 for user"

        elif(state == 2):
            if(not str(userid) in API.CoreData.sessions):
                cursor = self.connection.execute(
                    '''SELECT username FROM user_states WHERE userid = :n_userid''',
                    {"n_userid" : str(userid)}
                )
                row = cursor.fetchone()
                API.CoreData.sessions[str(userid)] = {"state" : 2, "password" : password, "username" : row[0]}
            else:
                API.CoreData.sessions[str(userid)]["state"] = state
                API.CoreData.sessions[str(userid)]["password"] = password
            self.connection.execute(
                '''UPDATE user_states SET state = :n_state, pass = :n_pass WHERE userid = :n_userid''',
                {"n_state" : state, "n_pass" : str(password), "n_userid" : str(userid)}
            )
            self.connection.commit()
            return "set state 2 for user"

    def setZState(self, userid):
        if(str(userid) in API.CoreData.sessions):
            API.CoreData.sessions[str(userid)]["state"] = 0
        else:
            API.CoreData.sessions[str(userid)] = {"state" : 0}
        self.connection.execute(
            '''UPDATE user_states SET state = 0 WHERE userid = :n_userid''',
            {"n_userid" : str(userid)}
        )
        self.connection.commit()
        return "updatet state 0 for user"


    def getUserState(self, userid):
        #if(API.CoreData.sessions.has_key(str(userid))):
        if(str(userid) in API.CoreData.sessions):
            return API.CoreData.sessions[str(userid)]["state"]
        else:
            cursor = self.connection.execute(
                '''SELECT state FROM user_states WHERE userid = :n_userid''',
                {"n_userid" : str(userid)}
            )
            row = cursor.fetchone()
            if(row != None):
                return row[0]
            else:
                return -1

    def getUserUsernamePass(self, userid):
        if(str(userid) in API.CoreData.sessions):
            #print ([API.CoreData.sessions[str(userid)]["username"], API.CoreData.sessions[str(userid)]["password"]])
            return [API.CoreData.sessions[str(userid)]["username"], API.CoreData.sessions[str(userid)]["password"]]
        else:
            cursor = self.connection.execute(
                '''SELECT username,pass FROM user_states WHERE userid = :n_userid''',
                {"n_userid" : userid}
            )
            row = cursor.fetchone()
            if(row != None):
                return [row[0], row[1]]
            else:
                return -1

    def removeFromUserSates(self, userid):
        try:
            #del(API.CoreData.sessions[str(userid)])
            if(str(userid) in API.CoreData.sessions):
                del(API.CoreData.sessions[str(userid)])
            self.connection.execute(
                '''DELETE  FROM user_states WHERE userid = :n_userid''',
                {"n_userid" : str(userid)}
            )
            self.connection.commit()
            return "user removed from the session"
        except:
            return "user does not exist in the session"


    def insertUser(self, userid, token):
        try:
            API.CoreData.mainSessions[str(userid)] = str(token)
            self.connection.execute(
                '''INSERT INTO users(userid, token) VALUES (:n_userid, :n_token)''',
                {"n_userid" : str(userid), "n_token" : str(token)}
            )
            self.connection.commit()
            return ("User added to users table")
        except:
            pass

    def removeFromUsers(self, userid):
        try:
            if(str(userid) in API.CoreData.mainSessions):
                del(API.CoreData.mainSessions[str(userid)])
            self.connection.execute(
                '''DELETE FROM users WHERE userid = :n_userid''',
                {"n_userid" : str(userid)}
            )
            self.connection.commit()
            return "User Removed from the main Session and Table"
        except:
            return "Could Not remove user from main session and Table"

    def getToken(self, userid):
        if(str(userid) in API.CoreData.mainSessions):
            return API.CoreData.mainSessions[str(userid)]
        else:
            cursor = self.connection.execute(
                '''SELECT token FROM users WHERE userid = :n_userid''',
                {"n_userid" : str(userid)}
            )
            row = cursor.fetchone()
            if(row != None):
                API.CoreData.mainSessions["userid"] = row[0]
                return row[0]
            else:
                return -1

