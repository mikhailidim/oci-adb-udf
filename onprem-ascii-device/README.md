## TCP Device Emulator

This project is a simple LPD device emulator. The main purpose is to use the OCI Function and Oracle Autonomous Database user-defined functions demonstration.
The function offers a basic network printer simulator, with access through the TCP protocol on port 9100. 


### Functional Description 

When activated, the function accepts connections on port **9100** (default). Due to its sole illustration purpose, the function does not support multi-client access and maintains the global configuration settings between connections as a regular hardware device would. the code allows two types of communication: PJL (**P**rinter **J**ob **L**anguage) commands and text to print. 

```shell
 $ nc onprem-device-address 9100 <<EOF
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
