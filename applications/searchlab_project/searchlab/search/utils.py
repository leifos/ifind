import redis
import random
import string

import django.utils.crypto as django

from ifind.search import EngineFactory



def check_input(input_string):
    """
    Takes a unicode string, encodes it to ascii
    whilst stripping out the punctuation.

    Returns cleaned string or None if string
    contains nothing/spaces.

    """
    # encode to ascii, ignoring non ascii chars
    s = input_string.encode('ascii', 'ignore')

    # remove all punctuation
    s = s.translate(string.maketrans("",""), string.punctuation)

    # set to None if just spaces
    if s.isspace():
        s = None

    return s


# def get_client_ip(request):
#     """
#     Get the client ip from the request (from stackoverflow <3)
#
#     """
#     remote_address = request.META.get('REMOTE_ADDR')
#     # set the default value of the ip to be the REMOTE_ADDR if available
#     # else None
#     ip = remote_address
#     # try to get the first non-proxy ip (not a private ip) from the
#     # HTTP_X_FORWARDED_FOR
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         proxies = x_forwarded_for.split(',')
#         # remove the private ips from the beginning
#         while (len(proxies) > 0 and
#                 proxies[0].startswith(PRIVATE_IPS_PREFIX)):
#             proxies.pop(0)
#         # take the first ip which is not a private one (of a proxy)
#         if len(proxies) > 0:
#             ip = proxies[0]
#
#     return ip


def get_or_create_experiment(exp_id):
    """
    Creates an engine/query.top permutation as an "experiment",
    assigns it an ID and is hashed to redis and tracked via a set.

    Returns experiment hashmap to caller.

    """
    PREFIX = 'exp-'
    SET_NAME = 'experiments'

    r = redis.StrictRedis()

    # if experiment id passed as argument
    if exp_id:
        var_list = r.hmget(exp_id, 'engine', 'top')

        # return experiment
        return {'id': exp_id,
                'engine': var_list[0],
                'top': int(var_list[1])}

    while True:

        # create experiment ID
        exp_id = PREFIX + django.get_random_string()

        # add to experiment set list
        ret = r.sadd(SET_NAME, exp_id)

        # if add was successful (first time running or new ID was unique)
        if ret:
            break

    # pick random engine
    engine = random.choice([e for e in EngineFactory().engines() if e != 'dummy' if e != 'bing'])
    # pick random top value
    top = random.choice(xrange(5, 50))

    experiment = {'id': exp_id,
                  'engine': engine,
                  'top': top}

    # save experiment in redis
    r.hmset(exp_id, experiment)

    return experiment