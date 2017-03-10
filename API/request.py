import requests
import API.Creator, API.CoreData

class RequestHandler():
    def __init__(self):
        self.messageCreator = API.Creator.MessageCreator()

    def getToken(self, data):
        return (requests.post('http://84.241.44.153:8585/api/v1/oauth/token', data = data).json()['access_token'])

    def getPackages(self, token):
        packages = requests.get('http://84.241.44.153:8585/api/v1/packages', headers = {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json'
        })
        return packages.json()

    def getFinalPackages(self, token):
        packages = self.getPackages(token)
        finalPackages = self.messageCreator.createPackageMessage(packages)
        return finalPackages

    def getTreaties(self, token):
        treaties = requests.get('http://84.241.44.153:8585/api/v1/treaties', headers = {
            'Authorization': 'Bearer ' + token,
            'Accept': 'application/json'
        })
        return treaties.json()

    def getFinalTreaties(self, token):
        treaties = self.getTreaties(token)
        finalTreaties = self.messageCreator.createTreatyMessage(treaties)
        return finalTreaties

    def signIn(self, username, password):
        log = requests.post('http://84.241.44.153:8585/api/v1/oauth/token', data= {
            'grant_type': 'password',
            'client_id': '1',
            'client_secret': 'Dr56kmtJWx2WzEgFbiHYJCZThno00dwqvkZrN7uV',
            'username': username,
            'password': password,
            'scope': ''
        })
        #print(username, password)
        if('error' in log.json()):
            return False
        else:
            return log.json()['access_token']

