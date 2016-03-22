import new
import sys
import uuid
from random import randint
import rstr

def on_platforms(platforms):
    def decorator(base_class):
        module = sys.modules[base_class.__module__].__dict__
        for i, platform in enumerate(platforms):
            d = dict(base_class.__dict__)
            d['desired_capabilities'] = platform
            name = "%s_%s" % (base_class.__name__, i + 1)
            module[name] = new.classobj(name, (base_class,), d)

    return decorator


def get_random_uuid(length=5):
    return str(uuid.uuid1())[:length]


def get_random_integer(length=2):
    range_start = 10**(length-1)
    range_end = (10**length)-1
    return str(randint(range_start, range_end))


def get_random_email():
    return get_random_uuid() + "@" + get_random_uuid() + ".pl",


def get_random_phone():
    return "+48." + get_random_integer(9)


def get_random_zip():
    return get_random_integer() + "-" + get_random_integer(3),


def get_random_address():
    return get_random_uuid() + " " + get_random_integer()

def get_random_string(length):
    return rstr.rstr("abcdefghijklmnoprstuwxyz", length)