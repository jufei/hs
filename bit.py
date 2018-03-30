import os

import re
import requests

url = u'https://btso.pw/search/%E6%98%9F%E7%90%83%E5%A4%A7%E6%88%98'


class bit_torr(object):
    def __init__(self):
        self.maglist = []
        pass

    def getpage(self, url):
        print('Retrieve url: {}'.format(url))
        headers = {'User-Agent':
                   'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
        rn = requests.get(url, headers=headers, proxies={'https': 'https://10.144.1.10:8080'})
        if rn.status_code == 200:
            return rn.text
        else:
            raise Exception('Get URL {} failed'.format(url))

    def parse_search_result_page(self):
        return re.findall(r'(https://btso.pw/magnet/detail/hash/[a-zA-Z0-9]*)"',
                          open('a.html').read())

    def find_magnet(self, keyword):
        url = u'https://btso.pw/search/{}'.format(keyword)
        try:
            search_page_content = self.getpage(url)
        except:
            return 0

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(search_page_content, 'html.parser')
        alos = soup.find_all('a')
        maglist = [x for x in alos if x and 'detail/hash' in str(x.get('href')) and
                   keyword.upper() in str(x.get('title')).upper()]
        if maglist:
            hashlink = maglist[0].get('href')
            print('Found a valid link: {} --- {}'.format(maglist[0].get('title'), hashlink))
            try:
                detail_page = self.getpage(hashlink)

                magnets = re.findall(r'href="(magnet:[?a-z=A-Z:0-9&\-\%]*)', detail_page)
                if magnets:
                    print('Found magnet: {}'.format(magnets[0]))
                    self.maglist.append(magnets[0])
                    return magnets[0]
                else:
                    print('Could not find magnet.')
                    return ''
            except:
                pass
        else:
            print('No detail link found.')
            return ''

if __name__ == '__main__':
    torr = bit_torr()
    for i in range(100, 150):
        torr.find_magnet('star-{}'.format(i))
    with open('seed.txt', 'a') as f:
        for line in torr.maglist:
            f.write(line + '\n')
