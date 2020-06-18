#!/usr/bin/python

import requests
import json

def get_temperature(appkey, city, module, units='metric'):
    session = requests.Session()
    headers = {'Content-Type': 'application/json'}
    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {'q': city, 'APPID': appkey, 'units': units}

    try:
    	response = session.request('GET', url, headers=headers, params=params)
    except requests.exceptions.RequestException as e:
    	module.fail_json(msg=e)

    if response.status_code not in [200]:
    	module.fail_json(msg=(response.status_code, response.content))

    response_content = json.loads(response.content)

    return response_content['main']['temp']


def main():
    module = AnsibleModule(
        argument_spec=dict(
        	appkey=dict(required=True),
            city=dict(default='munich,de'),
            treshold=dict(required=True, type='float')
        ),
    )

    city = module.params['city']
    treshold = module.params['treshold']
    appkey = module.params['appkey']
    temperature = get_temperature(appkey, city, module)
    
    if temperature > treshold:
        module.exit_json(changed=True, decision='Run, Yves, Run, it is {} in {}'.format(temperature, city))

    if temperature < treshold:
        module.exit_json(changed=False, decision='Stop, Yves, Stop, it is {} in {}'.format(temperature, city))

from ansible.module_utils.basic import *
main()
