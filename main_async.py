import asyncio
import logging
import pandas as pd
from datetime import datetime, timedelta

from config_loader import load_config
from fetcher_async import fetch, create_session
from saver import save_data
from logger_setup import setup_logger

# 單檔股票資料抓取邏輯（加上 semaphore 與延遲控制）
async def fetch_stock_data(session, stock_no, handle_date, config, semaphore, need_delay=True):
    twse = config["twse"]
    headers = twse["headers"]
    output_dir = config["output_dir"]
    max_lookback_days = config.get("max_lookback_days", 10)

    async with semaphore:
        temp_date = handle_date
        for _ in range(max_lookback_days):
            date_str = temp_date.strftime("%Y%m%d")
            logging.info(f"嘗試抓取日期: {date_str}，股票: {stock_no}")

            params = {
                "response": twse["response"],
                "date": date_str,
                "stockNo": stock_no
            }

            try:
                response_json = await fetch(session, twse["base_url"], params, headers)
                if response_json and response_json.get("stat") == "OK":
                    data = response_json["data"]
                    fields = response_json["fields"]
                    df = pd.DataFrame(data, columns=fields)

                    filename = f"{stock_no}_{date_str}.csv"
                    save_data(df, output_dir, filename)
                    logging.info(f"[{stock_no}] 抓取成功 - 日期: {date_str}, 筆數: {len(df)}")

                    if need_delay:
                        await asyncio.sleep(2)
                    return
                else:
                    msg = response_json.get("stat", "未知錯誤")if response_json else "無回應"
                    logging.warning(f"{date_str} 無資料: {msg}，往前一天繼續...")
                    temp_date -= timedelta(days=1)
            except Exception as e:
                logging.error(f"{date_str} 抓取失敗 [{stock_no}]，原因: {e}")
                temp_date -= timedelta(days=1)

        logging.error(f"超過 {max_lookback_days} 天仍未找到 {stock_no} 的有效資料")

        # 最後也延遲一下（為了避免錯誤後沒有休息）
        if need_delay:
            await asyncio.sleep(2)

# 主流程
async def main_async():
    handle_date = datetime.today()
    setup_logger(log_filename=handle_date.strftime("%Y%m%d"))

    config = load_config("config.json")
    stock_nos = config["twse"]["stock_nos"]
    max_concurrent_tasks = config.get("max_concurrent_tasks", 3)

    semaphore = asyncio.Semaphore(max_concurrent_tasks)

    async with await create_session() as session:
        tasks = [
            fetch_stock_data(
                session,
                stock_no,
                handle_date,
                config,
                semaphore,
                need_delay=(idx < len(stock_nos) - 1)   # 不是最後一支才延遲
            )
            for idx, stock_no in enumerate(stock_nos)
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main_async())