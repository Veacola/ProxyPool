import asyncio
import aiohttp
import random
from socket import *

ports = [80, 8080, 3128, 8081, 9080, 1080, 21, 23, 443, 69, 22, 25, 110, 7001, 9090, 3389, 1521, 1158, 2100, 1433]

usable_ip = []


def crawl_universal():
    ip = ['', '', '', '']
    ip[0] = str(random.randint(5, 254))
    ip[1] = str(random.randint(100, 254))
    ip[2] = str(random.randint(10, 200))
    ip[3] = str(random.randint(1, 254))
    return '.'.join(ip)


def portScanner(host):
    print('scan ip:', host)
    for port in ports:
        try:
            s = socket(AF_INET, SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((host, port))
            print('%d open' % port)
            ip = ':'.join([str(host), str(port)])
            print(ip)
            usable_ip.append(ip)
            s.close()
        except:
            print('%d close' % port)

# host = crawl_universal()
# portScanner(host)
# print(usable_ip)

count = 0
while True:
    host = crawl_universal()
    portScanner(host)
    count += 1
    print(count)
    if count == 1000:
        break
print(usable_ip)


# async def main(proxy):
#     async with aiohttp.ClientSession() as session:
#         async with session.get('https://www.baidu.com', proxy="http://"+proxy, timeout=15) as resp:
#             print(resp.status)
#             print(await resp.text())

# loop = asyncio.get_event_loop()
# print('use ip:',crawl_universal())
# loop.run_until_complete(main('5.189.153.156:80'))