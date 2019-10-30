from rest_api import rest_api
from os import environ, system, name
from sys import exit
from colorama import init, Back, Fore, Style
from pprint import pprint

def createAppAwareRoutePolicy(body):
    response = vmanage_session.post("template/policy/definition/approute", body)
    if response.status_code == 200:
        print("SUCESS. New definition ID: {}".format(response.json()["definitionId"]))
    else:
        print("FAIL, code id: {}".format(response.status_code))

def createTemplatePolicy(body):
    response = vmanage_session.post("template/policy/vsmart", body)
    if response.status_code == 200:
        print("SUCESS. HTTP code id {}".format(response.status_code))
    else:
        print("FAIL, code id: {}".format(response.status_code))

def activatePolicy(policyId):
    body = {"isEdited": False}
    response = vmanage_session.post("template/policy/vsmart/activate/{}".format(policyId), body)
    if response.status_code == 200:
        print("SUCESS. Policy {} ACTIVE.".format(policyId))
        print("Job Id: {}".format(response.json()['id']))
    else:
        print("FAIL, code id: {}".format(response.status_code))

def deactivatePolicy(policyId):
    body = {}
    response = vmanage_session.post("template/policy/vsmart/deactivate/{}".format(policyId), body)
    if response.status_code == 200:
        print("SUCESS. Policy {} NOT ACTIVE.".format(policyId))
        print("Job Id: {}".format(response.json()['id']))
    else:
        print("FAIL, code id: {}".format(response.status_code))

def getPolicyId(policyName):
    response = vmanage_session.get("template/policy/vsmart")
    for policy in response.json()['data']:
        if policy['policyName'] == policyName:
            return policy['policyId']
    return None

def clearScreen():
    system('cls' if name == 'nt' else 'clear')

# Creating vMANAGE session
# Reading env variables. In order to do this you will need to add this lines to .bash_profile:
# export VMANAGE_HOST="198.18.1.10"
# export VMANAGE_PORT="443"
# export VMANAGE_USERNAME="admin"
# export VMANAGE_PWD="admin"
# Another option is to pass the login variables as parameter when you call the Program.
# Another option is to use input and ask the user for variables.
vmanage_host = environ.get("VMANAGE_HOST")
vmanage_port = environ.get("VMANAGE_PORT")
vmanage_username = environ.get("VMANAGE_USERNAME")
vmanage_password = environ.get("VMANAGE_PWD")
vmanage_session = rest_api(vmanage_host, vmanage_port, vmanage_username, vmanage_password)
vmanage_session.login()

#Console Program
while True:
    init(autoreset=True)
    #Console Menu
    clearScreen()
    print(Back.MAGENTA + 'Please choose a valid option:')
    print('1- Create Aplication Aware Routing Policy (DC1 --> BR3). POST.')
    print('2- Create Template Policy. POST.')
    print('3- Activate Policy. POST.')
    print('4- Deactivate Policy. POST')
    print('Press any key to exit.')
    print('')
    userInput = input("YOUR OPTION?: ")

    if userInput == '1':
        clearScreen()
        policyName = input('ENTER POLICY NAME: ')
        policyDescription = input('ENTER POLICY DESCRIPTION: ')
        jsonBody = {
            "name": policyName,
            "type": "appRoute",
            "description": policyDescription,
            "sequences": [
                {
                "sequenceId": 1,
                "sequenceName": "App Route",
                "sequenceType": "appRoute",
                "sequenceIpType": "ipv4",
                "match": {
                    "entries": [
                        {
                        "field": "destinationDataPrefixList",
                        "ref": "81387e80-c3b2-41d7-9804-9a58a375021c"
                        }
                    ]
                },
                "actions": [
                    {
                    "type": "backupSlaPreferredColor",
                    "parameter": "mpls"
                    }
                ]
                }
            ]
        }
        createAppAwareRoutePolicy(jsonBody)
        input("Enter any key to continue.")
    elif userInput == '2':
        clearScreen()
        policyName = input('ENTER POLICY NAME: ')
        policyDescription = input('ENTER POLICY DESCRIPTION: ')
        definitionId = input('ENTER DEFINITION ID: ')
        jsonBody = {
            "policyDescription": policyDescription,
            "policyType": "feature",
            "policyName": policyName,
            "policyDefinition":
            {
                "assembly":
                        [{
                        "definitionId": definitionId,
                        "type": "appRoute",
                        "entries":  [{
                                    "siteLists": ["cf4bbb13-0a3f-4302-adfa-6cfce6b3950c"],
                                    "vpnLists": ["67c9a7e1-e1b2-4a31-bd7c-7d0bbf9b7bbb"]
                                    }]
                        }]
            },
            "isPolicyActivated": False
        }
        createTemplatePolicy(jsonBody)
        input("Enter any key to continue.")
    elif userInput == '3':
        clearScreen()
        policyName = input("ENTER POLICY NAME: ")
        policyId = getPolicyId(policyName)
        if policyId == None:
            print('ERROR, no policy with that name.')
            input("Enter any key to continue.")
            continue
        else:
            activatePolicy(policyId)
            input("Enter any key to continue.")
    elif userInput == '4':
        clearScreen()
        policyName = input("ENTER POLICY NAME: ")
        policyId = getPolicyId(policyName)
        if policyId == None:
            print('ERROR, no policy with that name.')
            continue
        else:
            deactivatePolicy(policyId)
        input("Enter any key to continue.")
    else:
        exit()
