# 顧晉瑋 Python 網站專案

這是一個綜合前端、後端、資料庫、雲端部署與網路爬蟲的整合專案，適用於 macOS 環境。

## 功能介紹

- 前端網頁設計：使用HTML、CSS和Bootstrap實現響應式設計
- 後端開發：使用Flask框架處理HTTP請求和路由
- 資料庫整合：使用Firebase Firestore儲存資料
- 網路爬蟲：爬取開眼電影網的電影資料並存入Firebase
- 雲端部署：支援Vercel部署

## 安裝與設定

### 環境需求

- Python 3
- pip
- Git
- Firebase帳號 (用於資料庫功能)

### 安裝步驟

1. 安裝必要套件:

```
pip install -r requirements.txt
```

2. Firebase設定:
   - 在Firebase Console建立專案
   - 下載serviceAccountKey.json並放在專案的credentials資料夾中（需先建立此資料夾）
   - 或在部署時設置環境變數FIREBASE_KEY

## 使用方式

### 本地運行

```
python index.py
```

預設訪問: http://127.0.0.1:5000/

### 爬取電影資料

```
python spider.py
```

### Firebase操作示例

- 新增資料: `python create.py`
- 讀取資料: `python read.py` 
- 更新資料: `python update.py`
- 刪除資料: `python delete.py`

## 專案結構

```
mis/
  ├─ index.py        # 主程式
  ├─ spider.py       # 網路爬蟲程式
  ├─ create.py       # Firebase新增資料示例
  ├─ read.py         # Firebase讀取資料示例
  ├─ update.py       # Firebase更新資料示例
  ├─ delete.py       # Firebase刪除資料示例
  ├─ requirements.txt # 依賴套件
  ├─ credentials/    # 存放認證文件
  │    └─ serviceAccountKey.json # Firebase服務帳戶金鑰
  ├─ templates/      # 放置各種HTML模板
  │    ├─ about.html
  │    ├─ today.html
  │    ├─ welcome.html
  │    ├─ account.html
  │    └─ movies.html
  └─ vercel.json     # Vercel部署設定
```

## 雲端部署

專案已配置好Vercel部署，請設置以下環境變數：

- FIREBASE_KEY: Firebase服務帳戶金鑰 (JSON格式)

## 作者

顧晉瑋
