#!/usr/bin/bash

sudo systemctl daemon-reload
sudo rm -f /etc/nginx/sites-enabled/default

sudo cp /home/ubuntu/autoproject/nginx/nginx.conf /etc/nginx/sites-available/autoproject
sudo ln -s /etc/nginx/sites-available/autoproject /etc/nginx/sites-enabled/

sudo gpasswd -a www-data ubuntu
sudo systemctl restart nginx