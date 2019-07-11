import praw
import time
import rlogin
import prawcore

# Log in
r = rlogin.pf()
print('Logged in as: {0}'.format(r.user.me()))
print('')

# Blacklist
blist = ['viajarencamboya.com', 'hangbiz.com']

# MODULE FOR SUBMISSIONS
def submissions():
    # Review the submissions in modqueue
    for item in r.subreddit('mod').mod.modqueue(only='submissions'):
        if item.domain in blist:
            
            item.mod.nsfw()
            item.mod.remove(spam=True)
            r.subreddit(item.subreddit.display_name).banned.add(item.author.name, ban_reason='spam: {0}'.format(item.domain))
            
            # King's Justice has been delivered. Now show proof and log the file.
            print('Banned /u/{0} from /r/{1} for spamming {2}'.format(item.author.name, item.subreddit.display_name, item.domain))
            f = open('log.csv', 'a+')
            f.write('{0},{1},{2},https://www.reddit.com{3}\n'.format(item.author.name, item.subreddit.display_name, item.domain, item.permalink))
            f.close()
            return



# MAIN LOOP
while True:
    try:
        submissions()
        
        # Now sleeeeeeep!
        time.sleep(10)
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
