import sqlite3
import API.CoreData

def setStateforUser( userid, state, username="", password=""):
    connection = sqlite3.connect('API/BotDb.db')
    if (state == 0):
        API.CoreData.sessions[str(userid)] = {"state": state}
        connection.execute(
            '''INSERT INTO user_states(userid, state) VALUES (:n_userid, :n_state)''',
            {"n_state": state, "n_userid": str(userid)})
        connection.commit()
        return "Set state 0 for user"
    elif (state == 1):
        API.CoreData.sessions[str(userid)]["state"] = state
        API.CoreData.sessions[str(userid)]["username"] = username
        connection.execute(
            '''UPDATE user_states SET state = :n_state, username = :n_username WHERE userid = :n_userid''',
            {"n_state": state, "n_username": str(username), "n_userid": str(userid)}
        )
        connection.commit()
        return "set state 1 for user"

    elif (state == 2):
        API.CoreData.sessions[str(userid)]["state"] = state
        API.CoreData.sessions[str(userid)]["password"] = password
        connection.execute(
            '''UPDATE user_states SET state = :n_state, pass = :n_pass WHERE userid = :n_userid''',
            {"n_state": state, "n_pass": str(password), "n_userid": str(userid)}
        )
        connection.commit()
        return "set state 2 for user"


def setZState( userid):
    connection = sqlite3.connect('BotDb.db')
    API.CoreData.sessions[str(userid)]["state"] = 0
    connection.execute(
        '''UPDATE user_states SET state = :n_state WHERE userid = :n_userid''',
        {"n_userid": str(userid)}
    )
    connection.commit()
    return "updatet state 0 for user"


def getUserState( userid):
    connection = sqlite3.connect('BotDb.db')
    # if(API.CoreData.sessions.has_key(str(userid))):
    if (str(userid) in API.CoreData.sessions):
        return API.CoreData.sessions[str(userid)]["state"]
    else:
        cursor = connection.execute(
            '''SELECT state FROM user_states WHERE userid = :n_userid''',
            {"n_userid": str(userid)}
        )
        row = cursor.fetchone()
        if (row != None):
            return row[0]
        else:
            return -1


def getUserUsernamePass( userid):
    connection = sqlite3.connect('BotDb.db')
    if (str(userid) in API.CoreData.sessions):
        return [API.CoreData.sessions[str(userid)]["username"], API.CoreData]
    else:
        cursor = connection.execute(
            '''SELECT username, pass FROM user_states WHERE userid = :n_userid''',
            {"n_userid": userid}
        )
        row = cursor.fetchone()
        if (row != None):
            return row
        else:
            return -1


def removeFromUserSates( userid):
    connection = sqlite3.connect('BotDb.db')
    try:
        del (API.CoreData.sessions[str(userid)])
        connection.execute(
            '''DELETE FROM user_states WHERE userid = :n_userid''',
            {"n_userid": str(userid)}
        )
        return "user removed from the session"
    except:
        return "user does not exist in the session"


def insertUser( userid, token):
    connection = sqlite3.connect('BotDb.db')
    try:
        connection.execute(
            '''INSERT INTO users(userid, token) VALUES (:n_userid, :n_token)''',
            {"n_userid": str(userid), "n_token": str(token)}
        )
        connection.commit()
        return ("User added to users table")
    except:
        pass