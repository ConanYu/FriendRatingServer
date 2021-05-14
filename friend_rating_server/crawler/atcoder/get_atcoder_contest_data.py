import datetime
import requests
from lxml import etree
import logging


def get_atcoder_contest_data(handle: str) -> dict:
    logging.info(f'crawling atcoder handle: {handle}')
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
                'timestamp': int(datetime.datetime.strptime(table.xpath('//td[1]/@data-order')[0],
                                                   '%Y/%m/%d %H:%M:%S').timestamp()),
                'name': table.xpath('//td[2]/a[1]')[0].text,
                'url': "https://atcoder.jp" + table.xpath('//td[2]/a[1]/@href')[0],
                'rating': int(table.xpath('//td[5]/span')[0].text),
            }
            ret.append(data)
        return {
            'status': 'OK',
            'data': ret,
            'handle': handle,
            'rating': ret[-1]["rating"] if len(ret) else None,
            'profile_url': f"https://atcoder.jp/users/{handle}",
            'length': len(ret),
        }
    except Exception as e:
        logging.exception(e)
        return {
            "status": "unknown error",
            "data": [],
        }


if __name__ == '__main__':
    print(get_atcoder_contest_data("ConanYu"))
