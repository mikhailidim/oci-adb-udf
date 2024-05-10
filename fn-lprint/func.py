import io
import json
import logging
import socket
from fdk import response

_PGL_STATUS = "@PJL INFO STATUS"
_PGL_CONFIG = "@PJL CONFIG"
lgr = logging.getLogger()
lgr.info("FN started. Perfroming function configuration.")

def commandProcessor(soc, cfg):
    rpl = ""
    for key,value in cfg:
        soc.sendall(f"{_PGL_CONFIG} {key}={value}")
        lgr.debug("Command was send")
        rpl+" "+soc.recv(1024)       
    return rpl

def printText(soc, text):
    rpl=""
    soc.sendall(f"{_PGL_CONFIG} {key}={value}")
    lgr.debug("Text was printed.")
    rpl+" "+soc.recv(1024)       
    return rpl;

def handler(ctx, data: io.BytesIO=None):
    payload = None
    device = ""
    rsp = { "result": 0 }
    timeout = 10
    reply = None
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

        device = body["device"] if "device" in body else device
        payload = body.get("text").encode()
        lpconfig = body["config"] if "config" in body else device         
        timeout = int(lpconfig["timeout"])  if "timeout" in lpconfig else timeout

        lgr.debug(f"Configuration extraxted. Device {device}, timeout: {timeout}")
        lgr.info("Connecting to device")
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            addr = (device.split(":")[0], 
                        int(device.split(":")[1]))
            lgr.debug(f"Ready to access {addr}")            
            s.connect(addr)
            lgr.debug(f"Connected to {addr}")            
            s.settimeout(timeout)            
            lgr.debug("Timout adjusted.")
            commandProcessor(s,lpconfig)
            lgr.debug("Configuration processed.")
            reply = printText(s,payload)
        lgr.debug("Connection closed")
        
        rsp["success"] = {"status": "Ok","Sent": len(payload), "Received": len(reply)}    
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