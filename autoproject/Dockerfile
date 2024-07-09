FROM python:3.9

WORKDIR /autoproject
COPY . /autoproject
RUN pip3 install -r /autoproject/requirements.txt

RUN apt-get -y update && \
    apt-get install -y \
    zip \
    unzip \
    wget \
    curl \
    gnupg && \
    rm -rf /var/lib/apt/lists/*

RUN wget -N https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -P /tmp/ && \
    unzip /tmp/chromedriver_linux64.zip -d /tmp/ && \
    mv /tmp/chromedriver /usr/local/bin/chromedriver && \
    rm /tmp/chromedriver_linux64.zip

RUN useradd -m ubuntu

RUN chown ubuntu:ubuntu /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -y update && \
    apt-get -y install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 777 /autoproject

RUN chown -R ubuntu:ubuntu /autoproject

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
