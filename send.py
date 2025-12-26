import requests, json, time, os
import random

BOLD = "\033[1m"
R = "\033[91m"
G = "\033[92m"
Y = "\033[93m"
B = "\033[94m"
D = "\033[0m"

BIN_ID = "69454f7643b1c97be9f91a85"
API_KEY = "$2a$10$TWuZ1cfV8BVaIKzzS2BGS.e56gTvpvpTAtDJz2S./2atXCKI2eIv2"

def fetch_data():
    """JSONBin থেকে টোকেন ও নাম্বার নেয়া"""
    url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
    headers = {"X-Master-Key": API_KEY}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            record = r.json()["record"]
            token = record.get("token")
            number = record.get("number")
            
            if token and number:
                print(f"{G}✅ JSONBin থেকে ডাটা লোড হয়েছে{D}")
                return token, number
            else:
                print(f"{R}❌ JSONBin এ টোকেন বা নাম্বার নেই{D}")
                return None, None
        else:
            print(f"{R}❌ JSONBin লোড ব্যর্থ: {r.status_code}{D}")
            return None, None
    except Exception as e:
        print(f"{R}❌ JSONBin এরর: {e}{D}")
        return None, None

def send_otp_request(token, number, attempt_num):
    """OTP রিকুয়েস্ট সেন্ড করা"""
    
    # প্রতিবার নতুন রিকুয়েস্ট আইডি
    request_id = random.randint(10000000, 99999999)
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://6s.live/bd/en/member/profile/info/verify-phone',
        'X-Internal-Request': str(request_id),
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'Origin': 'https://6s.live',
        'X-Requested-With': 'XMLHttpRequest',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

    json_data = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': '6s.live',
        'receiver': number,
        'callingCode': '880',
    }
    
    print(f"{B}📡 API কল করা হচ্ছে...{D}")
    print(f"{B}📱 নাম্বার: {number}{D}")
    print(f"{B}🔑 টোকেন: {token[:20]}...{D}")
    
    try:
        response = requests.post(
            'https://6s.live/api/bt/v2_1/user/getVerifyCodeByContactType',
            headers=headers,
            json=json_data,
            timeout=15
        )
        
        print(f"{B}📊 API রেসপন্স: {response.status_code}{D}")
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"{R}❌ API রেসপন্স কোড: {response.status_code}{D}")
            return None
            
    except Exception as e:
        print(f"{R}❌ রিকুয়েস্ট এরর: {e}{D}")
        return None

def send_telegram_notification():
    """টেলিগ্রামে নোটিফিকেশন সেন্ড করা"""
    BOT_TOKEN = "8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE"
    CHAT_ID = "-5099546793"
    msg = "✅ SIX BOOSTING চালু হয়েছে!"
    
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, 'parse_mode': 'Markdown'},
            timeout=5
        )
        print(f"{G}📨 টেলিগ্রাম নোটিফিকেশন সেন্ড হয়েছে{D}")
    except:
        print(f"{Y}⚠️ টেলিগ্রাম নোটিফিকেশন ব্যর্থ{D}")

def check_switch():
    """টুল চালু আছে কিনা চেক করা"""
    try:
        response = requests.get("https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch", timeout=10)
        if "ON" in response.text:
            print(f"{G}✅ টুল চালু আছে{D}")
            return True
        else:
            print(f"\n{R}❌ এই টুল অ্যাডমিন বন্ধ করেছেন!{D}")
            return False
    except:
        print(f"{Y}⚠️ স্যুইচ চেক ব্যর্থ, চালিয়ে যাচ্ছি...{D}")
        return True

def main():
    os.system("clear")
    
    print(f"{BOLD}{B}" + "="*60)
    print(f"{BOLD}{G}        SIX BOOSTING TOOL")
    print(f"{BOLD}{B}" + "="*60 + f"{D}\n")
    
    # টুল চালু আছে কিনা চেক
    if not check_switch():
        time.sleep(3)
        return
    
    # প্রথমে ডাটা ফেচ করা
    token, number = fetch_data()
    
    if not token or not number:
        print(f"\n{R}❌ টোকেন বা নাম্বার লোড করা যায়নি!{D}")
        print(f"{Y}JSONBin চেক করুন বা ৩০ সেকেন্ড পর আবার চেষ্টা করুন{D}")
        time.sleep(30)
        return
    
    print(f"\n{BOLD}{B}[+] টার্গেট নাম্বার: {G}{number}{D}")
    print(f"{BOLD}{B}[+] টোকেন স্ট্যাটাস: {G}লোডেড{D}\n")
    
    attempt_count = 1
    
    while True:
        print(f"\n{BOLD}{Y}" + "="*50)
        print(f"   চেষ্টা #{attempt_count}")
        print("="*50 + f"{D}\n")
        
        # প্রতি ৩ চেষ্টায় একবার ডাটা রিফ্রেশ
        if attempt_count % 3 == 1:
            print(f"{B}🔄 ডাটা রিফ্রেশ করা হচ্ছে...{D}")
            new_token, new_number = fetch_data()
            if new_token and new_number:
                token, number = new_token, new_number
                print(f"{G}✅ ডাটা আপডেট হয়েছে{D}")
        
        # ইউজার ইনপুট
        user_input = input(f"{BOLD}{Y}[+] এন্টার প্রেস করুন OTP সেন্ড করতে (বা 'exit' লিখুন): {D}")
        
        if user_input.lower() == 'exit':
            print(f"\n{Y}টুল বন্ধ করা হচ্ছে...{D}")
            break
        
        # OTP সেন্ড করা
        response = send_otp_request(token, number, attempt_count)
        
        if not response:
            print(f"{R}❌ সার্ভার থেকে রেসপন্স নেই, ১০ সেকেন্ড অপেক্ষা...{D}")
            time.sleep(10)
            attempt_count += 1
            continue
        
        # রেসপন্স এনালাইসিস
        api_status = response.get("status", "UNKNOWN")
        message = response.get("message", "কোন মেসেজ নেই")
        verification_code = response.get("verificationCode")
        
        print(f"\n{BOLD}{B}[+] স্ট্যাটাস: {Y}{api_status}{D}")
        print(f"{BOLD}{B}[+] মেসেজ: {Y}{message}{D}")
        
        if verification_code:
            print(f"{BOLD}{B}[+] ভেরিফিকেশন কোড: {G}{verification_code}{D}")
        
        # বিভিন্ন স্ট্যাটাস হ্যান্ডেলিং
        if api_status == "000000":
            print(f"\n{G}✅ OTP সফলভাবে সেন্ড হয়েছে!{D}")
            print(f"{G}⏰ ভ্যালিডিটি: ৫ মিনিট{D}")
            send_telegram_notification()
            
        elif api_status == "FS9997":
            print(f"\n{R}❌ এই নাম্বার ইতিমধ্যে ব্যবহৃত হয়েছে!{D}")
            print(f"{Y}নতুন নাম্বারের জন্য অপেক্ষা করছি...{D}")
            time.sleep(30)
            continue
            
        elif api_status == "FS9998":
            print(f"\n{R}⚠️ OTP সেন্ড ব্যর্থ (FS9998){D}")
            print(f"{Y}সম্ভাব্য কারণগুলো:{D}")
            print(f"  1. অনেকগুলো রিকুয়েস্ট (লিমিট){D}")
            print(f"  2. টোকেন এক্সপায়ার/ইনভ্যালিড{D}")
            print(f"  3. IP ব্লকড{D}")
            print(f"{Y}১৫ সেকেন্ড অপেক্ষা করছি...{D}")
            
        elif api_status == "S0001":
            print(f"\n{R}❌ আপনি লগআউট করেছেন। আবার লগইন করুন।{D}")
            print(f"{Y}JSONBin এ টোকেন চেক করুন{D}")
            
        else:
            print(f"\n{Y}⚠️ অজানা স্ট্যাটাস: {api_status}{D}")
            print(f"{Y}ফুল রেসপন্স: {response}{D}")
        
        # র্যান্ডম ডিলে - ডিটেকশন এড়ানো
        delay_time = random.uniform(10, 20)
        print(f"\n{B}{BOLD}[⏰] পরবর্তী চেষ্টা {delay_time:.1f} সেকেন্ড পর...{D}")
        
        # কাউন্টডাউন শো করা
        for sec in range(int(delay_time), 0, -1):
            print(f"\r{B}পরবর্তী চেষ্টা {sec} সেকেন্ড পর...{D}", end="", flush=True)
            time.sleep(1)
        print()
        
        attempt_count += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}⚠️ টুল ইউজার বন্ধ করেছেন{D}")
    except Exception as e:
        print(f"\n{R}❌ অপ্রত্যাশিত এরর: {e}{D}")
        print(f"{Y}টুল রিস্টার্ট করার চেষ্টা করুন{D}")
    
    print(f"\n{B}ধন্যবাদ, টুল ব্যবহারের জন্য!{D}")
