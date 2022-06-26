# LEGIT HOME TASK 

## Summary 
Setting up with docker a python service to inspect GIT-HUB status,
The automated script is running with a cron job that is configured in ./crontab. 


## requirements
- Docker installed on the local machine with user permissions

## Service build:
Setting file permission first, than you can run the deploy script,
```
chmod 754 build_deploy.sh; .
./build_deploy.sh
```
This service is being inialized as swarm manager, to scale the service, run 
```
docker swarm join-token worker
```
to get the manager token


## Service health checks:
Git hub services:
```
Git Operations, API Requests, Webhooks, Issues, Pull Requests, 
GitHub Actions, GitHub Packages, GitHub Pages, Codespaces
```

To add and remove services to check:
You can add the service name into ./services_to_test.txt with a new line,
- this file is bind-mounted into the docker service

To edit the cron job:
- Edit crontab file and re-build the service

Main site is always being checked.


## Initial Cron configuration
Service is runnig every minute, after inital deployment. 

## view serviec logs
'''
docker service logs legit_github_service
'''

## Slack notifications

Setup your ENV file to connect notification to a slack channel: 
SLACK_BOT_TOKEN=xoxo-token
CHANNEL_ID=chanell_id



### SOFTWARE DIAGRAM
in service_design.png

#### Author:
    Ron Portnoy
    ron.port11@gmail.com
