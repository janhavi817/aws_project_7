#!/bin/bash
isExistApp=$(pm2 list | grep -o "nodejs-app")
if [ -n "$isExistApp" ]; then
    pm2 stop nodejs-app
    pm2 delete nodejs-app
fi
