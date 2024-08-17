## Line Print Cloud Function 

This project contains a Fn compatible function, prepared and tested to run as a serverless Oracle Cloud Infrastructure function. The function demonstrates Oracle Autonomous Database integration capabilities. Function accepts requests to the netowrk devices and forwards strings of text and pseudo  Printer Job Language ([PJL](https://en.wikipedia.org/wiki/Printer_Job_Language)) commands to alter device configuration or request status. 
The function is designed and tested againts a [basic network printer simulator](../onprem-ascii-device). 

[!IMPORTANT]
This function was designed as a demonstaration of Oracle Autonomous Database User-Defined Functions. 
Although it's a working code, it was never developed to work in a production-grade environments. 

### Deployment and prerequesits 

Before you could test the Line Print Ffunction 

### How to run Line Print Function

According to [Oracle Documentation](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsinvokingfunctions.htm#rawrequestinvoke), to execute function you could use:

- Using the Fn Project CLI.
- Using the Oracle Cloud Infrastructure CLI.
- Using the Oracle Cloud Infrastructure SDKs.
- Making a signed HTTP request to the function's invoke endpoint.

But before to test the function you need to complete prerequesites: 




#### Using Fn Project CLI 

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
#### Using the Oracle Cloud Infrastructure CLI.
#### Using the Oracle Cloud Infrastructure SDKs.
#### Making a signed HTTP request to the function's invoke endpoint.

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





