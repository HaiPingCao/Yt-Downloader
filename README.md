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
docker build -t yt-link-extractor-server .
docker run -d --name yels-container -p 8000:8000 yt-link-extractor-server
```

Connect to WS

```
ws://localhost:8000/ws/music
```

Payload

```
{
    "url":"str",
    "start_index":int,
    "end_index":int
}
```
