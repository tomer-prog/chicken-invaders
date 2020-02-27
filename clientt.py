import socket
IP = "0.0.0.0"
Id_des = "127.0.0.1"
port = 8002
#from PIL import Image
import base64
import glob
import subprocess
global KEEP
KEEP = True
def main():
    global KEEP
    KEEP = True
    while KEEP:
        print ("hello")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((Id_des, port))
        msg = input("your command?")
        masg = msg.encode()
        client_socket.send(masg)
        msg = msg.upper()
        print (msg)
        if msg == "TAKE SCREEN SHOT":        #reciving the server screen shot
            saved_path = "C:\\Users\\tomme\\Desktop\\python1\\theimg.jpg"
            # picture = ""
            # picture = picture.encode()
            client_socket.close()
            # temerate server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((IP, 8072))
            server_socket.listen(1)
            client_socket, client_address = server_socket.accept()

            first_time = True
            while True:
                mge = client_socket.recv(1024)
                try:
                    mge = mge.decode()
                    if not mge == "exit":
                        mge = mge.encode()
                except:
                    pass
                if mge == "exit":
                    print("hahaha")
                    # image_file = open(saved_path, 'w')
                    with open(("%s"%saved_path),"wb") as fout:
                        fout.write(picture)
                    # image_file.write(picture)
                    break
                else:
                    if first_time:
                        picture = mge
                        first_time = False
                    else:
                        first_time=False
                        picture += mge
            print ("image has added to folder")
            server_socket.close()
            client_socket.close()
        elif msg == "SHOW FOLDER":
            thefolder = input("the folder?:")
            client_socket.send("C:\\Users\\tomme\\Desktop\\%s" %thefolder)
            client_socket.close()
        elif msg == "DELETE FOLDER":
            thefolder = input("the folder you would like to delete:")
            client_socket.send(thefolder)
            client_socket.close()

        elif msg == "EXECUTE":
            the_action = input("what would you like to open?:")
            client_socket.send(the_action)
            client_socket.close()
        elif msg== "TAKE VIDEO":
            #todo put my path
            video_bytes = client_socket.recv(2000)
            #todo put my path
            with open(r"mypath", "wb") as out_file:  # open for [w]riting as [b]inary
                out_file.write(video_bytes)
        elif msg == "EXIT":
            client_socket.close()
            KEEP = False
        #todo make a take if

if __name__ == '__main__':
    main()
