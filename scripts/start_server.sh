#!/bin/bash
cd /home/ec2-user/nodejs-app
pm2 start index.js --name "nodejs-app"
pm2 save
pm2 startup
