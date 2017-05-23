from urllib.request import urlopen
from urllib.parse import quote
import json
import re


qry_prefix = 'https://en.wikipedia.org/w/api.php?action=parse&section=0&redirects=1&prop=text&disablelimitreport=1&disableeditsection=1&disabletoc=1&format=json&page='


# precompile regexes
first_para_rx = re.compile(r'<p>.*?<b>.*?</p>')
first_para_nb_rx = re.compile(r'<p>.*?</p>')
second_para_rx = re.compile(r'<p>.*?<b>.*</p>\n<p>.*?</p>')
links_rx = re.compile(r'.*?<a href="/wiki/(.*?)"')
links_nb_rx = re.compile(r'<p>.*?<a href="/wiki/(.*?)"')
links_second_para_rx = re.compile(r'<a href="/wiki/(.*?)"')


manual_maps = {'Physical_body':'Physics',
               'Outline_of_human_anatomy':'Morphology_(biology)',
               'Study':'Education',
               'Southern_United_States':'United_States',
               'Transmission_(telecommunications)':'Analog_signal'}


# return first link
def get_next(page):
    first_link = None       # init

    if page in manual_maps:
        return manual_maps[page]

    # request page
    qry = qry_prefix+quote(page)
    try:
        with urlopen(qry) as res:
            json_ = json.loads(res.read().decode('utf-8'))
            html = json_['parse']['text']['*']
    except UnicodeEncodeError:
        # deal with special characters, like accents
        qry = qry_prefix+quote(page)
        try:
            with urlopen(qry) as res:
                json_ = json.loads(res.read().decode('utf-8'))
                html = json_['parse']['text']['*']
        except UnicodeEncodeError:
            return 'UnicodeEncodeError'
    except KeyError:
        return 'KeyError'

    # extract first paragraph
    para = re.findall(first_para_rx,html)
    if len(para)>0:
        para = para[0]
        # extract links
        links = re.findall(links_rx, rm_paren(para))
    else:
        # no bold in paragraph
        try:
            para = re.findall(first_para_nb_rx,html)[0]
        except IndexError:
            return 'IndexError'
        else: # extract link
            links = re.findall(links_nb_rx, rm_paren(para))

    # if no link in first paragraph, then get second paragraph
    if len(links)==0:
        para = re.findall(second_para_rx,html)
        if len(para)==0:
            # if no second paragraph, then page is deadend
            return 'deadend'
        else:
            links = re.findall(links_second_para_rx, rm_paren(para))
            if len(links)==0:
                return 'deadend'

    # get first link that's not a wikipedia guide
    for l in links:
        if ('Help:' not in l) and ('Wikipedia:' not in l) and ('Template:' not in l) and ('Special:' not in l) and ('User:' not in l) and ('User_talk:' not in l) and ('File:' not in l):
            first_link = l
            break

    if first_link is None:
        return 'NONE'
    else:
        # if parentheses deleted in link, put them back
        if first_link[-1] == '_':
            s = first_link + r'\(.*?\)'
            first_link = re.findall(s, para)[0]

        return first_link


# remove all text in parentheses
def rm_paren(test_str):
    ret = ''
    skip2c = 0
    count = 0
    for i in test_str:
        if i == '(':
            skip2c += 1
        elif i == ')'and skip2c > 0:
            skip2c -= 1
        elif skip2c == 0:
            ret += i
        count += 1
    return ret
