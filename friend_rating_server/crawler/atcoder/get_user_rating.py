from typing import Dict, Any
import logging
import datetime
import requests
from lxml import etree
from friend_rating_server.util.loading_cache import SchedulerCache


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


USER_RATING_CACHE = SchedulerCache(get_competition_history)

if __name__ == "__main__":
    logging.getLogger().setLevel(20)
    print(USER_RATING_CACHE.get('ConanYu'))
    print(USER_RATING_CACHE.get('tourist'))
    print(USER_RATING_CACHE.get('ConanYu'))
    print(USER_RATING_CACHE.get('ConanYu'))
    while True:
        pass
