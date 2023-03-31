# 使用 Flask API 創建基於 GCF 與 GCP DB 的 Linebot
這是一個使用 Flask 作為 API 創建 Linebot 的 Python 程序範例，並部署在 Google Cloud Functions（GCF）上，連接到 Google Cloud Platform（GCP）數據庫。

## 先決條件
在開始之前，您需要以下東西：

Line Messaging API 開發者帳戶
已啟用計費的 GCP 項目
已部署的 Google Cloud Functions
Google Cloud SQL 實例
Python 3.5 或更高版本
安裝了 functions-framework 和 Flask 库

將此存儲庫克隆到本地計算機上
創建一個新的虛擬環境並激活它
通過運行以下命令安裝所需的庫：


`pip install functions-framework Flask pymysql line-bot-sdk`

打開 main.py 文件，在適當的位置填寫必要的細節（API 密鑰、webhook、數據庫憑證等）
通過運行以下命令將函數部署到 GCF：


gcloud functions deploy [FUNCTION_NAME] --runtime python38 --trigger-http --allow-unauthenticated
將 [FUNCTION_NAME] 替換為您喜歡的函數名稱。
## 用法
要使用 Linebot，只需在 Line Messaging 應用程序中添加它為好友，然後發送消息。機器人應該會回復由 main.py 文件中的 bot_speaking() 函数生成的消息。

## 故障排除
如果機器人未回應消息，請檢查 Line webhook 是否正確配置，以及 GCF 函數是否已部署並可訪問。
如果存在與數據庫連接有關的問題，請仔細檢查數據庫憑證，並確保 Cloud SQL 實例已正確配置並可訪問。
