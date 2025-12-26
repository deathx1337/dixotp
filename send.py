import requests
import json
import time
import os

BOLD = '[1m'
R = '[91m'
G = '[92m'
Y = '[93m'
B = '[94m'
D = '[0m'
BIN_ID = '69454f7643b1c97be9f91a85'
API_KEY = '$2a$10$TWuZ1cfV8BVaIKzzS2BGS.e56gTvpvpTAtDJz2S./2atXCKI2eIv2'

def fetch_data():
    """
    Fetch token and number from JSONBin.
    Returns a tuple (token, number) or (None, None) if failed.
    """
    url = f'https://api.jsonbin.io/v3/b/{BIN_ID}/latest'
    headers = {'X-Master-Key': API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        record = r.json()['record']
        return (record.get('token'), record.get('number'))
    return (None, None)

def main():
    os.system('clear')
    token, number = fetch_data()
    i = 1
    print(f'\n{BOLD}{B} THIS NUMBER WILL BE ADDED >> {G}{number}{D}\n')
    
    while True:
        token, number = fetch_data()
        print('\n\n')
        input(f'{BOLD}{Y} PRESS ENTER TO SEND {D}')
        headers = {
            'sec-ch-ua': '"Chromium";v="139", "Not;A=Brand";v="99"', 
            'sec-ch-ua-mobile': '?1', 
            'Authorization': f'Bearer {token}', 
            'sec-ch-ua-arch': '""', 
            'Content-Type': 'application/json', 
            'sec-ch-ua-full-version': '"139.0.7339.0"', 
            'Accept': 'application/json, text/plain, */*', 
            'sec-ch-ua-platform-version': '"14.0.0"', 
            'Referer': 'https://6s.live/bd/en/member/profile/info/verify-phone', 
            'X-Internal-Request': '61405202', 
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36', 
            'sec-ch-ua-full-version-list': '"Chromium";v="139.0.7339.0", "Not;A=Brand";v="99.0.0.0"', 
            'sec-ch-ua-bitness': '""', 
            'sec-ch-ua-model': '"LE2101"', 
            'sec-ch-ua-platform': '"Android"'
        }
        json_data = {
            'languageTypeId': 1, 
            'currencyTypeId': 8, 
            'contactTypeId': 2, 
            'domain': 'https://6s.live', 
            'receiver': number, 
            'callingCode': '880'
        }
        
        try:
            response = requests.post('https://6s.live/api/wv/v1/user/getVerifyCodeByContactType', headers=headers, json=json_data)
            response_data = response.json()
            api_status = response_data.get('status')
            msg = response_data.get('message')
            print(msg)
            print(f'{BOLD}{B} ATTEMPT >> {G}{i}{D}')
            
            if api_status == '000000':
                send_noti()
                print(f'\n{BOLD}{G} OTP SENT VALIDITY >> 5 MUNITES{D}')
            elif response_data.get('status') == 'FS9997':
                print(f'{R} THIS NUMBER ALREADY USED!{D}')
                return
            elif 'S0001' == api_status:
                print(f'{BOLD}{R} You are logged out. Please Log In and Try Again{D}')
            else:
                print(f' ⚠️ {api_status}')
                print(f'{R} OTP FAILED TO SEND TRY AGAIN !{D}')
                
        except Exception as e:
            print(e)
        
        i += 1

def send_noti():
    BOT_TOKEN = '8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE'
    CHAT_ID = '-5099546793'
    msg = 'FB BOOSTING START....'
    requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'}).json()

def switch():
    s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch').text
    if 'ON' in s:
        return
    print(f'\n{BOLD}{R} THIS TOOL HAS DISABLED BY ADMIN!{D}')
    exit(0)

switch()
main()