import os
import logging

def save_data(df, directory, filename):
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, filename)
    if filename.endswith(".csv"):
        df.to_csv(filepath, index=False, encoding="utf-8-sig")
        logging.info(f"資料已儲存到 {filepath}")
    else:
        raise ValueError("只支援 .csv 副檔名")