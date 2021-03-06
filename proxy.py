import requests
from bs4 import BeautifulSoup
from random import choice

def get_proxy():
    html = requests.get('https://free-proxy-list.net/').text
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find('table', id='proxylisttable').find_all('tr')[1:150]

    proxies = []

    for tr in trs:
        tds = tr.find_all('td')
        ip = tds[0].text.strip()
        port = tds[1].text.strip()
        location = tds[2].text.strip()
        #schema = 'https' if 'yes' in tds[6].text.strip() else 'http'
        #if 'RU' in location:
        if tds[6].text.strip() == 'no':
            schema = 'http'
            proxy = {'schema': schema, 'address': ip + ':' + port}
            proxies.append(proxy)

    return choice(proxies)

def get_html(url):
    p = get_proxy()
    proxy= {p['schema']:p['address']}
    r = requests.get(url, proxies=proxy, timeout=5)
    return r.json()['origin']




def main():
    url = 'http://httpbin.org/ip'
    print(get_proxy())
    print(get_html(url))

if __name__ == '__main__':
    main()