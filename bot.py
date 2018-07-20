import requests
import time
import datetime
import math
from groupy.client import Client
from groupy import attachments
from groupy import exceptions

offset = 4
client = Client.from_token('QDGp5TUlTrv5nJcqgMgF6uUr2duyQCcfu0f4cG8P')
list_of_groups = client.groups.list()
main_group = {}
for group in list_of_groups:
    
    if group.name == "iDTech @ Marymount Boiiis":
        main_group = group
        
list_bots = client.bots.list()
jack_jack = {}
for bot in list_bots:
    if bot.name == "Jack Jack":
        jack_jack = bot



# 0 1 2 3 4 5 6
# M T W T F S S

MON = 0
TUE = 1
WED = 2
THU = 3
FRI = 4
SAT = 5
SUN = 6

members = []

#initialize list
for m in main_group.members:
    print(m.nickname)
    members.append({'name':m.nickname,
                    'user_id': m.user_id,
                    'break':False,
                    'start_time': 0,
                    'end_time': 0
                        
    })
    




start_punch = False
end_punch = False
theme_day = False
diploma_start_punch = False
diploma_end_punch = False
student_surveys = False
timer = 1800 #seconds
while True:
    


    # Listen for breaks
    last_message = ""
    try:
        last_message = main_group.messages.list()[0]
    except exceptions.BadResponse:
        continue
    
    if last_message.text == '@break':
        for i in range(0, len(members)):
            
            if members[i]['name'] == last_message.name and not members[i]['break']:
                members[i]['break'] = True
                members[i]['start_time'] = time.time()
                members[i]['end_time'] = math.floor(time.time()) + timer
                mention = attachments.Mentions(loci = [(0, len(members[i]['name']) + 1)],
                                               user_ids = [members[i]['user_id']])
                
                jack_jack.post(text = "@" + members[i]['name'] + " Timer Set", attachments = [mention])

    # @all function
    if last_message.text[0:4] == '@all':
        locis = []
        ids = []
        index = 0
        msg = ""
        for m in members:
            locis.append((index, len(m['name']) + 1))
            index += len(m['name']) + 1
            ids.append(m['user_id'])
            msg += "@" + m['name']
        mention_all = attachments.Mentions(loci = locis, user_ids = ids)
        jack_jack.post(text = msg, attachments = [mention_all])

    # Timer for breaks
    for i in range(0, len(members)):
        if members[i]['break']:
            if members[i]['end_time'] == math.floor(time.time()):
                    
                members[i]['break'] = False
                mention = attachments.Mentions(loci = [(0, len(members[i]['name']) + 1)],
                                               user_ids = [members[i]['user_id']])
                    
                jack_jack.post(text = "@" + members[i]['name'] + " Break is over", attachments = [mention])
                    

    now = datetime.datetime.now()
    
    # Punch in reminder at 8:28 AM weekdays
    if now.weekday() < 5 and now.hour == 8 + offset and now.minute == 30 and not start_punch:
        jack_jack.post(text = 'Punch in')
        start_punch = True

    # Punch out reminder at 8:28 AM weekdays
    if now.weekday() < 5 and now.hour == 17 + offset and now.minute == 15 and not end_punch:
        jack_jack.post(text = 'Punch out')
        end_punch = True

    # Theme day reminder at 12:45 PM on Wednesdays
    if now.weekday() == WED and now.hour == 12 + offset and now.minute == 30 and not theme_day:
        jack_jack.post(text = 'Remember to do theme day')
        theme_day = True

    # Punch in reminder at 5:58 PM Thursdays
    if now.weekday() == THU and now.hour == 17 + offset and now.minute == 58 and not diploma_start_punch:
        jack_jack.post(text = 'Punch in for diplomas')
        diploma_start_punch = True

    # Punch out at 8:28 PM Thursdays
    if now.weekday() == FRI and now.hour == 0 and now.minute == 28 and not diploma_end_punch:
        jack_jack.post(text = 'Punch out for diplomas')
        diploma_end_punch = True

    # Student surveys reminder
    if now.weekday() == FRI and now.hour == 14 + offset and now.minute == 0 and not student_surveys:
        jack_jack.post(text = 'Remember to do student surveys.')
        student_surveys = True
        
    # Reset vars at midnight
    if now.hour == 0 + offset and now.minute == 0:
        start_punch = False
        end_punch = False
        theme_day = False
        diploma_start_punch = False
        diploma_end_punch = False
        
    time.sleep(0.25)
