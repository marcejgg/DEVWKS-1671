from rest_api import rest_api
from os import environ, system, name
from sys import exit
from colorama import init, Back, Fore, Style

def consultaTemplateAsociado(ip):
    response = vmanage_session.get("system/device/vedges?deviceIP={}&".format(deviceIp))
    #if response OK -- Code status 200
    if response.status_code == 200:
        templateId = response.json()['data'][0]['templateId']
        print("SUCESS, HTTP code id: {}".format(response.status_code))
        print("Template ID: {}".format(templateId))
    #Else -- any other http code
    else:
        print("FAIL, code id: {}".format(response.status_code))

def consultaBannerTemplate(templateId):
    response = vmanage_session.get("template/device/object/{}".format(templateId))
    if response.status_code == 200:
        for dct in response.json()['generalTemplates']:
            if dct['templateType'] == 'banner':
                bannerTemplateId = dct['templateId']
                print("Banner ID: {} ---> Template ID: {}".format(bannerTemplateId, templateId))
    else:
        print("FAIL, code id: {}".format(response.status_code))

def creaBannerTemplate(body):
    response = vmanage_session.post("template/feature/", body)
    if response.status_code == 200:
        newBannerId = response.json()["templateId"]
        print("SUCESS. New banner ID: {}".format(newBannerId))
    else:
        print("FAIL, code id: {}".format(response.status_code))

def asociaBannerTemplate(templateId, body):
    response = vmanage_session.put("template/device/{}".format(templateId), body)
    if response.status_code == 200:
        print("SUCESS. HTTP code id {}".format(response.status_code))
    else:
        print("FAIL, code id: {}".format(response.status_code))

def reaplicaTemplate(body):
    response = vmanage_session.post("template/device/config/attachfeature", body)
    if response.status_code == 200:
        jobId = response.json()["id"]
        print("SUCESS. HTTP code id: {}".format(response.status_code))
        print("FYI, the job id associated with this task is: {}".format(jobId))
    else:
        print("FAIL, code id: {}".format(response.status_code))
    return response.status_code

def consultaTemplate(templateId):
    response = vmanage_session.get("template/device/object/{}".format(templateId)).json()
    return response

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
    print('1- Get the configuration template associated to a device IP Address. GET.')
    print('2- Get the banner template associated to a configuration template. GET.')
    print('3- Create a banner template. POST.')
    print('4- Associate a banner template to a configuration template. PUT.')
    print('5- Apply configuration template. POST.')
    print('Press any key to exit.')
    print('')
    userInput = input("YOUR OPTION?: ")

    if userInput == '1':
        clearScreen()
        deviceIp = input('ENTER THE IP ADDRESS: ')
        consultaTemplateAsociado(deviceIp)
        input("Enter any key to continue.")
    elif userInput == '2':
        clearScreen()
        configTemplateId = input('ENTER CONFIGURATION TEMPLATE ID: ')
        consultaBannerTemplate(configTemplateId)
        input("Enter any key to continue.")
    elif userInput == '3':
        clearScreen()
        templateName = input('ENTER THE BANNER TEMPLATE NAME: ')
        loginBanner = input('ENTER LOGIN BANNER: ')
        motdBanner = input('ENTER MOTD: ')
        bannerJsonPayload = {
            "templateName": templateName,
            "templateDescription": templateName,
            "templateType": "banner",
            "templateMinVersion": "15.0.0",
            "templateDefinition": {
                "login": {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": loginBanner,
                    "vipVariableName": "banner_login"
                },
                "motd": {
                    "vipObjectType": "object",
                    "vipType": "constant",
                    "vipValue": motdBanner,
                    "vipVariableName": "banner_motd"
                }
            },
            "transitionInProgress": True,
            "viewMode": "add",
            "deviceType": [
                "vedge-CSR-1000v"
            ],
            "deviceModels": [
                {
                    "name": "vedge-CSR-1000v",
                    "displayName": "CSR1000v",
                    "deviceType": "vedge",
                    "isCliSupported": False,
                    "isCiscoDeviceModel": True
                }
            ],
            "templateUrl": "/app/configuration/template/feature/templates/banner-15.0.0.html",
            "factoryDefault": False
        }
        creaBannerTemplate(bannerJsonPayload)
        input("Enter any key to continue.")
    elif userInput == '4':
        clearScreen()
        bannerTemplateId = input('ENTER BANNER TEMPLATE ID: ')
        configTemplateId = input('ENTER CONFIGURATION TEMPLATE ID: ')
        confirmation = input("You are about to associate: BANNER TEMPLATE ID {} ---> CONFIGURATION TEMPLATE ID: {}\r\nIs this OK? (y/n)".format(bannerTemplateId, configTemplateId))
        if confirmation == 'y':
            #Get the body for the next POST
            consulta = consultaTemplate(configTemplateId)
            for dct in consulta['generalTemplates']:
                if dct['templateType'] == 'banner':
                    dct['templateId'] = bannerTemplateId
            asociaBannerTemplate(configTemplateId, consulta)
            input("Enter any key to continue.")
        else:
            pass
    elif userInput == '5':
        clearScreen()
        #You can configure the body getting the parameters from a file or db... here is fixed with the exception of TemplateId.
        configTemplateId = input('ENTER CONFIGURATION TEMPLATE ID: ')
        attachFeatureJson = {
            "deviceTemplateList": [
                {
                    "templateId": configTemplateId,
                    "device": [
                        {
                            "csv-status": "complete",
                            "csv-deviceId": "CSR-3299b46e-90cd-4c5b-bebb-b6babfd8e0b1",
                            "csv-deviceIP": "10.5.0.1",
                            "csv-host-name": "BR3-CEDGE1",
                            "/40/VPN40_INTERFACE/interface/if-name": "GigabitEthernet7",
                            "/40/VPN40_INTERFACE/interface/ip/address": "10.5.40.1/24",
                            "/20/vpn-instance/ip/route/VPN20_TRAFFICGEN_DC1/prefix": "10.5.21.0/24",
                            "/20/vpn-instance/ip/route/VPN20_TRAFFICGEN_BR/prefix": "10.5.23.0/24",
                            "/20/vpn-instance/ip/route/VPN20_TRAFFICGEN_DC1/next-hop/VPN20_TRAFFIC_DC1_NH/address": "10.5.20.65",
                            "/20/vpn-instance/ip/route/VPN20_TRAFFICGEN_BR/next-hop/VPN20_TRAFFIC_BR_NH/address": "10.5.20.68",
                            "/20/VPN20_INTERFACE/interface/if-name": "GigabitEthernet6",
                            "/20/VPN20_INTERFACE/interface/ip/address": "10.5.20.1/24",
                            "/10/vpn-instance/ip/route/VPN10-TRAFFIC-GEN-DC1/prefix": "10.5.11.0/24",
                            "/10/vpn-instance/ip/route/VPN10-TRAFFIC-GEN-BR/prefix": "10.5.13.0/24",
                            "/10/vpn-instance/ip/route/VPN10-TRAFFIC-GEN-DC1/next-hop/VPN10_TRAFFIC_NH_DC1/address": "10.5.10.65",
                            "/10/vpn-instance/ip/route/VPN10-TRAFFIC-GEN-BR/next-hop/VPN10_TRAFFIC_NH_BR/address": "10.5.10.68",
                            "/10/VPN10_INTERFACE/interface/if-name": "GigabitEthernet5",
                            "/10/VPN10_INTERFACE/interface/ip/address": "10.5.10.1/24",
                            "/512/vpn-instance/ip/route/0.0.0.0/0/next-hop/VPN512_GW/address": "198.18.3.1",
                            "/512/VPN512_INTERFACE/interface/if-name": "GigabitEthernet1",
                            "/512/VPN512_INTERFACE/interface/ip/address": "198.18.3.107/24",
                            "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/MPLS_GW_IP_ADDR/address": "100.64.0.21",
                            "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/INET_GW_IP_ADDR/address": "100.64.2.9",
                            "/0/LTE_TLOC_INTERFACE/interface/if-name": "GigabitEthernet4",
                            "/0/LTE_TLOC_INTERFACE/interface/ip/address": "100.64.4.10/30",
                            "/0/MPLS_TLOC_INTERFACE/interface/if-name": "GigabitEthernet2",
                            "/0/MPLS_TLOC_INTERFACE/interface/ip/address": "100.64.0.22/30",
                            "/0/INET_TLOC_INTERFACE/interface/if-name": "GigabitEthernet3",
                            "/0/INET_TLOC_INTERFACE/interface/ip/address": "100.64.2.10/30",
                            "//system/host-name": "BR3-CEDGE1",
                            "//system/gps-location/latitude": "37.33",
                            "//system/gps-location/longitude": "-87.62",
                            "//system/system-ip": "10.5.0.1",
                            "//system/site-id": "500",
                            "/0/vpn-instance/ip/route/0.0.0.0/0/next-hop/LTE_GW_IP_ADDR/address": "100.64.4.9",
                            "csv-templateId": configTemplateId
                        }
                    ],
                    "isEdited": True,
                    "isMasterEdited": False
                }
            ]
        }

        reaplicaTemplate(attachFeatureJson)

        input("Enter any key to continue.")
    else:
        exit()
