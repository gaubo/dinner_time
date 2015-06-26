from lxml import html
import urllib
from datetime import date, datetime, timedelta

def main():
    get_meal_info()

def get_meal_info():
    url = "https://zerocater.com/menu/uVGcXhj/"
    tree = html.fromstring(urllib.urlopen(url).read())
    meals = tree.xpath('//div[@class="inherit-height meal-item"]')

    for meal in meals:
        today = meal.xpath('.//span[@class="meal-is-today label"]/text()')
        if len(today) == 0:
            continue

        meal_info = {}
        vendor = meal.xpath('.//h1[@class="vendor-name"]/text()')
        meal_info['vendor'] = get_string(vendor)
        order = meal.xpath('.//h3[@class="order-name"]/text()')
        meal_info['order'] = get_string(order)
        image = meal.xpath('.//img[@class="vendor-image"]/@src')
        meal_info['img_url'] = get_string(image)
        description = meal.xpath('.//p[@class="vendor-description"]/text()')
        meal_info['description'] = get_string(description)

        meal_info['items'] = []
        items = meal.xpath('.//li[@class="list-group-item"]')
        for item in items:
            item_info = {}
            item_name = item.xpath('.//h4[@class="item-name"]/text()')
            item_info['name'] = get_string(item_name)
            item_description = item.xpath('.//div[@class="item-description"]/text()')
            item_info['description'] = get_string(item_description)
            item_img_url = item.xpath('.//img[@class="img-responsive"]/@src')
            item_info['img_url'] = get_string(item_img_url)
            meal_info['items'].append(item_info)

        return meal_info

def get_meal_info2():
    url = "https://zerocater.com/menu/uVGcXhj/"
    tree = html.fromstring(urllib.urlopen(url).read())
    meals = tree.xpath('//div[@class="inherit-height meal-item"]')
    i = 0
    for meal in meals:
        today = meal.xpath('.//span[@class="meal-is-today label"]/text()')
        if len(today) > 0:
            break

        date = meal.xpath('.//h4[@class="overview-time"]/text()')
        date_string = get_string(date)
        date_string = ' '.join(date_string.split())
        day = int(date_string[-2:].strip())
        print day
        print date_string
        today = datetime.utcnow() - timedelta(hours=7)
        print today.day
        if today.day <= day:
            break

        i = i + 1

    meal_today = meals[i]
    vendor = meal_today.xpath('.//div[@class="overview-wrapper"]')[0]
    menu = meal_today.xpath('.//ul[@class="list-group swiper-no-swiping"]')[0]
    data = {}
    data['overview'] = html.tostring(vendor)
    data['menu'] = html.tostring(menu)
    print data
    return data

def get_string(element):
    if len(element) == 0:
        return None
    return element[0].encode('utf-8').strip()

if __name__ == "__main__":
    get_meal_info2()