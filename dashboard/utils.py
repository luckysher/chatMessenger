##############################################
#       Chat messenger utils file            #
##############################################

import logging
APP_NAME = 'CHATMESS'

def getLogger():
    logging.basicConfig(format='[%(name)s][%(levelname)s] %(message)s', level=logging.DEBUG)
    return logging.getLogger(APP_NAME)

# fun for getting the next url posting
def getNextUrl(request):
    nextUrl = None
    if request.method == 'POST' and 'next' in request.POST:
        nextUrl = request.POST.get('next')
    return nextUrl

# fun for getting user id from request
def getUserId(request):
    return request.__dict__['_user'].getUserId()

def getuser(request):
    return request.__dict__['_user'].get_full_name()

def getFirstLastName(full_name):

    first_name = ""
    last_name = ""

    if full_name.find(' ') > 0:
        first_name = full_name[: full_name.find(' ')]
        last_name = full_name[full_name.find(' ')+1 : len(full_name)]
        print(first_name, " ",  last_name)
    else:
        first_name = full_name.strip(' ')

    return first_name, last_name