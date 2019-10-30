class rest_api:
    import json
    import requests
    from os import sys

    def __init__(self, host, port, username, password):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.session = {}
        self.url = "https://{}:{}/dataservice/".format(self.host, self.port)

    def login(self):
        login_url = 'https://{}:{}/j_security_check'.format(self.host, self.port)
        login_data = {'j_username' : self.username, 'j_password' : self.password}
        self.requests.packages.urllib3.disable_warnings()
        self.session[self.host] = self.requests.session()

        #If the vmanage has a certificate signed by a trusted authority change verify to True
        login_response = self.session[self.host].post(url=login_url, data=login_data, verify=False)

        if b'<html>' in login_response.content:
            print ("Login to {}: Failed".format(self.host))
            sys.exit(0)
        else:
            print("Login to {}: Sucess -> Session Created".format(self.host))

    def get(self, mount_point):
        return self.session[self.host].get(self.url + mount_point, verify=False)

    def post(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        return self.session[self.host].post(self.url + mount_point, data=self.json.dumps(payload), headers=headers, verify=False)

    def put(self, mount_point, payload, headers={'Content-type': 'application/json', 'Accept': 'application/json'}):
        return self.session[self.host].put(self.url + mount_point, data=self.json.dumps(payload), headers=headers, verify=False)
