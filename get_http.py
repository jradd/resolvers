"""works in 3.7"""
from ssl import SSLContext, PROTOCOL_TLSv1_2, create_connection
from socket import AF_INET,getaddrinfo
from os.path import exists, abspath, join, curdir, getmtime

def http_get(url, port=443):
       _, _, hostname, path = url.split('/', 3)
       print(hostname, path)
       addr = getaddrinfo(str(hostname), port)[-1][-1]
       filename = path.split('/')[-1]
       print('saving to: %s' % filename)
       if exists(abspath(join(curdir, filename))):
         filename = str(getmtime(filename)) + '_' + filename

       context = SSLContext(PROTOCOL_TLSv1_2)
       with create_connection(addr) as conn_sock:
           with context.wrap_socket(conn_sock, server_hostname=hostname) as ssock:
               print(ssock.version())
               ssock.sendall(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, hostname), 'utf8'))
               data = ssock.recv(1024)
               with open(filename, 'wb') as f:
                   while True:
                       data = ssock.recv(1024)
                       if data:
                           f.write(bytes(str(data), encoding='utf8', errors='ignore'))
                       else:
                           break
               fh = open(filename, 'r').read()
           return fh
       fh.close()


if __name__ == '__main__':
  from sys import argv
  http_get(argv[1])
