A youtube video, music downloader using python and yt-dlp

Export requirements.txt

```
pip freeze | Out-File -Encoding UTF8 requirements.txt
```

Build and run docker image

```
docker build -t pydc .
docker run -d --name pydc-container -p 8000:8000 pydc
```
