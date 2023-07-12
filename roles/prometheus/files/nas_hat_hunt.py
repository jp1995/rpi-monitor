from bs4 import BeautifulSoup
import requests

results = {'allnet_ch': 0,
           'allnet_de': 0,
           'innet24': 0,
           'allnet_dk': 0,
           'maker': 0,
           'okdo_rock': 0,
           'okdo_pi': 0}
urls = [
    'https://shop.allnetchina.cn/collections/sata-hat/products/dual-sata-hat-open-frame-for-raspberry-pi-4?variant=31200524697702',
    'https://shop.allnet.de/search?sSearch=radxa&sPerPage=100',
    'https://www.innet24.de/search?sSearch=Radxa&sPage=1&sPerPage=48',
    'https://shop.allnet.dk/search?sSearch=Radxa&p=1&sPerPage=100',
    'https://shop.maker-store.de/search?sSearch=SATA%20HAT&sPerPage=48',
    'https://www.okdo.com/c/rock-shop/rock-accessories/rock-hats-and-add-ons/',
    'https://www.okdo.com/c/pi-shop/hats-phats/?orderby=price']


def generic_store_solve(url, store):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    product_info_divs = soup.find_all('div', {'class': 'product--info'})
    descriptions = []
    for div in product_info_divs:
        description_div = div.find('div', {'class': 'product--description'})
        if description_div:
            description = description_div.text.strip()
            descriptions.append(description)

    for description in descriptions:
        description = description.lower()
        if 'sata hat' in description or 'quad hat' in description or 'quad sata' in description:
            if 'penta hat' not in description and 'penta sata' not in description:
                results[store] = 1


def okdo_store_solve(url, store):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    a_elements = soup.find_all('a', {'class': 'c-product-listing__item'})

    data_names = []
    for a in a_elements:
        data_name = a.get('data-name')
        if data_name:
            data_names.append(data_name)

    for description in data_names:
        description = description.lower()
        if 'sata hat' in description or 'quad hat' in description or 'quad sata' in description:
            if 'penta hat' not in description and 'penta sata' not in description:
                results[store] = 1


def allnetCH_product_page_solve(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, 'html.parser')
    sold_out = soup.find('span', {'id': 'AddToCartText'})
    try:
        if sold_out.text.strip() != "Sold Out":
            results['allnet_ch'] = 1
    except AttributeError:
        pass


def push_data():
    pgw_url = 'http://iota:9091/metrics/job/pinas_sata_hat_hunt/instance/copium'
    payload = '\n'.join([f'pgw_nas{{site="{key}"}} {value}' for key, value in results.items()])
    payload += '\n'
    requests.post(pgw_url, data=payload)


if __name__ == '__main__':
    # allnet_ch product page for dual/quad hat
    allnetCH_product_page_solve(urls[0])

    # allnet_de products
    generic_store_solve(urls[1], 'allnet_de')

    # innet24 products
    generic_store_solve(urls[2], 'innet24')

    # allnet_dk products
    generic_store_solve(urls[3], 'allnet_dk')

    # maker-store products
    generic_store_solve(urls[4], 'maker')

    # okdo rock products
    okdo_store_solve(urls[5], 'okdo_rock')

    # okdo pi products
    okdo_store_solve(urls[6], 'okdo_pi')
    
    # send all gathered data to pushgateway-prometheus
    push_data()
