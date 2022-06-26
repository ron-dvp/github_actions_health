FROM python:3.9-alpine

WORKDIR /home/legit

COPY . /home/legit

RUN pip install -r ./requirement.txt

RUN crontab ./crontab && touch /tmp/out.log

CMD python /home/legit/test_github.py && crond && tail -f /tmp/out.log