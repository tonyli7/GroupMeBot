import requests
import time
import datetime
import math
from groupy.client import Client
from groupy import attachments

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
timer = 1800 #seconds
while True:
    


    # Listen for breaks
    last_message = main_group.messages.list()[0]
    
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
    
    if now.isoweekday() < 5 and now.hour == 8 + offset and now.minute == 28 and not start_punch:
        jack_jack.post(text = 'Punch in')
        start_punch = True

    
    if now.isoweekday() < 5 and now.hour == 17 + offset and now.minute == 28 and not end_punch:
        jack_jack.post(text = 'Punch out')
        end_punch = True


    if now.isoweekday() == WED and now.hour == 12 + offset and now.minute == 45 and not theme_day:
        jack_jack.post(text = 'Remember to do theme day')
        theme_day = True

    if now.isoweekday() == THU and now.hour == 17 + offset and now.minute == 58 and not diploma_start_punch:
        jack_jack.post(text = 'Punch in for diplomas')
        diploma_start_punch = True

    if now.isoweekday() == FRI and now.hour == 0 and now.minute == 28 and not diploma_end_punch:
        jack_jack.post(text = 'Punch out for diplomas')
        diploma_end_punch = True
        
    # Reset vars
    if now.hour == 0 + offset and now.minute == 0:
        start_punch = False
        end_punch = False
        theme_day = False
        diploma_start_punch = False
        diploma_end_punch = False
        
