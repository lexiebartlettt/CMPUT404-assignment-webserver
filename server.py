#  coding: utf-8 
import SocketServer
import mimetypes
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    

    def handle(self):
        
        #Set up and split the data to get the URL
        self.data = self.request.recv(1024).strip()
        self.split_data = self.data.split()
        self.url_start = 'www'

        try: 
            #Default case
            if (self.split_data[1]=='/'): 
                self.split_data[1] = '/index.html'
     
            #Deals with html files
            if ("html" in self.split_data[1]): 
                url = self.split_data[1]
                url = self.url_start + url
                print (url)
                file_handler = open(url,'rb')
                response_content = file_handler.read()
                file_handler.close()

                self.request.send('HTTP/1.1 200 OK\nContent-Type: text/html\n\n')
                self.request.send(response_content)

            #deals with CSS files
            elif ("css" in self.data):
                url = self.split_data[1]
                url = self.url_start + url
                print (url)
                file_handler = open(url,'rb')
                response_content = file_handler.read()
                file_handler.close()

                self.request.send('HTTP/1.1 200 OK\nContent-Type: text/css\n\n')
                self.request.send(response_content)

            #deals with files that haven't been found
            else:
                self.request.send('"HTTP/1.1 404 NOT FOUND\r\n')

        except IOError: 
            self.request.send('"HTTP/1.1 404 NOT FOUND\r\n')
        except IndexError: 
            print("This got thrown again and I don't know what to do about it")

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
