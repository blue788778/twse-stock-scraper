from datetime import datetime, timedelta
import time
import logging
import pandas as pd

from config_loader import load_config
from fetcher import fetch
from saver import save_data
from logger_setup import setup_logger

def main(handle_date):
    config = load_config("config.json")
    twse = config["twse"]
    headers = twse["headers"]
    stock_nos = twse["stock_nos"]
    output_dir = config["output_dir"]
    max_retries = config.get("max_retries", 5)
    max_lookback_days = config.get("max_lookback_days", 10)

    for stock_no in stock_nos:
        temp_date = handle_date   # 每檔獨立的日期控制
        for _ in range(max_lookback_days):
            date_str = temp_date.strftime("%Y%m%d")
            logging.info(f"嘗試抓取日期: {date_str}，股票: {stock_no}")

            params = {
                "response": twse["response"],
                "date": date_str,
                "stockNo": stock_no
            }

            try:
                response_json = fetch(twse["base_url"], params, headers, max_retries=max_retries)

                if response_json.get("stat") == "OK":
                    data = response_json["data"]
                    fields = response_json["fields"]
                    df = pd.DataFrame(data, columns=fields)

                    filename = f"{stock_no}_{date_str}.csv"
                    save_data(df, output_dir, filename)
                    break
                else:
                    logging.warning(f"{date_str} 無有效資料，往前一天繼續...")
                    temp_date -= timedelta(days=1)
            except Exception as e:
                logging.error(f"{date_str} 抓取失敗，原因: {e}")
                temp_date -= timedelta(days=1)
            finally: 
                time.sleep(2)   # 等待 2 秒，避免過度呼叫
        else:
            logging.error(f"超過 {max_lookback_days} 天仍未找到 {stock_no} 的有效資料")

if __name__ == "__main__":
    date_today = datetime.today()
    setup_logger(log_filename=date_today.strftime("%Y%m%d"))
    main(date_today)