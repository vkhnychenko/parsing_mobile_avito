# -*- coding: utf-8 -*-
from proxy import get_proxy
from random import choice
import requests
from time import sleep
import csv
from multiprocessing import Pool

def get_json(url, useragent = None, proxy = None):
    r = requests.get(url, headers=useragent, proxies=proxy, timeout=5)
    return r.json()

def find_element(tree, element_name):
    if element_name in tree:
        return tree[element_name]
    for key, sub_tree in tree.items():
        if isinstance(sub_tree, dict):
            result = find_element(tree=sub_tree, element_name=element_name)
            if result:
                break
    else:
        result = None
    return result

def get_number(id, useragent = None, proxy = None):
    url_number = 'https://m.avito.ru/api/1/items/{}/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir' \
        .format(str(id))
    number = find_element(get_json(url_number, useragent, proxy), 'uri')
    number = number.split('%')[1][2:]
    return number

def check_number(number):
    with open('avito.csv', encoding='utf8') as file:
        fieldnames = ['id', 'number', 'url', 'location', 'userType']
        reader = csv.DictReader(file, fieldnames=fieldnames)
        read_data =[]
        for row in reader:
            read_data.append(row['number'])
        check = number in read_data
    return check

def write_csv(data):
    with open('avito.csv', 'a', encoding='utf8') as f:
        order = ['id', 'number', 'url', 'location', 'userType']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_page_data(url):
    p = get_proxy()
    proxy = {p['schema']: p['address']}
    useragents = open('useragent.txt').read().split('\n')
    useragent = {'User-Agent': choice(useragents)}
    print(useragent)
    print(proxy)
    url = get_json(url, useragent, proxy)
    print(url)
    items = (find_element(url, 'items'))
    print(items)
    sleep(0.5)
    for keys in items:
        value = find_element(keys, 'value')
        print(value)
        id = find_element(keys, 'id')
        if id is not None:
            uri = find_element(keys, 'uri_mweb')
            url = 'https://www.avito.ru' + str(uri)
            print(url)
            location = find_element(keys, 'location')
            user_type = find_element(keys, 'userType')
            try:
                number = get_number(id, useragent, proxy)
            except:
                number = ""
            if not check_number(number):
                data = {'id': id,
                        'number': number,
                        'url': url,
                        'location': location,
                        'userType': user_type}
                write_csv(data)

        if find_element(value, 'list'):
            list = find_element(value, 'list')
            for k in list:
                id = find_element(k, 'id')
                uri = find_element(k, 'uri_mweb')
                url = 'https://www.avito.ru' + str(uri)
                location = find_element(k, 'location')
                user_type = find_element(k, 'userType')
                print(url)
                try:
                    number = get_number(id, useragent, proxy)
                except:
                    number = ""
                if not check_number(number):
                    data = {'id': id,
                            'number': number,
                            'url': url,
                            'location': location,
                            'userType': user_type}
                    write_csv(data)
                continue

def main():
    #url = 'https://m.avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=641470&categoryId=19&page={}&lastStamp=1579138620&display=list&limit=30'
    # urls = [url.format(str(i)) for i in range(1, 101)]
    # with Pool(1) as p:
    #     p.map(get_page_data, urls)
    for i in range(1, 101):
        print(i)
        #base_url='https://m.avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&locationId=641470&categoryId=19&page={}&lastStamp=1579138620&display=list&limit=30'.format(str(i))
        url='https://m.avito.ru/api/9/items?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir&sort=default&locationId=641470&categoryId=85&page={}&lastStamp=1579228620&display=list&limit=30'.format(str(i))
        get_page_data(url)

if __name__ == '__main__':
    main()



