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

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb \
    && apt-get -f install -y

# Install ChromeDriver
RUN LATEST_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget https://chromedriver.storage.googleapis.com/${LATEST_VERSION}/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/chromedriver \
    && chmod +x /usr/local/bin/chromedriver

RUN useradd -m ubuntu

RUN chown ubuntu:ubuntu /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver

# RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
#     apt-get -y update && \
#     apt-get -y install google-chrome-stable && \
#     rm -rf /var/lib/apt/lists/*

RUN chmod 777 /autoproject

RUN chown -R ubuntu:ubuntu /autoproject

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
