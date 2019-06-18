import praw
import time
import rlogin
import prawcore
import requests

# Log in
r = rlogin.pf()
print('Logged in as: {0}'.format(r.user.me()))
print('')

# Redirected here? Blacklisted site.
blacklist = ['stockprice.com', 'truetradinggroup.com']

while True:
    try:
        for item in r.subreddit('mod').mod.modqueue(only='comments'):
            for string in str.split(item.body, '('):
                if string.startswith('http'):
                    justice = str.split(requests.get(str.split(string, ')')[0]).url, '/')[2]
                    # If you want an age filter, add: and ((time.time() - item.author.created_utc) < (60 * 60 * 24 * 30))
                    if (justice in blacklist):
                        item.mod.remove(spam=True)
                        r.subreddit(item.subreddit.display_name).banned.add(item.author.name, ban_reason='spam: {0}'.format(justice), ban_message='spam: {0}'.format(justice))
                        print('Banned /u/{0} from /r/{1} for spamming {2}'.format(item.author.name, item.subreddit.display_name, justice))
                    
        time.sleep(120)
    # Exception list for when Reddit inevitably screws up
    except praw.exceptions.APIException:
        print('\nAn API exception happened.\nTaking a coffee break.\n')
        time.sleep(30)
    except prawcore.exceptions.ServerError:
        print('\nReddit\'s famous 503 error occurred.\nTaking a coffee break.\n')
        time.sleep(180)
    except prawcore.exceptions.InvalidToken:
        print('\n401 error: Token needs refreshing.\nTaking a coffee break.\n')
        time.sleep(30)
    # Probably another goddamn Snoosletter that the bot can't reply to.
    except prawcore.exceptions.Forbidden:
        print('  Unable to respond. Marking as read.\n')
        for item in r.inbox.unread(limit=100):
            if item in r.inbox.messages(limit=100):
                item.mark_read()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        print('\nException happened (PFhelper).\nTaking a coffee break.\n')
        time.sleep(30)
