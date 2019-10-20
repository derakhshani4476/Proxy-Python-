from socket import *


#http module
sproxy_ip = "127.0.0.1"
sclient_port=5100
sproxy_port = 5101
fragment_size =50
send_socket = socket(AF_INET, SOCK_DGRAM)
check = ['\\', '\\n', '\n', 'n', '\'', '\\t', '\t', 't', 'xa0', 'xc2']

def checksum(str1):
    c = 0
    for i in str1:
        if i not in check:
            c = c + ord(i)

    cs = bin(c)
    d=""
    cs = cs.split('b')
    #print("my:"+type(cs[1]))
    return cs[1]

def iscorrect(str,cstr):
    print("yes")
    if(checksum(str)+"'"==cstr) or (checksum(str)+"\""==cstr) or (checksum(str)+"\'"==cstr):
        print("yes")
        return 1
    else:
        print("no")
        return 0



def fragment_and_send (message,host):
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

        FragmentedMESSAGE =  str(x) + '*|' + message[start: end] +'*|'+host+'*|'+str(MF)+'*|'+checksum(message[start:end])
        print("send packet : "+ FragmentedMESSAGE )
        send_socket.sendto(bytes(FragmentedMESSAGE,"utf-8") ,(sproxy_ip, sproxy_port))
def receive():
    not_completed=1
    x=0
    received=""

    while not_completed:
        message, proxyAddress = send_socket.recvfrom(1000000)
        ack_socket = socket(AF_INET, SOCK_DGRAM)
        ack_socket.connect(('127.0.0.1', 5100))

        print("hhhhhhhhhhhhhhhhhh")
        print(message)
        REC=str(message).split('*|')
        print("rrrrrrrrrrrrrrrrrrr")
        print(REC)
        var=REC[0].split('\'')
        var2=REC[0].split('\"')
        print("########")
        print(var)
        try:
            #print("im heeeeeeeeereeeeeeeeee")
            if "b\'"+str(x)==REC[0] or  "b\""+str(x)==REC[0]:
               # print("im heeeeeeeeereeeee-----------eeee")
                # print(str(REC[1]))
                print(checksum(REC[1]))
                print(REC[3])
                # received=received + REC[1]
                # print("appended is : " + received)
                # x=x+1

                if(iscorrect(REC[1],REC[3])):

                    ack_socket.send(bytes(str(x),'utf-8'))
                    print ("send ack")
                    #ack_socket.close()


                    received=received + REC[1]
                    print("appended is : " + received)
                    x=x+1
                else:
                    ack_socket.send(bytes(str(x), 'utf-8'))
                    # print("send ack")
                    # received = received + REC[1]
                    #print("appended is : " + received)
                    #x = x + 1
                    print("message had problem ")
        except IndexError as e:
            print('sorry, no 5')
            print(var2)
            if x==int(var2[1]) :

                if(iscorrect(REC[1],REC[3])):

                    received=received + REC[1]
                    #print("appended is : " + received)
                    x=x+1
                else:
                    print("message had problem ")
        st=str(received)
        file = open("page.html", 'wb')
        file.write(st.encode('UTF-8'))


        #print("yes")
        print(received)
        if(REC[2]=="1"):
            not_completed=0
        else:
            not_completed=1


def udp_send (message,host ):


   #send_socket.bind(('', sclient_port))

   #send_socket.sendto(bytes(message+host,"utf-8") ,(sproxy_ip, sproxy_port))
   #print("sent")
   fragment_and_send(message,host)
   receive()

   #modifiedMessage1, addr = send_socket.recvfrom(1000000)
   ##print (modifiedMessage1)
   #print(addr)
   send_socket.close()


#request = input('enter your request : ')


#print(len(request))
#request2=input('enter your host : ')
#print("dd"+str(type(request2)))
#udp_send(request ,request2)
#udp_send("df" ,"httpbin.org/404")
#udp_send("df" ,"www.google.com")
#udp_send("df" ,"en.wikipedia.org/404")
#udp_send("df" ,"us.yahoo.com")
udp_send("df" ,"www.google.com")











