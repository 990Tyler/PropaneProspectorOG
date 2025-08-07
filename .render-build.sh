#!/usr/bin/env bash

# Update package list
apt-get update

# Install Chromium and Chromedriver
apt-get install -y chromium-browser chromium-driver

# Permissions (just in case)
chmod +x /usr/bin/chromium-browser
chmod +x /usr/lib/chromium-browser/chromedriver
