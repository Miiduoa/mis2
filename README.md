# 資訊管理課程專案

這是一個整合 Flask、Firebase、網路爬蟲和 Vercel 部署的完整資訊系統。

## 功能特色

- 響應式前端設計（使用 Bootstrap）
- Flask 動態網頁架構
- Firebase Firestore 資料庫整合
- 爬蟲自動獲取電影資訊
- Vercel 雲端部署

## 安裝與設置

1. 安裝所需套件：`pip install -r requirements.txt`
2. 設置 Firebase 認證
3. 本地執行：`python web.py`
4. 部署到 Vercel

## 專案結構說明

- `app.py`: 主要應用邏輯
- `spider.py`: 爬蟲功能
- `templates/`: 頁面模板
- `static/`: 靜態資源

## 學習資源

- [Flask 文件](https://flask.palletsprojects.com/)
- [Firebase 文件](https://firebase.google.com/docs)
- [Vercel 部署指南](https://vercel.com/docs)

## 專案資訊
- 學號：411211325
- 姓名：顧晉瑋
- 課程：資訊管理導論
- 授課教師：楊子青

## 說明
這是資訊管理系統的靜態展示版本，適合在 Vercel 上部署。

原始專案是基於 Flask 和 Firebase 的完整應用程式，由於部署平台限制，此版本僅提供靜態界面展示，不包含後端功能。

## 功能展示
- 使用者管理
- 文章系統
- 統計分析
- 電影資料 (網路爬蟲演示)

## 注意事項
- 登入帳號：admin@example.com
- 登入密碼：admin123 

# Vercel 部署詳細步驟

1. **準備部署檔案**
   - 確保 index.py, app.py, vercel.json 和 requirements.txt 都已正確設置
   - 確保 templates 和 static 文件夾結構正確

2. **設置 Firebase 憑證**
   - 從 Firebase 控制台下載 serviceAccountKey.json
   - 使用 vercel CLI 或網頁界面設置環境變數

3. **部署步驟**
   ```bash
   # 安裝 Vercel CLI
   npm install -g vercel
   
   # 登入
   vercel login
   
   # 設置 Firebase 憑證
   vercel secrets add firebase-credentials "$(cat serviceAccountKey.json)"
   
   # 部署
   vercel
   ```

4. **部署後檢查**
   - 訪問部署的 URL 確認應用正常運行
   - 查看 Vercel 日誌確認沒有錯誤
   - 測試各項功能是否正常 