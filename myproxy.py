
from socket import *
import requests as request
from socket import *
import  socket,select
import sys
import _thread
import struct
import dns
import dns.resolver
import requests as request


#import dns
#import dns.resolver
serverSocket = socket.socket(AF_INET, SOCK_DGRAM)

DNS_Cache = []
HTTP_cache = []
global inCache
fragment_size=50
check = ['\\', '\\n', '\n', 'n', '\'', '\\t', '\t', 't', 'xa0', 'xc2']

global received,host
def checksum(str1):
    c = 0
    for i in str1:
        if i not in check:
            c = c + ord(i)

    cs = bin(c)
    d=""
    cs = cs.split('b')
    #print("my:"+str(cs[1]))
    return cs[1]

def iscorrect(str,cstr):
    if (checksum(str) + "'" == cstr) or (checksum(str) + "\"" == cstr) or (checksum(str) + "\'" == cstr):
        return 1
    else:
        return 0
def fragment_and_send (message,cadd):

    MF=0
    if(int(len(message) % fragment_size)==0):
        numberoffrags=int(len(message) / fragment_size)
    else:
        numberoffrags = int(len(message) / fragment_size) + 1
    for x in range (0 ,numberoffrags) :
        if(x==numberoffrags-1):
            MF=1
        else:
            MF=0

        start = x * fragment_size
        end = (x + 1) * fragment_size

        print("----------")
        #print(str(message[start:end]))
        f=1;

        while(f==1):
            serverSocket1 = socket.socket(AF_INET, SOCK_DGRAM)
            FragmentedMESSAGE =  str(x) + '*|' + message[start:end] +'*|'+str(MF)+'*|'+checksum(message[start:end])
            print("send packet : "+ FragmentedMESSAGE )


            #while (f == 1):
            serverSocket1.sendto(bytes(FragmentedMESSAGE,"utf-8") ,cadd)
            #serverSocket1.close()

            ack_socket = socket.socket(AF_INET, SOCK_DGRAM)
            ack_socket.bind(('127.0.0.1', 5100))
            ack_mes, hgh = ack_socket.recvfrom(1000)
            res=str(ack_mes).split('\'')
            res1=res[1]
            print(str(x))
            print(str(res1))
            print("ack")
            if (str(x)==res1):
                f=0;
                print("equal")

            #ack_socket.close()



def recieve(serverName,rproxy_port):
    rproxy_port = 5101
    serverName='127.0.0.1'
    x=0
    received=""

    serverSocket.bind((serverName, rproxy_port))
    print ("The server is ready to receive")
    while 1:
        message, clientAddress = serverSocket.recvfrom(1000)
        REC=str(message).split('*|')
        #print(REC)
        var=REC[0].split('\'')
        var2 = REC[0].split('\"')

        try:
            if "b\'"+str(x)==REC[0] or  "b\""+str(x)==REC[0]:

                if(iscorrect(REC[1],REC[4])):

                    received=received + REC[1]
                    print("appended is : " + received)
                    x=x+1
                else:
                    print("message had problem ")
        except IndexError as e:
            print('sorry, no 5')
            if x==int(var2[1]) :

                if(iscorrect(REC[1],REC[4])):

                    received=received + REC[1]
                    print("appended is : " + received)
                    x=x+1
                else:
                    print("message had problem ")


        if(REC[3]=="1"):
            completed=1
        else:
            completed=0
        if(completed==1):
            host=REC[2]
            #print(host)
            #injaaaa
            result=server_Connection(host)
            print("completed")
            #result="ggggg"


            fragment_and_send(result,clientAddress)


        print("responsed")
        print("---------")

def UDP_Connection(query):

    global reply
    reply = ''
    global inCache
    inCache = 0
    for i in DNS_Cache:
        if i[0] == query:
            print('Is in cache')
            reply += i[1]
            print(i[1])
            inCache = 1

    queryS = str(query).split('#')
    type = queryS[0]
    server = queryS[1]
    target = queryS[2]
    #global reply


    if inCache==0:
        query1 = dns.message.make_query(target, 'A')
        try:
            print("here")
            query2 = dns.query.udp(query1, server, timeout=4)
            if query2.flags & dns.flags.AA == 1024:
                reply += "DNS Server is Authoritative | "
                print('Authoritative')
            else:
                reply += "DNS Server is Non Authoritative | "
                print('Non Authoritative')
        except dns.exception.Timeout:
            print('error')

        print(target[0:-1])
        print(type[2:])
        print(server)


        try:
            q = dns.resolver.query(target[0:-1], type[2:])
            for i in q:

                if type[2:] == 'A':
                    #print("###A")
                    print(i.address)
                    reply += "Type: A | Address: "+i.address + " "
                if type[2:] == 'CNAME':
                    #print("###CNAME")
                    print(i.target)
                    reply += "Type: CNAME | Target: " + str(i.target) + " "
        except dns.exception.Timeout:
            print('Timeout')
        except dns.resolver.NoAnswer:
            print('NoAnswer')
            conn.close()

        if len(DNS_Cache) == 20:
            DNS_Cache.pop(0)
        DNS_Cache.append((query, reply))
        inCache = 0

        #print("---"+ reply)



def server_Connection(URL):
    #host='www.google.com'
    global http_rep
    #global isinCache
    inCache = 0
    for i in HTTP_cache:
        if i[0] == URL:
            print("Is in cache")
            return i[1]
    print("-----")
    http_rep = request.request(method='GET', url='http://'+ URL, allow_redirects=False)
    status = http_rep.status_code
    #print(http_rep.text)

    #if int(status)==200:
    print(status)



    while int(status) == 301 or int(status) == 302 :
        print("Redirected")
        redirect = http_rep.headers['Location']
        http_rep = request.request(method='GET', url=redirect, allow_redirects=False)
        status = http_rep.status_code

    if int(status) == 404:
        #http_rep="Error 404 Not Found"
        if len(HTTP_cache) == 20:
            HTTP_cache.pop(0)
        HTTP_cache.append(("URL", "Error 404 Bad Request"))
        return "Error 404 Bad Request"


    if int(status) == 400:
        #http_rep="Error 400 Bad Request"
        if len(HTTP_cache) == 20:
            HTTP_cache.pop(0)
        HTTP_cache.append(("URL", "Error 400 Bad Request"))
        return "Error 404 Bad Request"

    # file = open("page.html", 'wb')
    # file.write(http_rep.text.encode('UTF-8'))

    if len(HTTP_cache) == 20:
        HTTP_cache.pop(0)
    HTTP_cache.append((URL, http_rep.text))
    return http_rep.text











    # serverName = '127.0.0.1'
    # serverPort = 5010
    # clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # clientSocket.bind((serverName, serverPort))
    # clientSocket.listen(1)
    #
    # while True:
    #     conn, addr = clientSocket.accept()
    #     query = conn.recv(1024)
    #         # if not data: break
    #         # print(addr)
    #     if query:
    #         print("Received Query:", query)
    #         UDP_Connection(query)
    #     global reply
    #     r = bytes(reply, 'utf-8')
    #     conn.send(r)
    # conn.close()



if __name__ == '__main__':

    while True:
        sel = input('Enter : \n')
        sel = sel.split(' ')
        s = ''
        d = ''
        if sel[0] == "proxy":
            sel1 = sel[1].split(':')
            sel10 = sel1[0].split('=')
            print(sel10[1])
            s = sel10[1]
            # if sel10[0]=="-s":
            #     print (sel10[1])
            print(sel1[1])
            serverName = sel1[1]
            print(sel1[2])
            serverPort = sel1[2]
            sel2 = sel[2].split('=')
            print(sel2[1])
            d = sel2[1]

        #proxy –s=tcp:127.0.0.1:80 –d=udp
        if s == "tcp" and d == "udp":
            serverName = '127.0.0.1'
            serverPort = 5010
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.bind((serverName, serverPort))
            clientSocket.listen(1)

            while True:
                conn, addr = clientSocket.accept()
                query = conn.recv(1024)
                # if not data: break
                # print(addr)
                if query:
                    print("Query:", query)
                    UDP_Connection(query)
                global reply
                r = bytes(reply, 'utf-8')
                conn.send(r)
            conn.close()

        elif s == "udp" and d == "tcp":

            recieve(serverName,serverPort)

        else:
            print("Unvalid")

