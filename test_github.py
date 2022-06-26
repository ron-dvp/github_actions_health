import slack_service
import requests
import sys
import datetime
import os


GITHUB_API = 'https://www.githubstatus.com/api/v2/summary.json'
MAIN_PORTAL= 'https://github.com'

class TestService:
    def __init__(self, main_portal_url, services_url, services):
        self.services_url = services_url
        self.main_portal_url = main_portal_url
        self.services = services
        self.results = {}

    def check_main_portal(self):
        req = requests.get(self.main_portal_url)
        code = req.status_code
        if code == 200:
            sys.stdout.write(f'{datetime.datetime.now()} INFO: Main portal is up\n')
            return
        else:
            sys.stdout.write(f'{datetime.datetime.now()} INFO: Main portal is down\n')
            return '[-] Main portal is down'


    def set_info(self,web_status):
        try:
            info = requests.get(self.services_url)
            res = info.json()
            for s in res['components']:
                if s['name'] in self.services:
                    self.results[s['name']] = s['status']
        except requests.exceptions.HTTPError:
            slack_service.send_message(f'GITHUB SERVICES \n Job failed \n ISSUE - API\n {web_status}')
            sys.stdout.write(f'{datetime.datetime.now()} ERROR: http error the github api\n')
            sys.exit(1)

    def get_info(self):
        return self.results


def init_data():
    sys.stdout.write(f'{datetime.datetime.now()} INFO: starting job\n')
    slack_alert = []
    with open(os.path.join(os.path.dirname(__file__),'services_to_test.txt'), 'r') as f:
        data = f.read()
        
        if data:
            services_li = [x for x in data.split('\n')]
            service = TestService(MAIN_PORTAL, GITHUB_API, services_li)

            # check web health check
            web_health = service.check_main_portal()
            if web_health:
                # Website id down, add to alert
                slack_alert.append(web_health)

            # set info for github services
            service.set_info(web_health)

            results = service.get_info()

            for k in results.items():
                if k[1] == 'operational':
                    sys.stdout.write(f'{datetime.datetime.now()} INFO: {k[0]} is up\n')
                else:
                    slack_alert.append(f'[-] {k[0]} is down')
                    sys.stdout.write(f'{datetime.datetime.now()} INFO: {k[0]} is down\n')

           
            if slack_alert:
                # If alert li is not empty notify team
                message = 'GITHUB SERVICES {}{}'.format('\n', '\n'.join(slack_alert))
                slack_service.send_message(message)

            sys.stdout.write(f'{datetime.datetime.now()} INFO: job done\n')
            sys.exit(0)
        else:
            slack_service.send_message('GITHUB SERVICES \n job failed \n ISSUE - FILE EMPTY')
            sys.stdout.write(f'{datetime.datetime.now()} ERROR: services_to_test.txt file is empty\n')
            sys.exit(1)


init_data()
