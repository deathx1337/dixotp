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
    url = f'https://api.jsonbin.io/v3/b/{BIN_ID}/latest'
    headers = {'X-Master-Key': API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        record = r.json()['record']
        token = record.get('token')
        number = record.get('number')
        print(f"{G}✅ Token found: {token[:50]}...{D}")
        print(f"{G}✅ Number found: {number}{D}")
        return (token, number)
    return (None, None)

def main():
    os.system('clear')
    
    print(f"{BOLD}{B}" + "="*60)
    print(f"{BOLD}{G}        SIX LIVE OTP SENDER TOOL")
    print(f"{BOLD}{B}" + "="*60 + f"{D}\n")
    
    # প্রথমে switch চেক
    try:
        switch_req = requests.get('https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch', timeout=5)
        if 'ON' not in switch_req.text:
            print(f"{R}❌ Tool disabled by admin!{D}")
            return
        print(f"{G}✅ Tool is enabled{D}\n")
    except:
        print(f"{Y}⚠️ Switch check skipped{D}\n")
    
    # ডাটা ফেচ
    token, number = fetch_data()
    if not token or not number:
        print(f"{R}❌ Failed to get token or number from JSONBin{D}")
        return
    
    print(f"\n{BOLD}{B}🎯 Target Number: {G}{number}{D}")
    print(f"{BOLD}{B}🔑 Token loaded successfully{D}\n")
    
    i = 1
    session = requests.Session()  # সেশন ব্যবহার
    
    while True:
        print(f"\n{BOLD}{Y}" + "="*50)
        print(f"   Attempt #{i}")
        print("="*50 + f"{D}\n")
        
        input(f"{BOLD}{Y}📱 Press ENTER to send OTP {D}")
        
        # প্রতিবার নতুন রিকুয়েস্ট আইডি
        request_id = random.randint(10000000, 99999999)
        
        # ASLI HEADERS - আপনার দেওয়া হেডার্স
        headers = {
            'accept': 'application/json, text/plain, */*',
            'authorization': f'Bearer {token}',
            'content-type': 'application/json',
            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'x-internal-request': str(request_id),
            'referer': 'https://6s.live/bd/en/member/profile',
            'origin': 'https://6s.live',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
        }
        
        # ASLI BODY - আপনার দেওয়া বডি (কিন্তু verificationCode ছাড়া)
        body_data = {
            'languageTypeId': 1,
            'currencyTypeId': 8,
            'contactTypeId': 2,
            'domain': 'https://6s.live',  # ✅ আপনার কাছ থেকে এইটাই পাওয়া গেছে
            'receiver': number,
            'callingCode': '880'
            # ❌ verificationCode: দিবেন না - শুধু নতুন OTP পাঠানোর জন্য
        }
        
        print(f"{B}📡 Sending OTP request...{D}")
        print(f"{B}📞 To number: {number}{D}")
        print(f"{B}🆔 Request ID: {request_id}{D}")
        print(f"{B}🌐 Domain: https://6s.live{D}")
        
        try:
            response = session.post(
                'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType',
                headers=headers,
                json=body_data,
                timeout=15
            )
            
            print(f"\n{B}📊 Response Status: {response.status_code}{D}")
            
            if response.status_code == 200:
                response_data = response.json()
                
                # ডিবাগিংয়ের জন্য পুরো রেসপন্স
                print(f"{B}📄 Full Response:")
                print(json.dumps(response_data, indent=2))
                print(f"{D}")
                
                api_status = response_data.get('status', 'NO_STATUS')
                message = response_data.get('message', 'No message')
                verification_code = response_data.get('verificationCode')
                
                print(f"\n{BOLD}{B}🎯 API Status: ", end="")
                if api_status == '000000':
                    print(f"{G}{api_status} ✅{D}")
                else:
                    print(f"{R}{api_status} ❌{D}")
                
                print(f"{BOLD}{B}📨 Message: {Y}{message}{D}")
                
                if verification_code:
                    print(f"{BOLD}{B}🔢 Verification Code: {G}{verification_code[:50]}...{D}")
                
                # বিভিন্ন স্ট্যাটাস হ্যান্ডেলিং
                if api_status == '000000':
                    print(f"\n{G}✅ SUCCESS! OTP sent successfully{D}")
                    print(f"{G}⏰ Code valid for 5 minutes{D}")
                    
                    # টেলিগ্রাম নোটিফিকেশন
                    try:
                        telegram_msg = f"✅ SIX OTP SENT!\n📱 Number: {number}\n🎯 Status: {api_status}"
                        requests.post(
                            'https://api.telegram.org/bot8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE/sendMessage',
                            json={'chat_id': '-5099546793', 'text': telegram_msg, 'parse_mode': 'Markdown'},
                            timeout=5
                        )
                        print(f"{G}📨 Telegram notification sent{D}")
                    except:
                        print(f"{Y}⚠️ Failed to send Telegram notification{D}")
                
                elif api_status == 'FS9997':
                    print(f"\n{R}❌ This number has already been used!{D}")
                    print(f"{Y}Waiting for new number...{D}")
                    time.sleep(30)
                    continue
                
                elif api_status == 'FS9998':
                    print(f"\n{R}⚠️ Sending failed (FS9998){D}")
                    print(f"{Y}Possible reasons:{D}")
                    print(f"{Y}  • Rate limit reached{D}")
                    print(f"{Y}  • Account/IP restriction{D}")
                    print(f"{Y}  • Server issue{D}")
                
                elif api_status == 'S0001':
                    print(f"\n{R}⚠️ You are logged out. Please login again.{D}")
                
                else:
                    print(f"\n{Y}⚠️ Unknown status code{D}")
                
            else:
                print(f"{R}❌ API Error: {response.status_code}{D}")
                print(f"{R}Response: {response.text[:200]}...{D}")
        
        except Exception as e:
            print(f"{R}❌ Request Error: {e}{D}")
        
        # র্যান্ডম ডিলে
        delay = random.uniform(10, 20)
        print(f"\n{B}{BOLD}⏰ Waiting {delay:.1f} seconds for next attempt...{D}")
        
        # কাউন্টডাউন
        for sec in range(int(delay), 0, -1):
            print(f"\r{B}Next in {sec} seconds...{D}", end='', flush=True)
            time.sleep(1)
        print()
        
        i += 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}⚠️ Tool stopped by user{D}")
    except Exception as e:
        print(f"\n{R}❌ Error: {e}{D}")
