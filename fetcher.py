import requests
import certifi
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session(max_retries=5):
    s = requests.Session()
    retries = Retry(total=max_retries, backoff_factor=0.5, status_forcelist=(429, 500, 502, 503, 504))
    s.mount("https://", HTTPAdapter(max_retries=retries))
    return s

def fetch(url, params, headers, use_certifi=True, fallback_disable_verify=True, max_retries=5):
    s = create_session(max_retries=max_retries)
    try:
        if use_certifi:
            r = s.get(url, params=params, headers=headers, timeout=15, verify=certifi.where())
        else:
            r = s.get(url, params=params, headers=headers, timeout=15)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.SSLError as e:
        logging.error(f"SSL error: {e}")
        if fallback_disable_verify:
            logging.warning("嘗試備援：暫時跳過 SSL 驗證（僅建議測試用）")
            r = s.get(url, params=params, headers=headers, timeout=15, verify=False)
            r.raise_for_status()
            return r.json()
        raise
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        raise