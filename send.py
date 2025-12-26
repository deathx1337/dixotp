import requests
import json
import time
import os
import random
import secrets

BOLD = '[1m'
R = '[91m'
G = '[92m'
Y = '[93m'
B = '[94m'
D = '[0m'

BIN_ID = '69454f7643b1c97be9f91a85'
API_KEY = '$2a$10$TWuZ1cfV8BVaIKzzS2BGS.e56gTvpvpTAtDJz2S./2atXCKI2eIv2'

def fetch_data():
    """Fetch data from JSONBin"""
    url = f'https://api.jsonbin.io/v3/b/{BIN_ID}/latest'
    headers = {
        'X-Master-Key': API_KEY,
        'X-Bin-Meta': 'false'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            token = data.get('token', '').strip()
            number = str(data.get('number', '')).strip()
            
            if token and number:
                print(f"{G}✅ Token loaded (length: {len(token)}){D}")
                print(f"{G}✅ Number: {number}{D}")
                return token, number
            else:
                print(f"{R}❌ Token or number missing in JSONBin{D}")
                return None, None
        else:
            print(f"{R}❌ JSONBin error: {response.status_code}{D}")
            return None, None
    except Exception as e:
        print(f"{R}❌ JSONBin fetch error: {e}{D}")
        return None, None

def generate_fingerprint():
    """Generate browser-like fingerprint"""
    return {
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'platform': 'Win32',
        'language': 'en-US,en;q=0.9',
        'timezone': 'Asia/Dhaka',
        'screen_resolution': '1920x1080'
    }

def create_headers(token, request_id):
    """Create complete browser-like headers"""
    fp = generate_fingerprint()
    
    headers = {
        # Authorization
        'Authorization': f'Bearer {token}',
        
        # Standard headers
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': fp['language'],
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Host': '6s.live',
        'Origin': 'https://6s.live',
        'Referer': 'https://6s.live/bd/en/member/profile',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        
        # User agent and platform
        'User-Agent': fp['user_agent'],
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Ch-Ua-Platform-Version': '"15.0.0"',
        
        # Internal request ID
        'X-Internal-Request': str(request_id),
        'X-Requested-With': 'XMLHttpRequest',
        
        # Additional headers to bypass WAF
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        
        # Cookies simulation (important for session)
        'Cookie': f'session_id={secrets.token_hex(16)}; _ga=GA1.1.{random.randint(1000000000, 9999999999)}.{random.randint(1000000000, 9999999999)}'
    }
    
    return headers

def send_otp_request(token, number, attempt_num):
    """Send OTP request with proper browser simulation"""
    request_id = random.randint(10000000, 99999999)
    
    # Request body
    payload = {
        'languageTypeId': 1,
        'currencyTypeId': 8,
        'contactTypeId': 2,
        'domain': 'https://6s.live',
        'receiver': str(number),
        'callingCode': '880'
    }
    
    # Create headers
    headers = create_headers(token, request_id)
    
    print(f"{B}📡 Sending OTP request (Attempt #{attempt_num})...{D}")
    print(f"{B}📱 To: +880 {number}{D}")
    print(f"{B}🆔 Request ID: {request_id}{D}")
    
    # Create session with browser-like settings
    session = requests.Session()
    
    # Add retry logic
    retries = 3
    for retry in range(retries):
        try:
            response = session.post(
                'https://6s.live/api/bt/v1/user/getVerifyCodeByContactType',
                headers=headers,
                json=payload,
                timeout=30,
                allow_redirects=True,
                verify=True  # SSL verification
            )
            
            print(f"{B}📊 HTTP Status: {response.status_code}{D}")
            
            if response.status_code == 200:
                try:
                    return response.json(), response.status_code
                except json.JSONDecodeError:
                    print(f"{Y}⚠️ Response is not JSON{D}")
                    return {'message': response.text}, response.status_code
            elif response.status_code == 403:
                print(f"{R}❌ 403 Forbidden - Cloudflare/WAF blocked{D}")
                print(f"{Y}↻ Retrying ({retry + 1}/{retries})...{D}")
                time.sleep(5)
                continue
            else:
                return {'error': f'HTTP {response.status_code}', 'message': response.text}, response.status_code
                
        except requests.exceptions.Timeout:
            print(f"{R}❌ Request timeout{D}")
            if retry < retries - 1:
                print(f"{Y}↻ Retrying...{D}")
                time.sleep(3)
                continue
            return {'error': 'Timeout'}, 0
        except requests.exceptions.RequestException as e:
            print(f"{R}❌ Network error: {e}{D}")
            if retry < retries - 1:
                print(f"{Y}↻ Retrying...{D}")
                time.sleep(3)
                continue
            return {'error': str(e)}, 0
    
    return {'error': 'Max retries exceeded'}, 0

def main():
    os.system('clear')
    
    print(f"{BOLD}{B}" + "="*70)
    print(f"{BOLD}{G}           SIX LIVE OTP SENDER (BYPASS 403 FIX)")
    print(f"{BOLD}{B}" + "="*70 + f"{D}\n")
    
    # Check if tool is enabled
    try:
        switch_resp = requests.get(
            'https://raw.githubusercontent.com/havecode17/dg/refs/heads/main/switch',
            timeout=10
        )
        if 'ON' not in switch_resp.text:
            print(f"{R}❌ Tool disabled by admin!{D}")
            return
        print(f"{G}✅ Tool Status: ENABLED{D}")
    except:
        print(f"{Y}⚠️ Could not check switch status{D}")
    
    # Fetch data
    token, number = fetch_data()
    if not token or not number:
        print(f"{R}❌ Could not fetch token or number{D}")
        time.sleep(5)
        return
    
    print(f"\n{BOLD}{B}" + "-"*50)
    print(f"{BOLD}{B}🎯 Target: {G}{number}{D}")
    print(f"{BOLD}{B}🔑 Token: {G}{token[:30]}...{D}")
    print(f"{BOLD}{B}" + "-"*50 + f"{D}\n")
    
    attempt = 1
    
    while True:
        print(f"\n{BOLD}{Y}" + "="*50)
        print(f"   Attempt #{attempt}")
        print("="*50 + f"{D}")
        
        input(f"\n{BOLD}{Y}🚀 Press ENTER to send OTP {D}")
        
        # Send OTP request
        response_data, status_code = send_otp_request(token, number, attempt)
        
        if status_code == 200:
            print(f"\n{B}✅ Server Response:{D}")
            print(json.dumps(response_data, indent=2, ensure_ascii=False))
            
            api_status = response_data.get('status')
            message = response_data.get('message', 'No message')
            
            print(f"\n{BOLD}{B}🎯 API Status: ", end="")
            if api_status == '000000':
                print(f"{G}{api_status} ✓ SUCCESS{D}")
                print(f"{G}✅ OTP sent successfully!{D}")
                print(f"{G}⏰ Valid for 5 minutes{D}")
                
                # Send Telegram notification
                try:
                    telegram_msg = f"✅ OTP Sent Successfully!\n📱 Number: {number}\n🔢 Status: {api_status}"
                    requests.post(
                        'https://api.telegram.org/bot8345339682:AAFs60FHY__L2dSKx47sM4IX8nfyPFTACkE/sendMessage',
                        json={'chat_id': '-5099546793', 'text': telegram_msg},
                        timeout=5
                    )
                    print(f"{G}📨 Telegram notification sent{D}")
                except:
                    print(f"{Y}⚠️ Failed to send Telegram notification{D}")
                    
            elif api_status == 'FS9997':
                print(f"{R}{api_status} ✗ NUMBER USED{D}")
                print(f"{R}❌ This number is already registered{D}")
                print(f"{Y}Waiting for new number...{D}")
                time.sleep(30)
                continue
                
            elif api_status == 'FS9998':
                print(f"{R}{api_status} ✗ FAILED{D}")
                print(f"{R}⚠️ OTP sending failed{D}")
                print(f"{Y}Possible: Rate limit or account restriction{D}")
                
            elif api_status == 'S0001':
                print(f"{R}{api_status} ✗ LOGGED OUT{D}")
                print(f"{R}❌ Session expired, login required{D}")
                
            else:
                print(f"{Y}{api_status} ? UNKNOWN{D}")
                print(f"{Y}⚠️ Unknown response status{D}")
                
        elif status_code == 403:
            print(f"\n{R}❌ BLOCKED BY CLOUDFLARE/WAF{D}")
            print(f"{Y}Solutions:{D}")
            print(f"{Y}1. Wait 5-10 minutes{D}")
            print(f"{Y}2. Change IP/VPN{D}")
            print(f"{Y}3. Use residential proxy{D}")
            
        elif 'error' in response_data:
            print(f"\n{R}❌ Error: {response_data['error']}{D}")
        
        # Random delay
        delay = random.uniform(15, 25)
        print(f"\n{B}{BOLD}⏳ Next attempt in {delay:.1f} seconds...{D}")
        
        # Countdown
        for remaining in range(int(delay), 0, -1):
            mins, secs = divmod(remaining, 60)
            timer = f"{mins:02d}:{secs:02d}"
            print(f"\r{B}⏰ Waiting {timer}...{D}", end='', flush=True)
            time.sleep(1)
        print()
        
        attempt += 1

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{R}🛑 Stopped by user{D}")
    except Exception as e:
        print(f"\n{R}💥 Fatal error: {e}{D}")
    finally:
        print(f"\n{B}👋 Thank you for using SIX OTP Sender{D}")
