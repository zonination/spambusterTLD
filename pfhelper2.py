import praw
import time
import rlogin
import prawcore
import requests

# Log in
r = rlogin.pf()
print('Logged in as: {0}'.format(r.user.me()))
print('')

# Redirected here? Blacklist these sites.
blacklist = ['stockprice.com', 'truetradinggroup.com']


# MODULE FOR COMMENTS
def comments():
    # Review the comments in modqueue
    for item in r.subreddit('mod').mod.modqueue(only='comments'):
        # Check every word of the comment
        for body in str.split(item.body):
            # Split every open-parentheses
            for string in str.split(body, '('):
                # Check if there's an opening link [like reddit formatting](http://reddit.com)
                if string.startswith('http'):
                    # Check to see if the URL ends at one of our blacklisted sites. If you want an age filter, add: and ((time.time() - item.author.created_utc) < (60 * 60 * 24 * days))
                    justice = str.split(requests.get( str.split(string,')')[0] ).url, '/')[2]
                    if (justice in blacklist):
                        item.mod.remove(spam=True)
                        r.subreddit(item.subreddit.display_name).banned.add(item.author.name, ban_reason='spam: {0}'.format(justice), ban_message='spam: {0}'.format(justice))
                        # Justice has been delivered. Now show proof and log the file.
                        print('Banned /u/{0} from /r/{1} for spamming {2} (comment)'.format(item.author.name, item.subreddit.display_name, justice))
                        f = open('log.csv', 'a+')
                        f.write('comment, {0}, {1}, {2}, https://www.reddit.com{3}\n'.format(item.author.name, item.subreddit.display_name, justice, item.permalink))
                        f.close()
                        return


# MODULE FOR SUBMISSIONS
def submissions():
    # Review the submissions in modqueue
    for item in r.subreddit('mod').mod.modqueue(only='submissions'):
        # Check every word of the submission
        for body in str.split(item.selftext):
            # Split every open-parentheses
            for string in str.split(body, '('):
                # Check if there's an opening link [like reddit formatting](http://reddit.com)
                if string.startswith('http'):
                    # Check to see if the URL ends at one of our blacklisted sites. If you want an age filter, add: and ((time.time() - item.author.created_utc) < (60 * 60 * 24 * days))
                    justice = str.split(requests.get( str.split(string,')')[0] ).url, '/')[2]
                    if (justice in blacklist):
                        item.mod.remove(spam=True)
                        r.subreddit(item.subreddit.display_name).banned.add(item.author.name, ban_reason='spam: {0}'.format(justice), ban_message='spam: {0}'.format(justice))
                        # Justice has been delivered. Now show proof and log the file.
                        print('Banned /u/{0} from /r/{1} for spamming {2} (submission)'.format(item.author.name, item.subreddit.display_name, justice))
                        f = open('log.csv', 'a+')
                        f.write('submission, {0}, {1}, {2}, https://www.reddit.com{3}\n'.format(item.author.name, item.subreddit.display_name, justice, item.permalink))
                        f.close()
                        return



# MAIN LOOP
while True:
    try:
        comments()
        submissions()
        
        # Now sleeeeeeep!
        time.sleep(5)
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
#        time.sleep(30)
