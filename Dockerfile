FROM python:3.10.7-slim

COPY ["./requirements.txt", "/ws/"]
COPY ["./src/", "/ws/src/"]

WORKDIR "/ws"
RUN [\
  "python", "-m", "pip", "install", \
  "--no-cache-dir", "--upgrade", "-r", "requirements.txt"\
]

EXPOSE 3001
WORKDIR "/ws/src/fastapi_app"
CMD ["python", "main.py"]
