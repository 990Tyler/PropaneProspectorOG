#!/usr/bin/env bash

# Install Chromium
apt-get update
apt-get install -y chromium-browser chromium-driver

# Give execution permission to Chrome and chromedriver
chmod +x /usr/bin/chromium-browser
chmod +x /usr/lib/chromium-browser/chromedriver
