#-----------------------------------------------------
#        DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#                    Version 2, December 2004 
#
# Copyright (C) 2004 Sam Hocevar <sam@hocevar.net> 
#
# Everyone is permitted to copy and distribute verbatim or modified 
# copies of this license document, and changing it is allowed as long 
# as the name is changed. 
#
#            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE 
#   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION 
#
#  0. You just DO WHAT THE FUCK YOU WANT TO.
#-----------------------------------------------------

import datetime
import os
import time
import twitter

api_key = ''
api_secret_key = ''
api_access_token = ''
api_secret_access_token = ''

api = twitter.Api(consumer_key=api_key,
                  consumer_secret=api_secret_key,
                  access_token_key=api_access_token,
                  access_token_secret=api_secret_access_token)

rightnow = datetime.datetime.now()
usernumber = -1
logfile = rightnow.strftime("%Y-%m-%d") + '.txt'
log = open(logfile, 'a+')

def i_am_not_following(username, myself=usernumber): 
    #time.sleep(90)
    returnvalue = None
    try:
        selflist = api.GetFollowers(screen_name=username, cursor=myself, count=1)
        print('the list length for ' + username + ' is ' + str(len(selflist)))
        if(len(selflist)==1):
            print('You are following ' + username + '.')
            returnvalue = False
        else:
            print('You are NOT following ' + username + '.')
            returnvalue = True

    except Exception as e:
        log.write(str(datetime.datetime.now()) + ' Following Method Error: ' + str(e) + '\n')
        log.write(str(datetime.datetime.now()) + ' Following Method Error: ' + username + '\n')
        print(str(datetime.datetime.now()) + ' In i_am_not_following method : probably ran into the rate limit ' + username)
        print(e.args[0])
    return returnvalue


def investigate_followers(investigated_user, oldcursor=-1, myself=usernumber):
    if(True):
        openfile = investigated_user + '-followers.txt'
        f = open(openfile, 'a+')
        newcursor = oldcursor
        stillgoing = True
        count = 0
        try:
            while stillgoing:
                userlist = api.GetFollowersPaged(screen_name=investigated_user, cursor=newcursor, count=200)
                newcursor = userlist[0]
                log.write(str(datetime.datetime.now()) + ' ' + str(newcursor) + '\n')
                log.flush()
                for user in userlist[2]:
                    if stillgoing:
                        log.write(str(datetime.datetime.now()) + ' ' + user.screen_name + '\n')
                        log.flush()
                        f.write(user.screen_name + "\n")
                        f.flush()
                    count = count + 1
                    if count % 10 == 0:
                        print('.', end='')
                    if count % 1000 == 0:
                        print('.')
                        print(str(count))
                if newcursor == oldcursor or newcursor == 0:
                    stillgoing = False
                    print('Ta Da!')    
                oldcursor = newcursor
                time.sleep(30)
            log.write(str(datetime.datetime.now()) + ' Finished: ' + investigated_user + '\n')

        except Exception as e:
            log.write(str(datetime.datetime.now()) + ' Method Error: ' + str(e) + '\n')
            log.write(str(datetime.datetime.now()) + ' Method Error: ' + investigated_user + ' ' + str(newcursor) + '\n')
            print(str(datetime.datetime.now()) + ' In investigate_followers method : probably ran into the rate limit ' + str(newcursor) + ' ' + investigated_user)
            time.sleep(120)
            print(e.args[0])
            if e.message and e.message == 'User not found.':
                print(str(datetime.datetime.now()) + ' In investigate_followers method : user not found block.' )
            elif e.message and e.message == ' Rate limit exceeded':
                print(str(datetime.datetime.now()) + ' In investigate_followers method : rate limit block.' )
        f.close()

def investigate_friends(investigated_user, oldcursor=-1, myself=usernumber):
    if(True):
        openfile = investigated_user + '-friends.txt'
        g = open(openfile, 'a+')
        newcursor = oldcursor
        stillgoing = True
        count = 0
        try:
            while stillgoing:
                userlist = api.GetFriendsPaged(screen_name=investigated_user, cursor=newcursor, count=200)
                newcursor = userlist[0]
                log.write(str(datetime.datetime.now()) + ' ' + str(newcursor) + '\n')
                log.flush()
                for user in userlist[2]:
                    if stillgoing:
                        log.write(str(datetime.datetime.now()) + ' ' + user.screen_name + '\n')
                        log.flush()
                        g.write(user.screen_name + "\n")
                        g.flush()
                    count = count + 1
                    if count % 10 == 0:
                        print('.', end='')
                    if count % 1000 == 0:
                        print('.')
                        print(str(count))
                if newcursor == oldcursor or newcursor == 0:
                    stillgoing = False
                    print('Ta Da!')    
                oldcursor = newcursor
                time.sleep(30)
            log.write(str(datetime.datetime.now()) + ' Finished: ' + investigated_user + '\n')

        except Exception as e:
            log.write(str(datetime.datetime.now()) + ' Method Error: ' + str(e) + '\n')
            log.write(str(datetime.datetime.now()) + ' Method Error: ' + investigated_user + ' ' + str(newcursor) + '\n')
            print(str(datetime.datetime.now()) + ' In investigate_friends method : probably ran into the rate limit ' + str(newcursor) + ' ' + investigated_user)
            time.sleep(120)
            print(e.args[0])
            if e.message and e.message == 'User not found.':
                print(str(datetime.datetime.now()) + ' In investigate_friends method : user not found block.' )
            elif e.message and e.message == ' Rate limit exceeded':
                print(str(datetime.datetime.now()) + ' In investigate_friends method : rate limit block.' )
        g.close()


testfile = open('testfile.txt', 'r')
myself = api.GetUser(screen_name='YOUR USER NAME')
print(myself.id)
listed_user = ''
try:
    while True: 
        user_line = testfile.readline().rstrip('\n')
        if not user_line:
            break
        else:
            next_user = user_line.split()
            listed_user = next_user[0]
            cursor = next_user[1]
            cursor2 = next_user[2]
            investigate_followers(listed_user, cursor)
            investigate_friends(listed_user, cursor2)
        
except Exception as e:
    log.write(str(datetime.datetime.now()) + ' Main Error: ' + str(e) + '\n')
    log.write(str(datetime.datetime.now()) + ' Main Error: ' + str(listed_user) + '\n')
    print(str(datetime.datetime.now()) + ' In main loop: probably ran into the rate limit ' + listed_user)
    print(e.args[0])

testfile.close()
log.close()
