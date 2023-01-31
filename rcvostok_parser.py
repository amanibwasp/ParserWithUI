import requests
from bs4 import BeautifulSoup


def parser(vendor_code, params_dict):
    r = requests.get(f'https://rcvostok.ru/search?q={vendor_code}')
    if r.status_code != 200:
        return 'Error'
    params_dict['Артикул продавца'] = vendor_code
    soup = BeautifulSoup(r.text, 'lxml')
    params = soup.find('div', class_='tab-content')
    if params != None:
        params = params.find_all('p')
        params_list = []

        for param in params:
            try:
                name = param.find('span', class_='product_properties_name').get_text(strip=True)
                value = param.find('span', class_='product_properties_value').get_text(strip=True)
                params_list.append({name: value})

            except:
                continue
        try:
            desc = soup.find('div', {"id": "desc-bottom"}).get_text(strip=True)
        except:
            desc = 'Не указано'
        try:
            title = soup.find('h1', {"itemprop": "name"}).get_text(strip=True)
        except:
            title = 'Не указан'
        params_list.append({"Описание": desc})
        params_list.append({"Название": title})

    for p in params_list:
        name = list(p.keys())[0].lower()
        value = list(p.values())[0]
        if name == 'вес':
            params_dict['Вес'] = value
        elif 'страна' in name:
            params_dict['Страна производства'] = value
        elif 'бренд' in name:
            params_dict['Бренд'] = value
        elif 'состав' or 'материал' in name:
            params_dict['Состав'] = value
        elif 'цвет' in name:
            params_dict['Цвет'] = value
        elif name == 'описание':
            params_dict['Описание'] = value
        elif name == 'название':
            params_dict['Название'] = value

    try:
        images = soup.find('div', class_='catalog-item-article__images').find_all('div',
                                                                                  class_='catalog-item-article__additional-image')
    except:
        images = 'not found'
    images_set = set()
    if images != 'not found':
        for img in images:
            href = img.find('img').get('src')
            images_set.update(href)

    return [params_dict, images_set]
