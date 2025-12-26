import requests
import json
import time
import os
import random

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
    
    if not token or not number:
        print(f'{R}❌ Token or number not found in JSONBin{D}')
        return
    
    print(f'\n{BOLD}{B}🎯 TARGET NUMBER: {G}{number}{D}')
    print(f'{BOLD}{B}🔑 TOKEN LOADED: {G}{token[:30]}...{D}\n')
    
    while True:
        token, number = fetch_data()
        print('\n' + '='*60)
        
        input(f'{BOLD}{Y}📱 PRESS ENTER TO SEND OTP {D}')
        
        # র্যান্ডম রিকুয়েস্ট আইডি জেনারেট করা
        request_id = str(random.randint(10000000, 99999999))
        
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
            'X-Internal-Request': request_id,  # র্যান্ডম আইডি
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36', 
            'sec-ch-ua-full-version-list': '"Chromium";v="139.0.7339.0", "Not;A=Brand";v="99.0.0.0"', 
            'sec-ch-ua-bitness': '""', 
            'sec-ch-ua-model': '"LE2101"', 
            'sec-ch-ua-platform': '"Android"',
            'Origin': 'https://6s.live',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        json_data = {
            'languageTypeId': 1, 
            'currencyTypeId': 8, 
            'contactTypeId': 2, 
            'domain': '6s.live',  # ✅ এখানে https:// দিবেন না
            'receiver': number, 
            'callingCode': '880'
        }
        
        print(f'{B}📡 Sending request to API...{D}')
        print(f'{B}🔢 Number: {number}{D}')
        print(f'{B}🆔 Request ID: {request_id}{D}')
        
        try:
            # ✅ CORRECT API ENDPOINT
            response = requests.post(
                'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType', 
                headers=headers, 
                json=json_data,
                timeout=15
            )
            
            print(f'{B}📊 Status Code: {response.status_code}{D}')
            
            if response.status_code == 200:
                response_data = response.json()
                
                # ডিবাগিং: পুরো রেসপন্স দেখানো
                print(f'{B}📄 Full Response: {json.dumps(response_data, indent=2)}')
                
                api_status = response_data.get('status', 'NO_STATUS')
                msg = response_data.get('message', 'No message')
                
                print(f'{BOLD}{B}🎯 STATUS: {Y}{api_status}{D}')
                print(f'{BOLD}{B}📨 MESSAGE: {Y}{msg}{D}')
                
                if api_status == '000000':
                    send_noti()
                    print(f'\n{BOLD}{G}✅ OTP SENT SUCCESSFULLY!{D}')
                    print(f'{BOLD}{G}⏰ VALIDITY: 5 MINUTES{D}')
                    
                elif api_status == 'FS9997':
                    print(f'{R}❌ THIS NUMBER ALREADY USED!{D}')
                    return
                    
                elif api_status == 'S0001':
                    print(f'{BOLD}{R}⚠️ You are logged out. Please Log In and Try Again{D}')
                    
                elif api_status == 'FS9998':
                    print(f'{R}⚠️ OTP SENDING FAILED (FS9998){D}')
                    print(f'{Y}Possible reasons:{D}')
                    print(f'{Y}1. Rate limited{D}')
                    print(f'{Y}2. Invalid token{D}')
                    print(f'{Y}3. Server issue{D}')
                    
                else:
                    print(f'{R}⚠️ UNKNOWN STATUS: {api_status}{D}')
                    print(f'{R}OTP FAILED TO SEND!{D}')
                    
            else:
                print(f'{R}❌ API Error: {response.status_code}{D}')
                print(f'{R}Response: {response.text[:200]}{D}')
                
        except Exception as e:
            print(f'{R}❌ Request Error: {e}{D}')
        
        print(f'\n{BOLD}{B}🎯 ATTEMPT #{i}{D}')
        
        # র্যান্ডম ডিলে - ডিটেকশন এড়ানো
        delay = random.uniform(10, 20)
        print(f'{B}⏰ Next attempt in {delay:.1f} seconds...{D}')
        
        # কাউন্টডাউন
        for sec in range(int(delay), 0, -1):
            print(f'\r{B}Waiting {sec} seconds...{D}', end='', flush=True)
            time.sleep(1)
        print()
        
        i += 1

def send_noti():
    BOT_TOKEN = '8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE'
    CHAT_ID = '-5099546793'
    msg = '✅ SIX BOOSTING STARTED SUCCESSFULLY!'
    
    try:
        requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage', 
            json={'chat_id': CHAT_ID, 'text': msg, 'parse_mode': 'Markdown'},
            timeout=5
        )
        print(f'{G}📨 Telegram notification sent{D}')
    except:
        print(f'{Y}⚠️ Failed to send Telegram notification{D}')

def switch():
    try:
        s = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch', timeout=10).text
        if 'ON' in s:
            print(f'{G}✅ Tool is ENABLED{D}')
            return True
        else:
            print(f'\n{BOLD}{R}❌ THIS TOOL HAS BEEN DISABLED BY ADMIN!{D}')
            return False
    except:
        print(f'{Y}⚠️ Switch check failed, continuing...{D}')
        return True

if __name__ == '__main__':
    if switch():
        main()
