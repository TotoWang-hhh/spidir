import re

def match(filename,condition):
    return re.match(condition,filename)