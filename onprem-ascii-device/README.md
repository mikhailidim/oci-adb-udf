## TCP Device Emulator

This project is a simple LPD device emulator. The main purpose is to use the OCI Function and Oracle Autonomous Database user-defined functions demonstration.
The function offers a basic network printer simulator, with access through the TCP protocol on port 9100. 

### Run the Device emulator

You can run device emulator as a:

- Local Python code
- Docker container

#### Local Python Code 

To run device a s a local Python application, run commands as below. We recommedn you to create a new virtual environment for that. 

1. Clone this repository
2. Install dependencies into your Python environment

  ```shell
    $ cd onprem-ascii-device
    $ python -m pip install --upgrade pip
    $  pip install -r requirements.txt    
   ```
3.  Run device emulator

   ```shell
    $ python device-driver.py 
 
   ```
    
4.  Optionally you may change device port with the **LISTEN_PORT** environment variable

   ```shell
    $ LISTEN_PORT=9110 python device-driver.py 
 
   ```
#### Docker Container

To run function as a container use Docker command as below:

```
  $ docker run -d -p 9100:9100 mikhailidim/print-device
```

To change the port in the container use the environment variable **LINSTEN_PORT**:

```
  $ docker run -e "LISTEN_PORT=9110" -d -p 9110:9110 mikhailidim/print-device
```


### Functional Description and Usage

When activated, the function accepts connections on port **9100** (default). Due to its sole illustration purpose, the function does not support multi-client access and maintains the global configuration settings between connections as a regular hardware device would. the code allows two types of communication: PJL (**P**rinter **J**ob **L**anguage) commands and text to print. 

```shell
 $ nc localhost 9100 <<EOF
  Text to Print
  EOF 
```

As a result of the command above, the function will produce log entries similar to the sample below:

```
Connected by 192.168.1.1:29223
 _____              _     _            ____         _         _   
|_   _|  ___ __  __| |_  | |_   ___   |  _ \  _ __ (_) _ __  | |_ 
  | |   / _ \\ \/ /| __| | __| / _ \  | |_) || '__|| || '_ \ | __|
  | |  |  __/ >  < | |_  | |_ | (_) | |  __/ | |   | || | | || |_ 
  |_|   \___|/_/\_\ \__|  \__| \___/  |_|    |_|   |_||_| |_| \__|
                                                                  


Closed ('192.168.1.1', 29223)
```

To check the device status, use **@PJL INFO STATUS** command as in the example below

```shell
$ nc localhost 9100<<EOF
  @PJL INFO STATUS
  EOF
```
The simulator should reply with the status and current configuration details:

```
{'status': 'READY', 'config': {'encoding': 'utf-8'}, 'client': ('192.168.1.1', 29223)}

```
The configuration command  controls character encoding and  ASCII art font. To change the output, run the commands below:

```shell
$ nc localhost 9100 <<EOF
 @PJL CONFIG font=random
 Test Output
 Test 2
 EOF
OK
```
Now, with the random ASCII font face, the device log my look like one below:

```
Connected by 192.168.1.1:46523
                                                                                                   
   ##     ######   ######   ######                     ##  ##   ######   ######   ##  ##   ######  
 ######   ######   ###      ######            ######   ##  ##   ######   ##  ##   ##  ##   ######  
   ##     ##       ######     ##              ##  ##   ##  ##     ##     ##  ##   ##  ##     ##    
   ##     ####         ##     ##              ##  ##   ##  ##     ##     ######   ##  ##     ##    
   ##     ##       ######     ##              ##  ##   ######     ##     ###      ######     ##    
   ####   ######   ######     ##              ######   ######     ##     ###      ######     ##    
                                                                                                   

         _  _________  _   _____          _    _____   _ 
 _______| |(  _   _  )( ) (  _  ) _______| |  (  _  ) ( )
(_______  || | | | | || |_| | | |(_______  |  | | | |_| |
        |_|(_) (_) (_)(_____) (_)        |_|  (_) (_____)


Closed ('192.168.1.1', 46523)
```





