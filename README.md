# TWSE 台股個股爬蟲工具（Python）

本專案是一個用 Python 撰寫的自動化爬蟲，用來抓取台灣證券交易所（TWSE）的每日個股交易資料。支援多檔股票、日期回退重試、自動儲存為 CSV、log 記錄與模組化設計。

---

## 專案功能

- 擷取台股個股每日交易資料（開盤/收盤/成交量等）
- 支援多支股票代碼
- 若當日無資料自動往前找資料（假日或無成交）
- 模組化拆分，便於維護與擴充
- 儲存為 UTF-8 編碼 `.csv` 檔
- 詳細日誌記錄（logs/）

---

## 專案結構

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

---

## 安裝套件

請先安裝必要依賴：

```bash
pip install -r requirements.txt