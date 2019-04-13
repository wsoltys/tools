#!/usr/bin/python

import sys
import socket
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler

class MyHandler(SimpleHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/ip':
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()
      self.wfile.write('Your IP address is %s' % self.client_address[0])
      return
    else:
      return SimpleHTTPRequestHandler.do_GET(self)

  def do_POST(self):
      content_length = int(self.headers['Content-Length'])
      body = self.rfile.read(content_length)
      self.send_response(200)
      self.end_headers()
      self.wfile.write('ok')
      filename = self.path[1:]
      with open(filename, 'w') as f:
          f.write(body)
      return

  def do_PUT(self):
      MyHandler.do_POST(self)
      return

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6

def main():
  if len(sys.argv) > 1:
    port = int(sys.argv[1])
  else:
    port = 80  

  server = HTTPServerV6(('::', port), MyHandler)
  print('Serving http on '+server.server_name+' port '+str(server.server_port))
  print('Upload files with: curl -T <file> <server ip>')
  server.serve_forever()

if __name__ == '__main__':
  main()
