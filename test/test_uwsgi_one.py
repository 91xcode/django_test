#!/usr/bin/python
#coding=utf-8
import os
import sys
def application(environ, start_response):
        status = '200'
        output = 'this is a test for uwsgi,HOHO~'
        response_headers = [('Content-type', 'text/plain'),('Content-Length', str(len(output)))]
        start_response(status, response_headers)
        return output
