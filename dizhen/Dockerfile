FROM docker.xuanyuan.me/python:3.13.3-slim-bookworm
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "python","app.py" ]