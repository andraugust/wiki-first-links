import wiki_utils
'''
Get first links recursively from a pre-defined start page.
'''

page = 'Physical_body'

print(page)
for _ in range(15):
    page = wiki_utils.get_next(page)
    # mark deadends
    if page=='deadend':
        print('^ deadend')
        break
    print(page)


# TODO: see if faster with full page GET

'''
Main issues:
    need to delete inside parenthesis, but not for links
    no links in first paragraph
    no links in summary (deadend) e.g., Study
    sometimes first links aren't the abstraction e.g., Transmission_(telecommunications)
'''
