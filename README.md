# README.md

# My Flask App

這是一個使用 Flask 框架構建的簡單應用程式。

## 專案結構

```
my-flask-app
├── app
│   ├── __init__.py      # Flask 應用程式的初始化檔
│   ├── routes.py        # 定義應用程式的路由
│   └── templates
│       └── index.html   # 應用程式的 HTML 模板
├── Dockerfile            # 構建 Flask 應用的 Docker 映像
├── requirements.txt      # 列出所需的 Python 依賴包
└── README.md             # 專案文檔
```

## 安裝與運行

1. 確保已安裝 Docker 和 Docker Compose。
2. 在專案根目錄下，使用以下命令構建 Docker 映像：

   ```
   docker-compose build
   ```

3. 使用以下命令啟動應用程式：

   ```
   docker-compose up
   ```

4. 打開瀏覽器，訪問 `http://localhost:8000` 查看應用程式。

## 依賴

請參考 `requirements.txt` 檔案以獲取所需的 Python 依賴包。