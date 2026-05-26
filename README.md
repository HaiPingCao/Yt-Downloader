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

Run the dispatcher gRPC server

```
segment-grpc-server --host "[::]" --port 50051
```

Run the test client

```
segment-grpc-client "https://www.youtube.com/watch?v=VIDEO_ID" --target localhost:50051
```

For JSONL output from the client

```
segment-grpc-client "https://www.youtube.com/watch?v=VIDEO_ID" --jsonl
```
