A youtube video, music downloader using python and yt-dlp
Python 3.14.5 is required

Export requirements.txt

```
pip freeze > requirements.txt
```

Run server

```
cd src
fastapi dev run_server.py
```

Build and run docker image

```
docker build -t pydc .
docker run -d --name pydc-container -p 8000:8000 pydc
```
