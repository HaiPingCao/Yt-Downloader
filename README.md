A youtube video, music downloader using python and yt-dlp

Export requirements.txt

```
pip freeze
```

Run server

```
cd src
fastapi dev transport.py
```

Build and run docker image

```
docker build -t pydc .
docker run -d --name pydc-container -p 8000:8000 pydc
```
