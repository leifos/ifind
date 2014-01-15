__author__ = 'rose'

import random
with open('gla_url_list.txt') as f:
    urls = f.read().splitlines()

limited = []
for url in urls:
    if url.count('&') < 1 and url.count('/') <=6 and url.count('?') <1 and url.count('.') < 4:
        limited.append(url)

print len(limited)
#print urls
selection = random.sample(limited,50)
print selection
out = open("urls.txt","w")
for item in selection:
  out.write("%s\n" % item)

out.close()