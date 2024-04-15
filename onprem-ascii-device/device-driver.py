import art
import socket
import os
import sys

PORT = int(os.environ.get("LISTEN_PORT",9100))  # Port to listen on (non-privileged ports are > 1023)
CFG  = dict({"status": "DOWN","config":{"encoding": "utf-8"}})
_PGL_STATUS = "@PJL INFO STATUS"
_PGL_CONFIG = "@PJL CONFIG"
def process_data(bytestr):
    rply = ""
    line = bytestr.decode(CFG.get("config").get("encoding","utf-8")).strip()
    if line.startswith(_PGL_STATUS):
        rply = f"{CFG}"
    elif line.startswith(_PGL_CONFIG):
        cmd = line.split()[2]
        CFG[cmd.split("=")[0]] = cmd.split("=")[1]
        rply = "OK"
    else:           
        art.tprint(line,CFG.get("font","standard"))
        rply= ""
    sys.stdout.flush()   
    return bytes(rply+"\n",CFG.get("config").get("encoding","utf-8"))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("", PORT))
    CFG["status"]="READY"
    while True: 
        s.listen()        
        conn, addr = s.accept()
        CFG["client"] = addr
        with conn:
            print("Connected by {0}".format(":".join([addr[0],str(addr[1])])))
            while True:
                data = conn.recv(1024)
                conn.send(process_data(data))
                if not data:
                    break
            print(f"Closed {addr}")
            sys.stdout.flush()    

