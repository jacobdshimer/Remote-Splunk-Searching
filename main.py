#Future goals, change from using services to using proper namespaces.  This way,
#the user can use proper user/app context

import authenticate as auth
import search
import json
import argparse

#Setting up the argument parser
parser = argparse.ArgumentParser(
    add_help=True,
    description='''
    This is a utility script to send searches to Splunk. If ran with
    switch statements, it will take the username, password and hostname from them
    if there are no switch statements other then the search string, then it will
    attempt to open a settings.json.  If one is not available, then it will ask in the
    command prompt for the username, password, and hostname.'''
)

parser.add_argument('-s', '--search', action='store',
    dest='search',
    help='The search string to send to splunk.  This field is mandatory',
    required=True)
parser.add_argument('-u', '--username', action='store',
    dest='username',
    help=
    '''
    The username the search will be ran under.  This is optional, if left blank,
    the program will pull from a file called "settings.json"
    ''')
parser.add_argument('-p', '--password', action='store',
    dest='password',
    help=
    '''
    The password for the username.  This is optional, if left blank,
    the program will pull from a file called "settings.json"
    ''')
parser.add_argument('-host', '--hostname', action='store',
    dest='hostname',
    help=
    '''
    The hostname of the splunk instance the search will be ran against.
    This is optional, if left blank, the program will pull from a file
    called "settings.json"
    ''')
parser.add_argument('-o', '--output', action='store',
    dest='output_mode',
    help=
    '''
    This specifies the output mode of the search results.  The available options are:
    atom, csv, json, xml, and raw. This will default to json if it is not specified
    ''',
    default='json')
parser.add_argument('-of', '--output_file', action='store_true',
    default=False,
    dest='output_file',
    help=
    '''
    This specifies whether to output the results to a file or not.
    ''')
parser.add_argument('--port', action='store',
    dest='splunkdPort',
    help='The splunkd port.  If blank, defaults to port 8089',
    default='8089')
arguments = parser.parse_args()

#First check if neither the username, password, or hostname was provided
if (arguments.username is None and arguments.password is None) and arguments.hostname is None:
    with open('settings.json') as f:
        data = f.read()
        settings_json = json.loads(data)

#Then check if the hostname was provided but not the username or password
elif (arguments.username is None and arguments.password is None) and arguments.hostname != None:
    with open('settings.json') as f:
        data = json.loads(f.read())
        settings_json['hostname'] = arguments.hostname
        settings_json['username'] = data['username']
        settings_json['password'] = data['password']

#Then check if all three were provided
elif arguments.username != None and arguments.password != None and arguments.hostname != None:
    settings_json['hostname'] = arguments.hostname
    settings_json['username'] = arguments.username
    settings_json['password'] = arguments.password

#If hostname was not provided nor was it in the settings.json file, quit the program with an error
if settings_json['hostname'] == '' or settings_json['hostname'] is None:
    print('Hostname is required, either add it to settins.json or specify with the -host or --hostname switch.')
    exit()

#Get a session key
sessionKey = auth.getLogon(settings_json['hostname'],settings_json['username'], settings_json['password'],arguments.splunkdPort)
#Send the search
sid = search.sendSearch(sessionKey,settings_json['hostname'], settings_json['splunkdPort'],arguments.search)
#Retrive the status of the search
status = search.checkSearchStatus(sessionKey, settings_json['hostname'],settings_json['splunkdPort'],sid)

#Print the status, index 1 in status is an error flag.  If it is False, then something is wrong with the search string,
#if it is True, then everything is fine
print(status[0])
if status[1] == True:
    results = search.getResults(sessionKey,settings_json['hostname'],settings_json['splunkdPort'],sid,arguments.output_mode)
    if arguments.output_mode == 'json':
        parsed = json.loads(results)
        if arguments.output_file:
            with open(sid,'w+') as f:
                f.write(json.dumps(parsed, indent=4,sort_keys=True))
        else:
            print(json.dumps(parsed, indent=4,sort_keys=True))
    else:
        if arguments.output_file:
            with open(sid,'w+') as f:
                f.write(results)
        else:
            print(results)
elif status[1] == False:
    exit()
else:
    print("Something that shouldn't of happened happened, because this can literally only have two results")

#Clean up by deleting the token.
auth.deleteSession
