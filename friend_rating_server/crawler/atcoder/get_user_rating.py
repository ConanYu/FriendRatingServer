from typing import Dict, Any
import datetime
import requests
from lxml import etree


def get_competition_history(handle: str) -> Dict[str, Any]:
    try:
        url = f'https://atcoder.jp/users/{handle}/history'
        html = requests.get(url).text
        obj = etree.HTML(html)
        res = obj.xpath('//table[@id="history"]//tr[contains(@class, "text-center")]')
        ret = []
        for item in res:
            table = etree.tostring(item)
            table = etree.HTML(table)
            performance = table.xpath('//td[4]')[0].text
            if performance == '-':
                continue
            data = {
                'time': datetime.datetime.strptime(table.xpath('//td[1]/@data-order')[0], '%Y/%m/%d %H:%M:%S'),
                'name': table.xpath('//td[2]/a[1]')[0].text,
                'url': table.xpath('//td[2]/a[1]/@href')[0],
                'rank': table.xpath('//td[3]/a')[0].text,
                'performance': int(performance),
                'new_rating': int(table.xpath('//td[5]/span')[0].text),
            }
            ret.append(data)
        return {
            'status': 'OK',
            'data': ret,
            'username': handle,
        }
    except Exception as e:
        return {
            "status": "unknown error",
            "exception": e,
        }
