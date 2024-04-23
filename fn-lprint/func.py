import io
import json
import logging
import socket
from fdk import response

def handler(ctx, data: io.BytesIO=None):
    payload = None
    device = ""
    rsp = { "result": 0 }
    timeout = 10
    reply = None
    lgr = logging.getLogger()
    try:
        # Retrieve key OCID and cryptographic endpoint
        cfg = ctx.Config()
        device = cfg.get("device","localhost:9100")
        lgr.setLevel(
                    logging.getLevelName(
                    cfg.get("log_level","INFO"))
        )
        
    except Exception as ex:
        print('ERROR: Missing configuration key', ex, flush=True)
        raise    
    
    try:
        body = json.loads(data)
        lgr.debug(str(body))
        lgr.debug(ctx)
        device = body.get("device")
        timeout = body.config.pop("timeout",default=10)
        payload = body.get("text")
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