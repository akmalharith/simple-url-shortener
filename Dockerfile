FROM python:3.9
LABEL maintainer="Akmal Harith"
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY . . 
CMD [ "python3", "./app.py" ]
