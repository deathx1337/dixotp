import requests
import json
import time
import os
import random
from urllib.parse import urlparse
import uuid

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
                print(f"{G}✓ Token loaded: {token[:30]}...{D}")
                print(f"{G}✓ Number: {number}{D}")
                return token, number
            else:
                print(f"{R}✗ Token or number missing{D}")
                return None, None
        else:
            print(f"{R}✗ JSONBin error: {response.status_code}{D}")
            return None, None
    except Exception as e:
        print(f"{R}✗ Error: {e}{D}")
        return None, None

def create_browser_headers(token):
    """আসল ব্রাউজারের মতো হেডার্স তৈরি করা"""
    
    # র্যান্ডম ভ্যালু জেনারেট
    request_id = str(random.randint(10000000, 99999999))
    session_id = str(uuid.uuid4())
    
    headers = {
        # Basic headers
        'Host': '6s.live',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        
        # Authorization
        'Authorization': f'Bearer {token}',
        
        # Content
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,bn;q=0.8',
        'Content-Type': 'application/json',
        
        # Origin and Referer
        'Origin': 'https://6s.live',
        'Referer': 'https://6s.live/bd/en/member/profile/info/verify-phone',
        
        # Security headers
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        
        # Custom headers
        'X-Requested-With': 'XMLHttpRequest',
        'X-Internal-Request': request_id,
        
        # User Agent - Windows Chrome
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        
        # Cookies (simulated)
        'Cookie': f'_ga=GA1.1.{random.randint(100000000, 999999999)}.{random.randint(1000000000, 9999999999)}; _gid=GA1.2.{random.randint(100000000, 999999999)}.{random.randint(1000000000, 9999999999)}; session={session_id}'
    }
    
    return headers

def simulate_browser_session():
    """ব্রাউজার সেশন সিমুলেট করা"""
    session = requests.Session()
    
    # Browser-like settings
    session.headers.update({
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    })
    
    return session

def send_otp(token, number, attempt):
    """OTP পাঠানোর মেইন ফাংশন"""
    
    print(f"\n{B}[{attempt}] OTP পাঠানো হচ্ছে...{D}")
    print(f"{B}📱 নাম্বার: {number}{D}")
    print(f"{B}🔑 টোকেন: {token[:40]}...{D}")
    
    # 1. প্রথমে সাইট ভিজিট করা (ব্রাউজারের মতো)
    try:
        session = simulate_browser_session()
        
        print(f"{Y}1. সাইট ভিজিট করা হচ্ছে...{D}")
        homepage = session.get(
            "https://6s.live/bd/en/member/profile/info/verify-phone",
            timeout=15,
            allow_redirects=True
        )
        
        if homepage.status_code == 200:
            print(f"{G}✓ সাইট লোডেড: {len(homepage.text)} bytes{D}")
        else:
            print(f"{Y}⚠️ সাইট লোড: {homepage.status_code}{D}")
    except:
        print(f"{Y}⚠️ সাইট ভিজিট স্কিপড{D}")
    
    # 2. OTP রিকুয়েস্ট পাঠানো
    headers = create_browser_headers(token)
    
    payload = {
        "languageTypeId": 1,
        "currencyTypeId": 8,
        "contactTypeId": 2,
        "domain": "6s.live",  # এখানে https:// দিবেন না
        "receiver": str(number),
        "callingCode": "880"
    }
    
    print(f"{Y}2. API কল করা হচ্ছে...{D}")
    
    try:
        response = requests.post(
            "https://6s.live/api/bt/v1/user/getVerifyCodeByContactType",
            headers=headers,
            json=payload,
            timeout=20,
            allow_redirects=True,
            verify=True
        )
        
        print(f"{B}📊 HTTP Status: {response.status_code}{D}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"{G}✓ JSON রেসপন্স পেয়েছি{D}")
                return data, response.status_code
            except:
                print(f"{Y}⚠️ JSON পার্স করতে সমস্যা{D}")
                return {"raw": response.text}, response.status_code
                
        elif response.status_code == 403:
            print(f"{R}✗ 403 Forbidden - Cloudflare/WAF ব্লক করছে{D}")
            print(f"{Y}⚡ সমাধান: 5-10 মিনিট অপেক্ষা করুন{D}")
            return {"error": "403 Forbidden"}, 403
            
        elif response.status_code == 429:
            print(f"{R}✗ 429 Too Many Requests - Rate Limited{D}")
            print(f"{Y}⚡ সমাধান: 30 মিনিট অপেক্ষা করুন{D}")
            return {"error": "429 Rate Limited"}, 429
            
        else:
            print(f"{R}✗ HTTP {response.status_code}{D}")
            return {"error": f"HTTP {response.status_code}", "text": response.text[:200]}, response.status_code
            
    except requests.exceptions.Timeout:
        print(f"{R}✗ টাইমআউট হয়েছে{D}")
        return {"error": "Timeout"}, 0
    except Exception as e:
        print(f"{R}✗ Error: {e}{D}")
        return {"error": str(e)}, 0

def main():
    os.system("clear")
    
    print(f"{BOLD}{B}" + "="*65)
    print(f"{BOLD}{G}           SIX OTP SENDER - ULTIMATE FIX")
    print(f"{BOLD}{B}" + "="*65 + f"{D}")
    
    # টুল চালু আছে কিনা চেক
    try:
        switch = requests.get(
            "https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch",
            timeout=5
        ).text
        if "OFF" in switch:
            print(f"\n{R}✗ টুল বন্ধ করা আছে!{D}")
            return
        print(f"{G}✓ টুল চালু আছে{D}")
    except:
        print(f"{Y}⚠️ স্যুইচ চেক করা যায়নি{D}")
    
    # ডাটা লোড
    token, number = fetch_data()
    if not token or not number:
        print(f"{R}✗ ডাটা লোড করা যায়নি{D}")
        return
    
    print(f"\n{B}" + "-"*50)
    print(f"{B}🎯 টার্গেট: {number}")
    print(f"{B}🔑 টোকেন: {token[:40]}...")
    print(f"{B}" + "-"*50 + f"{D}")
    
    attempt = 1
    
    while True:
        print(f"\n{Y}" + "="*50)
        print(f"   চেষ্টা #{attempt}")
        print("="*50 + f"{D}")
        
        input(f"\n{BOLD}{Y}👉 এন্টার চাপুন OTP পাঠাতে: {D}")
        
        # OTP পাঠানো
        result, status = send_otp(token, number, attempt)
        
        if status == 200:
            print(f"\n{G}✅ API রেসপন্স:{D}")
            
            # রেসপন্স ডিসপ্লে
            if isinstance(result, dict):
                for key, value in result.items():
                    if key not in ['raw', 'error']:
                        print(f"   {B}{key}: {Y}{value}{D}")
                
                api_status = result.get('status')
                message = result.get('message', '')
                
                if api_status == '000000':
                    print(f"\n{G}🎉 সফল! OTP পাঠানো হয়েছে!{D}")
                    print(f"{G}⏰ কোড ৫ মিনিটের জন্য ভ্যালিড{D}")
                    
                    # টেলিগ্রাম নোটিফিকেশন
                    try:
                        tg_msg = f"✅ OTP সেন্ড সফল!\n📱: {number}\n🔢: {api_status}"
                        requests.post(
                            "https://api.telegram.org/bot8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE/sendMessage",
                            json={"chat_id": "-5099546793", "text": tg_msg},
                            timeout=3
                        )
                        print(f"{G}📨 টেলিগ্রামে নোটিফিকেশন পাঠানো হয়েছে{D}")
                    except:
                        print(f"{Y}⚠️ টেলিগ্রাম নোটিফিকেশন ব্যর্থ{D}")
                        
                elif api_status == 'FS9997':
                    print(f"\n{R}✗ এই নাম্বার ইতিমধ্যে ব্যবহৃত{D}")
                    
                elif api_status == 'FS9998':
                    print(f"\n{R}✗ OTP পাঠানো যায়নি (FS9998){D}")
                    
                elif api_status == 'S0001':
                    print(f"\n{R}✗ লগআউট হয়ে গেছে, আবার লগইন করুন{D}")
                    
                else:
                    print(f"\n{Y}⚠️ অজানা স্ট্যাটাস: {api_status}{D}")
                    
        elif status == 403:
            print(f"\n{R}🚫 গুরুত্বপূর্ণ: Cloudflare/WAF ব্লক করছে!{D}")
            print(f"{Y}সমাধানের উপায়:{D}")
            print(f"1. {B}5-10 মিনিট অপেক্ষা করুন{D}")
            print(f"2. {B}আপনার IP পরিবর্তন করুন (VPN/Proxy){D}")
            print(f"3. {B}ব্রাউজার থেকে ম্যানুয়ালি চেষ্টা করুন{D}")
            
        elif status == 429:
            print(f"\n{R}⚡ Rate limit exceeded!{D}")
            print(f"{Y}30 মিনিট অপেক্ষা করুন{D}")
            
        else:
            print(f"\n{R}⚠️ সমস্যা: HTTP {status}{D}")
            print(f"{Y}রেসপন্স: {str(result)[:100]}...{D}")
        
        # অপেক্ষা
        wait_time = random.randint(15, 25)
        print(f"\n{B}⏳ পরবর্তী চেষ্টা {wait_time} সেকেন্ড পর...{D}")
        
        for i in range(wait_time, 0, -1):
            print(f"\r{B}অপেক্ষা করুন: {i} সেকেন্ড...{D}", end="", flush=True)
            time.sleep(1)
        print()
        
        attempt += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}✗ ইউজার বন্ধ করেছেন{D}")
    except Exception as e:
        print(f"\n{R}💥 Error: {e}{D}")
