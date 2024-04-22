import io
import json
import logging
import socket
from fdk import response

def handler(ctx, data: io.BytesIO=None):
    payload = None
    device = "localhost:9100"
    enc = "base64"
    rsp = { "result": 0 }
    timeout = 10
    reply = None
    try:
        body = json.loads(data)
        device = body.get("device")
        timeout = body.config.pop("timeout",default=10)
        
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((device.split(":")[0], 
                        int((device.split(":")[1]))))
            s.settimeout(timeout)
            s.sendall(payload)
            reply = s.recv(1024)
            s.close()
        rsp["success"] = {"status": "Ok","Sent": len(payload), "Received": int(reply)}
        
    except (Exception, ValueError) as ex:
        print(str(ex))
        rsp["result"] = 1
        rsp["error"] = { "message": str(ex)}
        pass
    
    return response.Response(ctx, 
                            response_data=json.dumps(rsp),
                            headers={"Content-Type": "application/json"})