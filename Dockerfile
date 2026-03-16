FROM selenium/standalone-chrome
WORKDIR /usr/local/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

RUN ["python3", "main.py"]

