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
    """JSONBin থেকে ডাটা ফেচ করা"""
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json().get("record", {})
            token = data.get("token", "").strip()
            number = str(data.get("number", "")).strip()
            
            if token and number:
                print(f"{G}✓ Token লোড হয়েছে{D}")
                print(f"{G}✓ Number: {number}{D}")
                return token, number
            else:
                print(f"{R}✗ Token বা Number নেই{D}")
                return None, None
    except Exception as e:
        print(f"{R}✗ Error: {e}{D}")
        return None, None

def send_otp_request(token, number, attempt_num):
    """OTP পাঠানোর রিকুয়েস্ট"""
    
    # আপনার দেওয়া হেডার্স (এক্সাক্ট ব্রাউজার থেকে)
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'referer': 'https://6s.live/bd/en/member/profile',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'x-internal-request': '61405202',
        'origin': 'https://6s.live'
    }
    
    # ✅ সঠিক বডি ফরম্যাট - নতুন OTP পাঠানোর জন্য
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': '6s.live',  # এখানে শুধু domain, https:// নয়
        'receiver': str(number),
        'callingCode': '880'
        # ❌ verifyCode: দিবেন না - শুধু verify করার সময় দিতে হয়
        # ❌ random: দিবেন না - শুধু verify করার সময় দিতে হয়
    }
    
    print(f"\n{B}[চেষ্টা #{attempt_num}] OTP পাঠানো হচ্ছে...{D}")
    print(f"{B}📱 নাম্বার: {number}{D}")
    print(f"{B}🔑 টোকেন: {token[:40]}...{D}")
    
    try:
        # ✅ সঠিক API endpoint ব্যবহার করুন
        response = requests.post(
            'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType',  # ✅ সঠিক
            headers=headers,
            json=payload,
            timeout=15
        )
        
        print(f"{B}📊 HTTP Status: {response.status_code}{D}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                return data
            except:
                return {"raw": response.text}
        else:
            return {"error": f"HTTP {response.status_code}", "text": response.text}
            
    except Exception as e:
        return {"error": str(e)}

def verify_otp(token, number, verify_code):
    """OTP verify করার ফাংশন (যদি প্রয়োজন হয়)"""
    headers = {
        'accept': 'application/json, text/plain, */*',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'referer': 'https://6s.live/bd/en/member/profile',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'x-internal-request': '61405202'
    }
    
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'verifyCode': verify_code,
        'callingCode': '880',
        'random': '157c0755db8340b5be1ae83c158e8fb2',
        'receiver': str(number)
    }
    
    try:
        response = requests.post(
            'https://6s.live/api/bt/v1/user/verifyContact',
            headers=headers,
            json=payload,
            timeout=15
        )
        return response.json()
    except:
        return None

def send_telegram_notification(message):
    """টেলিগ্রাম নোটিফিকেশন"""
    try:
        BOT_TOKEN = '8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE'
        CHAT_ID = '-5099546793'
        requests.post(
            f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage',
            json={'chat_id': CHAT_ID, 'text': message, 'parse_mode': 'Markdown'},
            timeout=5
        )
        print(f"{G}📨 Telegram notification sent{D}")
    except:
        print(f"{Y}⚠️ Failed to send Telegram notification{D}")

def main():
    os.system('clear')
    
    print(f"{BOLD}{B}" + "="*70)
    print(f"{BOLD}{G}           SIX OTP SENDER - CORRECT API FIX")
    print(f"{BOLD}{B}" + "="*70 + f"{D}")
    
    # টুল স্যুইচ চেক
    try:
        switch = requests.get(
            'https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch',
            timeout=5
        ).text
        if 'OFF' in switch:
            print(f"{R}✗ Tool disabled by admin!{D}")
            return
        print(f"{G}✓ Tool is enabled{D}")
    except:
        print(f"{Y}⚠️ Could not check switch{D}")
    
    # ডাটা লোড
    token, number = fetch_data()
    if not token or not number:
        print(f"{R}✗ Failed to load data{D}")
        return
    
    print(f"\n{B}" + "-"*50)
    print(f"{B}🎯 Target Number: {G}{number}{D}")
    print(f"{B}🔑 Token: {G}{token[:50]}...{D}")
    print(f"{B}" + "-"*50 + f"{D}\n")
    
    attempt = 1
    
    while True:
        print(f"\n{Y}" + "="*50)
        print(f"   Attempt #{attempt}")
        print("="*50 + f"{D}")
        
        input(f"{BOLD}{Y}👉 Press ENTER to send OTP: {D}")
        
        # OTP পাঠানো
        result = send_otp_request(token, number, attempt)
        
        print(f"\n{B}📄 Response:{D}")
        
        if 'error' in result:
            print(f"{R}✗ Error: {result['error']}{D}")
            if 'text' in result:
                print(f"{Y}{result['text'][:200]}...{D}")
        else:
            # JSON রেসপন্স ডিসপ্লে
            for key, value in result.items():
                if key != 'raw':
                    print(f"   {B}{key}: {Y}{value}{D}")
            
            api_status = result.get('status')
            message = result.get('message', '')
            
            print(f"\n{B}🎯 API Status: ", end="")
            
            if api_status == '000000':
                print(f"{G}{api_status} ✓ SUCCESS{D}")
                print(f"{G}✅ OTP sent successfully!{D}")
                print(f"{G}⏰ Code valid for 5 minutes{D}")
                
                # টেলিগ্রাম নোটিফিকেশন
                tg_msg = f"✅ OTP SENT SUCCESSFULLY!\n📱 Number: {number}\n🔢 Status: {api_status}"
                send_telegram_notification(tg_msg)
                
                # যদি verification code থাকে
                verify_code = result.get('verificationCode')
                if verify_code:
                    print(f"\n{G}🔢 Verification Code: {verify_code[:50]}...{D}")
                    
                    # Automatically verify (optional)
                    # verify_response = verify_otp(token, number, "0245")
                    # print(f"Verify response: {verify_response}")
                
            elif api_status == 'FS9997':
                print(f"{R}{api_status} ✗ NUMBER ALREADY USED{D}")
                print(f"{R}❌ This number is already registered{D}")
                
            elif api_status == 'FS9998':
                print(f"{R}{api_status} ✗ SENDING FAILED{D}")
                print(f"{R}⚠️ Failed to send OTP{D}")
                
            elif api_status == 'S0001':
                print(f"{R}{api_status} ✗ LOGGED OUT{D}")
                print(f"{R}❌ Session expired, please login again{D}")
                
            elif api_status:
                print(f"{Y}{api_status} ? UNKNOWN{D}")
                print(f"{Y}⚠️ Unknown status code{D}")
            else:
                print(f"{Y}No status code in response{D}")
        
        # অপেক্ষা
        wait_time = random.randint(10, 20)
        print(f"\n{B}⏳ Next attempt in {wait_time} seconds...{D}")
        
        for i in range(wait_time, 0, -1):
            print(f"\r{B}Waiting {i} seconds...{D}", end="", flush=True)
            time.sleep(1)
        print()
        
        attempt += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}✗ Stopped by user{D}")
    except Exception as e:
        print(f"\n{R}💥 Error: {e}{D}")
