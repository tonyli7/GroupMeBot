#!/usr/bin/env python
import requests
import time
import datetime
import math
from groupy.client import Client
from groupy import attachments

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gettingstarted.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

    client = Client.from_token('QDGp5TUlTrv5nJcqgMgF6uUr2duyQCcfu0f4cG8P')
    list_of_groups = client.groups.list()
    main_group = {}
    for group in list_of_groups:
        if group.name == "Test Bot":
            main_group = group


    list_bots = client.bots.list()
    jack_jack = {}
    for bot in list_bots:
        if bot.name == "Jack Jack":
            jack_jack = bot

            now = datetime.datetime.now()

    # 0 1 2 3 4 5 6
    # M T W T F S S

    mon = 0
    tue = 1
    wed = 2
    thu = 3
    fri = 4
    sat = 5
    sun = 6

    members = []

    #initialize list
    for m in main_group.members:
        members.append({'name':m.nickname,
                        'user_id': m.user_id,
                        'break':False,
                        'start_time': 0,
                        'end_time': 0
                        
        })

        # Some variables that will be used in making calls to the APIs





    start_punch = False
    end_punch = False

    while True:
    


        # Listen for breaks
        last_message = main_group.messages.list()[0]
    
        if last_message.text == '@break':
            for i in range(0, len(members)):
                if members[i]['name'] == last_message.name and not members[i]['break']:
                    members[i]['break'] = True
                    members[i]['start_time'] = time.time()
                    members[i]['end_time'] = math.floor(time.time()) + 5
                    mention = attachments.Mentions(loci = [(0, len(members[i]['name']) + 1)],
                                                   user_ids = [members[i]['user_id']])
                
                    jack_jack.post(text = "@" + members[i]['name'] + " Timer Set", attachments = [mention])
                
    

        # Timer for breaks
        for i in range(0, len(members)):
            if members[i]['break']:
                if members[i]['end_time'] == math.floor(time.time()):
                    
                    members[i]['break'] = False
                    mention = attachments.Mentions(loci = [(0, len(members[i]['name']) + 1)],
                                                   user_ids = [members[i]['user_id']])
                    
                    jack_jack.post(text = "@" + members[i]['name'] + " Break is over", attachments = [mention])
                
    
        to_send = 'Punch in'
        if now.isoweekday() < 5 and now.hour == 8 and now.minute == 30 and not start_punch:
            main_group.post(text = to_send)
            start_punch = True

        if now.isoweekday() < 5 and now.hour == 5 and now.minute == 30 and not end_punch:
            main_group.post(test = to_send)
            end_punch = True

    
        
    
    

   

    
