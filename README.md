# TWSE 台股個股爬蟲工具（Python）

本專案是一個用 Python 撰寫的自動化爬蟲，用來抓取台灣證券交易所（TWSE）的每日個股交易資料。支援多檔股票、日期回退重試、自動儲存為 CSV、log 記錄與模組化設計。

---

## 專案功能

- 擷取台股個股每日交易資料（如開盤價、收盤價、成交量等）
- 支援多支股票代碼
- 當日無資料（假日或無成交）時，會自動往前查找直到找到有效資料
- 模組化拆分（fetcher / saver / config / logger），方便維護擴充
- 自動儲存為 `.csv`（UTF-8 編碼含 BOM）
- 日誌記錄功能：每次執行會產出 logs 檔案

---

## 專案結構

```text
twse_stock_scraper/
├── main.py # 主流程，進入點
├── config_loader.py # 讀取 JSON 設定檔
├── fetcher.py # 處理 API 資料抓取
├── saver.py # 儲存 DataFrame 成 CSV
├── logger_setup.py # 日誌設定
├── config.json # 設定檔（股票代碼/網址/headers）
├── requirements.txt # 套件清單
├── README.md # 本文件
└── logs/ # 執行產生的 log 檔案
```

---

## 安裝套件

請先安裝必要依賴：

```bash
pip install -r requirements.txt
```

---

## 設定檔 `config.json`

```json
{
  "twse": {
    "base_url": "https://www.twse.com.tw/exchangeReport/STOCK_DAY",
    "response": "json",
    "stock_nos": ["2330", "2317", "0050"],
    "headers": {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
  },
  "output_dir": "data",
  "max_retries": 5,
  "max_lookback_days": 10
}
```

| 參數名稱                | 說明                                |
| ------------------- | --------------------------------- |
| `twse.base_url`     | TWSE 公開 API 的網址（固定為 `STOCK_DAY`）  |
| `twse.response`     | API 回傳格式（目前只支援 `"json"`）          |
| `twse.stock_nos`    | 要查詢的股票代碼清單（如 `"2330"` 為台積電）       |
| `twse.headers`      | HTTP 請求標頭，建議加上 `User-Agent` 避免被擋  |
| `output_dir`        | 資料輸出的資料夾名稱（如 `data`，程式會自動建立）      |
| `max_retries`       | 單次請求的重試次數，適用於網路錯誤、API timeout 等情況 |
| `max_lookback_days` | 若當日無資料（如假日、無成交），最多往前回溯幾天繼續嘗試抓資料   |

---

## 執行方式

```bash
python main.py

- 程式會抓取設定檔中所有股票代碼的最近有效交易日資料。
- 資料將存入 data/ 資料夾。
- Log 檔會存入 logs/，檔名為當天日期，例如：logs/20251005.log
```

---

## 注意事項

- 台股休市日（週末、假日）或股票當日無成交，API 會回傳 stat != OK
- 程式會自動向前找資料，直到找到資料或超過 max_lookback_days
- 資料來源為 TWSE 官網，請勿過於頻繁呼叫，以免被封鎖
- 儲存格式為 CSV，使用 UTF-8 編碼（含 BOM），可直接開啟於 Excel