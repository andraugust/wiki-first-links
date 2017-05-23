import wiki_utils
import time
from urllib.parse import unquote
'''
Constructs a dict {page: next_page}

Notes:
dead-ends are given the next_page value of 'deadend'
pages with problems return 'IndexError'
unfound links return 'NONE'
Other errors: UnicodeEncodeError, KeyError
'''

names_f = 'names_all.txt'
net_f = 'net.txt'
sleept = 0.05           # DON'T OVERLOAD WIKI-SERVERS!!!!!

open(net_f, 'w').close()
with open(names_f,'r') as f:
    for line in iter(f):
        l = line.strip()
        with open(net_f,'a') as g:
            link = unquote(wiki_utils.get_next(l))
            g.write('%s\t%s\n' % (l,link))
        time.sleep(sleept)

'''
for k in net:
    print('%s : %s' % (k,net[k]))
'''