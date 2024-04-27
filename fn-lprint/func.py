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
    lgr.info("FN started. Perfroming function configuration.")
    try:
        # Retrieve key OCID and cryptographic endpoint
        cfg = ctx.Config()
        lgr.info(f'FN Configuration received {cfg}')
        # Default device from configuration
        device = cfg.get("device","localhost:9100")
        lgr.setLevel(cfg.get("log_level","INFO"))
        lgr.info(f'FN Configuration completed')
        
    except Exception as ex:
        lgr.error(f'Missing configuration key {ex}', flush=True)
        raise    
    
    try:
        body = json.loads(data.getvalue())
        lgr.debug(f'Reciveid request {body}')
        lgr.debug(f'Function context {ctx}')
        # Test if device is requested

        device = body["device"] if "device" in body else device
        timeout = int(body["timout"])  if "timeout" in body else timeout
        lgr.debug(f"Configuration extraxted. Device {device}, timeout: {timeout}")
        payload = body.get("text")
        lgr.info("Connecting to device")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((device.split(":")[0], 
                        int((device.split(":")[1]))))
            lgr.debug(f"Connected to {device}")            
            s.settimeout(timeout)
            lgr.debug("Timout adjusted")
            s.sendall(payload)
            lgr.debug("Message was send")
            reply = s.recv(1024)
            s.close()
            lgr.debug("Connection closed")
        rsp["success"] = {"status": "Ok","Sent": len(payload), "Received": int(reply)}    
        lgr.debug(f"Ready to reply {rsp}")    
    except (Exception, ValueError) as ex:
        lgr.error(f"Received exception {ex}")
        rsp["result"] = 1
        rsp["error"] = { "message": str(ex)}
        pass
    lgr.info(f"Function completed.")
    return response.Response(ctx, 
                            response_data=json.dumps(rsp),
                            headers={"Content-Type": "application/json"})