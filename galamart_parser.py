import requests
from bs4 import BeautifulSoup
import math


def parser(vendor_code, params_dict):
    page = requests.get(f'https://galamart.ru/product/{vendor_code}/')
    if page.status_code != 200:
        print(vendor_code)
        return 'Error'
    soup = BeautifulSoup(page.text, 'lxml')
    try:
        params_dict['Название'] = soup.find('h1', class_='page-title').get_text(strip=True)
    except AttributeError:
        pass
    try:
        if soup.find('div', class_='product-desc').get_text(strip=True).strip() == '':
            params_dict['Описание'] = 'Не указано'
        else:
            params_dict['Описание'] = soup.find('div', class_='product-desc').get_text(strip=True)
    except AttributeError:
        pass
    try:
        params_dict['Бренд'] = soup.find('div', class_='brand').find('a').get_text(strip=True)
    except AttributeError:
        pass
    params_dict['Артикул продавца'] = vendor_code
    params = soup.find('table', class_='params-table')
    if params != None:
        params = params.find_all('tr')
        for p in params:
            tds = p.find_all('td')
            name = tds[0].get_text(strip=True)
            value = tds[1].get_text(strip=True)
            if 'Материал' in name or 'Состав' in name:
                params_dict['Состав'] = value
            elif 'Вес в упаковке' in name:
                allowed = [str(i) for i in range(0, 10)]
                allowed.extend([',', '.'])
                value = [str(i) for i in value if str(i) in allowed]
                value = ''.join(value)
                params_dict['Вес в упаковке'] = str(
                    math.ceil(float(value.replace(',', '.'))))
            elif 'Вес' in name:
                allowed = [str(i) for i in range(0, 10)]
                allowed.extend([',', '.'])
                value = [str(i) for i in value if str(i) in allowed]
                value = ''.join(value)
                params_dict['Вес'] = str(
                    math.ceil(float(value.replace(',', '.'))))
            elif 'Цвет' in name:
                params_dict['Цвет'] = value
            elif 'Страна производитель' in name or 'Страна производства' in name:
                params_dict['Страна производства'] = value
            elif 'Размер упаковки' in name:
                for i in ['x', 'X', 'х', 'Х']:
                    value = value.replace(i, '|')
                allowed = [str(i) for i in range(0, 10)]
                allowed.extend([',', '.', '|'])
                value = [str(i) for i in value if str(i) in allowed]
                value = ''.join(value)
                if len(value.split('|')) == 3:
                    params_dict['Высота упаковки'] = str(math.ceil(float(value.split('|')[0].replace(',', '.'))))
                    params_dict['Длина упаковки'] = str(math.ceil(float(value.split('|')[1].replace(',', '.'))))
                    params_dict['Ширина упаковки'] = str(math.ceil(float(value.split('|')[2].replace(',', '.'))))
            if 'Высота коробки' in name:
                allowed = [str(i) for i in range(0, 10)]
                allowed.extend([',', '.'])
                value = [str(i) for i in value if str(i) in allowed]
                value = ''.join(value)
                params_dict['Высота упаковки'] = str(
                    math.ceil(float(value.replace(',', '.'))))
            if 'Ширина коробки' in name:
                allowed = [str(i) for i in range(0, 10)]
                allowed.extend([',', '.'])
                value = [str(i) for i in value if str(i) in allowed]
                value = ''.join(value)
                params_dict['Ширина упаковки'] = str(
                    math.ceil(float(value.replace(',', '.'))))
            if 'Глубина коробки' in name:
                allowed = [str(i) for i in range(0, 10)]
                allowed.extend([',', '.'])
                value = [str(i) for i in value if str(i) in allowed]
                value = ''.join(value)
                params_dict['Длина упаковки'] = str(
                    math.ceil(float(value.replace(',', '.'))))
    images = soup.find_all('div', class_='slick-slide')

    images_hrefs = set()
    for i in images:
        try:
            img_href = i.find('img').get('src')
            images_hrefs.add(img_href)
        except:
            continue

    return [params_dict, images_hrefs]
