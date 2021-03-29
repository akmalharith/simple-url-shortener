from math import floor
import string
import logging
logger = logging.getLogger(__name__)

BASE_LIST = string.digits + string.ascii_letters
BASE_NO = 62

def encode(num):
    """
    Encode a number to base62
    """
    r = num % BASE_NO
    res = BASE_LIST[r]
    q = floor(num / BASE_NO)
    while q:
        r = q % BASE_NO
        q = floor(q / BASE_NO)
        res = BASE_LIST[int(r)] + res
    return res

def decode(num):
    """
    Decode a number to base10
    """
    limit = len(num)
    res = 0
    for i in range(limit):
        res = BASE_NO * res + BASE_LIST.find(num[i])
    return res