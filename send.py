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
    """
    Fetch token and number from JSONBin.
    Returns a tuple (token, number) or (None, None) if failed.
    """
    url = f"https://api.jsonbin.io/v3/b/{BIN_ID}/latest"
    headers = {"X-Master-Key": API_KEY}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            record = r.json()["record"]
            return record.get("token"), record.get("number")
        else:
            print(f"{R}JSONBin fetch failed: {r.status_code}{D}")
            return None, None
    except Exception as e:
        print(f"{R}JSONBin error: {e}{D}")
        return None, None

def send_otp_request(token, number):
    """Send OTP request and return response"""
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
        'X-Internal-Request': str(random.randint(10000000, 99999999)),  # Randomize this
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-full-version-list': '"Chromium";v="139.0.7339.0", "Not;A=Brand";v="99.0.0.0"',
        'sec-ch-ua-bitness': '""',
        'sec-ch-ua-model': '"LE2101"',
        'sec-ch-ua-platform': '"Android"',
        'Origin': 'https://6s.live',
        'X-Requested-With': 'XMLHttpRequest',
    }

    json_data = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': '6s.live',
        'receiver': number,
        'callingCode': '880',
    }
    
    try:
        response = requests.post(
            'https://6s.live/api/bt/v2_1/user/getVerifyCodeByContactType',
            headers=headers,
            json=json_data,
            timeout=15
        )
        return response.json()
    except Exception as e:
        print(f"{R}Request error: {e}{D}")
        return None

def send_noti():
    BOT_TOKEN = "8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE"
    CHAT_ID = "-5099546793"
    msg = "✅ SIX BOOSTING STARTED SUCCESSFULLY!"
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": msg, 'parse_mode': 'Markdown'},
            timeout=5
        )
    except:
        pass

def switch():
    try:
        s = requests.get("https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch", timeout=10).text
        if "ON" in s:
            return True
        else:
            print(f"\n{BOLD}{R} THIS TOOL HAS BEEN DISABLED BY ADMIN!{D}")
            return False
    except:
        print(f"{Y}Switch check failed, continuing...{D}")
        return True

def main():
    os.system("clear")
    
    if not switch():
        return
    
    token, number = fetch_data()
    
    if not token or not number:
        print(f"\n{BOLD}{R}Failed to fetch token or number from JSONBin{D}")
        return
    
    print(f"\n{BOLD}{B}[+] TARGET NUMBER: {G}{number}{D}")
    print(f"{BOLD}{B}[+] TOKEN STATUS: {G}Loaded{D}\n")
    
    i = 1
    
    while True:
        # Refresh token and number every 5 attempts
        if i % 5 == 1:
            token, number = fetch_data()
            if not token or not number:
                print(f"{R}Failed to refresh data, retrying in 30 seconds...{D}")
                time.sleep(30)
                continue
        
        print(f"\n{BOLD}{Y}═"*50)
        print(f" ATTEMPT #{i}")
        print(f"═"*50 + f"{D}\n")
        
        input(f"{BOLD}{Y}[+] PRESS ENTER TO SEND OTP{D} ")
        
        response = send_otp_request(token, number)
        
        if not response:
            print(f"{R}No response from server, waiting 10 seconds...{D}")
            time.sleep(10)
            i += 1
            continue
        
        # Debug: print full response
        print(f"{B}Full Response: {response}{D}")
        
        api_status = response.get("status")
        msg = response.get("message", "No message")
        
        print(f"\n{BOLD}{B}[+] Status: {Y}{api_status}{D}")
        print(f"{BOLD}{B}[+] Message: {Y}{msg}{D}")
        
        if api_status == "000000":
            print(f"\n{BOLD}{G}✅ OTP SENT SUCCESSFULLY!{D}")
            print(f"{BOLD}{G}⏰ VALIDITY: 5 MINUTES{D}")
            send_noti()
            time.sleep(2)  # Wait before next attempt
            
        elif api_status == "FS9997":
            print(f"\n{R}❌ THIS NUMBER HAS ALREADY BEEN USED!{D}")
            print(f"{Y}Waiting for new number...{D}")
            time.sleep(30)
            continue
            
        elif api_status == "FS9998":
            print(f"\n{R}⚠️ SENDING FAILED (FS9998){D}")
            print(f"{Y}Possible reasons:{D}")
            print(f"{Y}1. Too many requests (rate limited){D}")
            print(f"{Y}2. Token expired or invalid{D}")
            print(f"{Y}3. IP blocked{D}")
            print(f"{Y}Waiting 15 seconds before retry...{D}")
            time.sleep(15)
            
        elif api_status == "S0001":
            print(f"\n{R}❌ YOU ARE LOGGED OUT. PLEASE LOG IN AGAIN.{D}")
            print(f"{Y}Check your token in JSONBin.{D}")
            time.sleep(10)
            
        else:
            print(f"\n{Y}⚠️ Unknown status: {api_status}{D}")
            print(f"{Y}Waiting 10 seconds...{D}")
            time.sleep(10)
        
        # Add random delay between attempts to avoid detection
        delay = random.uniform(8, 15)
        print(f"\n{B}{BOLD}[⏰] Next attempt in {delay:.1f} seconds...{D}")
        time.sleep(delay)
        
        i += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}Tool stopped by user{D}")
    except Exception as e:
        print(f"\n{R}Unexpected error: {e}{D}")
