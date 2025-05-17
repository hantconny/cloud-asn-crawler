# -*- coding:utf-8 -*-
"""
根据 AS 编号抓取国内云服务厂家的 IP 列表（IPv4 + IPv6）
"""
import requests
from bs4 import BeautifulSoup

ASN = {
    "ALI": ['AS37963', 'AS45102', 'AS134963', 'AS24429'],
    "BAIDU": ['AS38365', 'AS55967', 'AS56048', 'AS58657', 'AS38627'],
    "TENCENT": ['AS132203', 'AS45090', 'AS132203', 'AS133478'],
    "BYTEDANCE": ['AS396986', 'AS138699', 'AS139190', 'AS137775']
}


def go():
    def get(url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        for a in soup.find_all('a', href=True):
            href = a['href']
            if href.startswith('/net'):
                net_links.append(a.text)

        return net_links

    result = {}

    for _vendor, asn_list in ASN.items():
        net_links = []
        for asn in asn_list:
            net_links.extend(get(f'https://bgp.he.net/{asn}#_prefixes'))
            net_links.extend(get(f'https://bgp.he.net/{asn}#_prefixes6'))

        result.update({
            _vendor: net_links
        })

    return result


if __name__ == '__main__':
    for vendor, prefixes in go().items():
        with open(f'{vendor}.text', mode='w', encoding='utf-8') as f:
            f.write('\n'.join(prefixes))
