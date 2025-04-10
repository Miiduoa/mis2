# Vercel 部署指南

本文件提供將 Flask 應用部署到 Vercel 的步驟指南。

## 部署前準備

1. **確保專案結構正確**：
   - 主要 Flask 應用在 `index.py`
   - 建立 `api/index.py` 作為 Vercel 的入口點
   - 確保 `vercel.json` 正確配置

2. **Firebase 認證設置**：
   為安全起見，不要將 `serviceAccountKey.json` 上傳到 Vercel。相反，請將其內容設置為環境變數。

## 部署步驟

1. **安裝 Vercel CLI** (如果尚未安裝)：
   ```bash
   npm i -g vercel
   ```

2. **登入 Vercel**：
   ```bash
   vercel login
   ```

3. **設定 Firebase 環境變數**：
   在 Vercel 控制台中，為你的專案設置以下環境變數：
   - 名稱: `FIREBASE_SERVICE_ACCOUNT`
   - 值: 複製 `serviceAccountKey.json` 的全部內容

   或使用 CLI：
   ```bash
   vercel env add FIREBASE_SERVICE_ACCOUNT
   ```
   然後貼上 JSON 內容。

4. **部署專案**：
   在專案根目錄執行：
   ```bash
   vercel
   ```
   或直接從 GitHub 部署：
   1. 將程式碼推送到 GitHub
   2. 在 Vercel 控制台中導入專案
   3. 設置環境變數
   4. 部署

## 測試部署

1. 部署完成後，測試以下路由是否正常工作：
   - 首頁: `/`
   - 學生資料: `/read`
   - 電影資訊: `/movie`

2. 如果遇到問題，檢查 Vercel 日誌以獲取詳細錯誤訊息。

## 常見問題排除

1. **404 錯誤**：
   - 確保 `vercel.json` 中的路由設定正確
   - 檢查 `api/index.py` 是否正確導入主應用

2. **Firebase 錯誤**：
   - 確認環境變數已正確設置
   - 檢查日誌中是否有身份驗證錯誤

3. **靜態檔案無法加載**：
   - 確保 `vercel.json` 中有正確配置靜態檔案路由

## 注意事項

1. 免費版 Vercel 有一些限制，例如最大部署大小和執行時間限制。
2. Firebase 請求可能會被計入您的 Firebase 配額。
3. 若網站長時間未訪問，Vercel 可能會使實例休眠，導致初次訪問較慢。 