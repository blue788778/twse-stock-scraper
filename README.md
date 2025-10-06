# TWSE 台股個股爬蟲工具（Python）

本專案是一個使用 Python 撰寫的自動化爬蟲工具，用來擷取台灣證券交易所（TWSE）的每日個股交易資料。支援同步與非同步模式、併發控制、自動錯誤處理與 CSV 儲存格式，適合用於金融資料分析、後續自動化處理等場景。

---

## 專案功能

- 擷取台股個股每日交易資料（開盤/收盤/成交量等）
- 支援多支股票代碼（由 `config.json` 設定）
- 自動處理休市日 / 無成交日，往前找最近有效資料
- 支援同步 (`requests`) 與非同步 (`aiohttp`) 兩種抓取模式
- 使用 Retry 機制 + 併發限制，避免 API 被擋或過度請求
- 資料儲存為 UTF-8 BOM 編碼 `.csv`，可直接開啟於 Excel
- 詳細日誌自動儲存於 `logs/` 資料夾，方便追蹤錯誤與執行情況
- 模組化程式架構，便於維護與擴充

---

## 專案結構

```text
twse_stock_scraper/
├── main.py              # 同步版主流程（適合少量股票或初學者）
├── main_async.py        # 非同步版主流程（支援併發與大量股票）
├── config_loader.py     # 讀取 JSON 設定檔
├── fetcher.py           # 同步資料抓取（requests）
├── fetcher_async.py     # 非同步資料抓取（aiohttp）
├── saver.py             # 儲存 DataFrame 成 CSV
├── logger_setup.py      # 日誌設定
├── config.json          # 設定檔（股票代碼/網址/headers 等）
├── requirements.txt     # 套件清單
├── README.md            # 本文件
└── logs/                # 執行產生的日誌檔案
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
  "concurrent_limit": 3,   // 非同步模式下的最大同時請求數
  "max_lookback_days": 10
}
```

| 參數名稱                | 說明                                         |
| ------------------- | ------------------------------------------ |
| `twse.base_url`     | TWSE 公開 API 網址（固定為 `STOCK_DAY`）            |
| `twse.response`     | API 回傳格式（目前僅支援 `"json"`）                   |
| `twse.stock_nos`    | 要查詢的股票代碼清單（如 `"2330"` 為台積電）                |
| `twse.headers`      | HTTP 請求標頭，建議提供 `User-Agent` 避免被阻擋          |
| `output_dir`        | 資料儲存資料夾名稱（如 `data`，程式會自動建立）                |
| `max_retries`       | 單次請求的最大重試次數（網路錯誤、API timeout 等情況）          |
| `concurrent_limit`  | 非同步模式下的最大併發數量，用來避免 API 被擋或主機資源過載（預設建議：3） |
| `max_lookback_days` | 若當日無資料（如假日、無成交），最多往前幾天尋找最近一筆有效資料           |

---

## 執行方式

同步模式（適合少量股票）
```bash
python main.py
```
每支股票會依序抓資料，過程中有 2 秒間隔避免頻繁請求
適合用於測試或查詢少量股票

非同步模式（支援大量股票＋併發控制）
```bash
python main_async.py
```
支援併發查詢多檔股票，速度較快
會自動根據 config.json 中 concurrent_limit 控制同時最大請求數
使用 asyncio + aiohttp 架構，效率佳且穩定

---

## 資料輸出

所有成功抓取的資料將儲存在 data/ 資料夾中
檔名格式為：[股票代碼]_[日期].csv 例如：2330_20251006.csv
使用 UTF-8 編碼（含 BOM），可直接用 Excel 開啟

---

## 日誌紀錄

每次執行會產生一個對應日期的 log 檔，例如：logs/20251006.log
包含每支股票的抓取狀態、失敗訊息與錯誤堆疊
方便後續問題追蹤與錯誤分析

---

## 注意事項

台股休市日（週末、假日）或股票當日無成交，API 會回傳 stat != OK
程式會自動向前找資料，直到找到資料或超過 max_lookback_days
資料來源為 TWSE 官網，請勿過於頻繁呼叫、建議保守設定 concurrent_limit，避免遭 TWSE 封鎖 IP