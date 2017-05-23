from urllib.request import urlopen
from urllib.parse import quote
import json
from time import sleep
'''
Get all page names in ns0 that don't redirect, write them to file.
Uses wikiapi, docs at https://www.mediawiki.org/wiki/API:Allpages

Notes:
Max query length is 500.

Results:
Requires about 26,000 queries.
Total pages: 10,609,764.
First page: !!
Last page: ʻotuhaka
'''

######
# Params and init

qry_prefix = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=allpages&apnamespace=0&apfilterredir=nonredirects&aplimit=499&apfrom='
qry_prefix_redir = 'https://en.wikipedia.org/w/api.php?action=query&format=json&list=allpages&apnamespace=0&aplimit=499&apfrom='
names_f = 'names.txt'
sleept = 0.05              # don't overload wikiservers!!!
end_name = '%CA%BBotuhaka' # 'ʻotuhaka' last name to print (basically the last one on wikipedia)


######
# Aux f'ns

def call_api(qry):
    with urlopen(qry) as res:
        json_ = json.loads(res.read().decode('utf-8'))
        names_etc = json_['query']['allpages']
    return [x['title'] for x in names_etc]


######
# Main

apfrom = '' # 'Ýedigen' (for testing ending)
numqueries = 30000
#open(names_f, 'w').close()
for i in range(numqueries):
    if i % 500 == 0:
        print('query num %i/%i' % (i, numqueries))

    # query
    sleep(sleept)
    qry = qry_prefix + quote(apfrom)
    res_names = call_api(qry)

    # if not enough names returned by api, then query with redirects to move forward...
    while len(res_names) < 2:
        # do redirect query
        qry = qry_prefix_redir + quote(apfrom)
        redir_names = call_api(qry)
        # do non-redirect query
        apfrom = redir_names[-1]
        qry = qry_prefix + quote(apfrom)
        res_names = call_api(qry)
        if end_name in [quote(x) for x in res_names]:
            print('at the last title')
            exit()

    # write names to file
    with open(names_f, 'a') as f:
        for n in res_names[0:-1]:
            f.write(n+'\n')
            if quote(n)==end_name:
                print('at the last title')
                exit()

    apfrom = res_names[-1]  # starting page for next query