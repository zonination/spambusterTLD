import praw
import time
import rlogin
import prawcore

# Log in
r = rlogin.pf()
print('Logged in as: {0}'.format(r.user.me()))
print('')

# Blacklist
blist = ['viajarencamboya.com', 'hangbiz.com', 'httpexploracamboya.com', 'freemom.httpexploracamboya.com', 'thekhmerfood.com']

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
            f.write('{4},{0},{1},{2},https://www.reddit.com{3}\n'.format(item.author.name, item.subreddit.display_name, item.domain, item.permalink, item.created))
            f.close()
            
            # Write a helpdesk ticket
            r.subreddit('reddit.com').message('Help Center Report','\nNew Help Center report has been received.\n\nReport details:\n- Report Reason: This is spam\n\n- Reported Users\n1) {0} (https://www.reddit.com/u/{0})\n\n\n\n\n        Custom Text: Spam from domain {3} made at {1} (GTC epoch), posted to https://www.reddit.com{2}\n\n'.format(item.author.name, item.created, item.permalink, item.domain))
            print(' + reported /u/{0} to the admins.\n'.format(item.author.name))
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
#    except:
#        print('\nException happened (PFhelper).\nTaking a coffee break.\n')
#    time.sleep(30)
