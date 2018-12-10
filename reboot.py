##### Huawei 4G Model reboot script using web API
##### Tested on model B310s-927
##### See resource.txt for links and API details
##### Use your own username, password and IP (baseurl variable) !!!



#!/usr/bin/env python

from __future__ import unicode_literals

import requests
import re
import hashlib
import base64
import os, sys


def login(baseurl, username, password):
    s = requests.Session()
    r = s.get(baseurl + "html/home.html") #sometimes it can be index.html, check webUI for the modem/router
    #print r.text
    csrf_tokens = grep_csrf(r.text)
    headers_update(s.headers, csrf_tokens[1])
    data = login_data(username, password, str(csrf_tokens[1]))
    r = s.request('POST', baseurl + "api/user/login", data=data)
    s.headers.update({'__RequestVerificationToken': r.headers["__requestverificationtokenone"]})
    print (r.text)
    return s

def headers_update(dictbase, token):
    dictbase['Accept-Language'] = 'en-US'
    dictbase['Content-Type'] = 'application/x-www-form-urlencoded'
    dictbase['X-Requested-With'] = 'XMLHttpRequest'
    dictbase['__RequestVerificationToken'] = token
    dictbase['Cache-Control'] = 'no-cache'
    dictbase['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 (KHTML, like Gecko) Version/8.0.8 Safari/600.8.9'
  
def grep_csrf(html):
    pat = re.compile(r".*meta name=\"csrf_token\" content=\"(.*)\"", re.I)
    matches = (pat.match(line) for line in html.splitlines())
    return [m.group(1) for m in matches if m]

def login_data(username, password, csrf_token):
    def encrypt(text):
        m = hashlib.sha256()
        m.update(text.encode("utf-8"))
        return base64.b64encode(m.hexdigest().encode("utf-8")).decode("utf-8")
    password_hash = encrypt(username + encrypt(password) + csrf_token)
    return '<?xml version "1.0" encoding="UTF-8"?><request><Username>%s</Username><Password>%s</Password><password_type>4</password_type></request>' % (username, password_hash)

def reboot(baseurl, session):
  r = s.post(baseurl + "api/device/control", data='<?xml version "1.0" encoding="UTF-8"?><request><Control>1</Control></request>')
  print (r.text)

#Change these usually they are 192.168.8.1, admin, admin
baseurl = "http://192.168.8.1/"
username = "admin"
password = "admin"

if __name__ == "__main__":
    print ("Trying to log in...")
    s = login(baseurl, username, password)
    print ("Logged !!")
    reboot(baseurl, s)
    print ("Rebooted !!")