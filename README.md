A youtube video, music downloader using python and yt-dlp

Test
```
cd .\src\backend
fastapi dev main.py
```
```
cd .\src\backend
uvicorn main:app --reload
```
Production
```
cd .\src\backend
fastapi run main.py
```
```
cd .\src\backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

Export requirements.txt
```
pip freeze | Out-File -Encoding UTF8 requirements.txt
```

Build and run docker image
```
docker build -t pydc .
docker run -d --name pydc-container -p 8000:8000 pydc
```
