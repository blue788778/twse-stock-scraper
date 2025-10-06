import aiohttp
import certifi
import ssl
import logging

# 建立 aiohttp session（使用 SSL 驗證）
async def create_session():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    timeout = aiohttp.ClientTimeout(total=20)
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    return aiohttp.ClientSession(timeout=timeout, connector=connector)

# 建立 aiohttp session（禁用 SSL 驗證，用於 fallback）
async def create_insecure_session():
    timeout = aiohttp.ClientTimeout(total=20)
    connector = aiohttp.TCPConnector(ssl=False)
    return aiohttp.ClientSession(timeout=timeout, connector=connector)

# 非同步 fetch 函數（含 fallback 支援）
async def fetch(session, url, params, headers, fallback_disable_verify=True):
    try:
        async with session.get(url, params=params, headers=headers) as response:
            if response.status == 200:
                return await response.json()
            else:
                logging.error(f"API 回傳狀態碼: {response.status}")
                return None

    except aiohttp.ClientSSLError as e:
        logging.error(f"SSL 錯誤: {e}")

        if fallback_disable_verify:
            logging.warning("備援：嘗試使用非驗證 SSL 連線")
            async with await create_insecure_session() as insecure_session:
                try:
                    async with insecure_session.get(url, params=params, headers=headers) as response:
                        if response.status == 200:
                            return await response.json()
                        else:
                            logging.error(f"備援連線也失敗，狀態碼: {response.status}")
                            return None
                except Exception as fallback_error:
                    logging.error(f"備援請求仍失敗: {fallback_error}")
                    return None
        else:
            raise

    except aiohttp.ClientError as e:
        logging.error(f"請求錯誤: {e}")
        return None