## Oracle Cloud Infrastructure Functions

This repository contains sample code for the presentation "OCI Functions: Key to Database in Clouds."

The repository contains two projects:

* On-premises device emulator. Detail descriptions are [here](./onprem-ascii-device/README.md).
* Oracle OCI Function project. The subfolder contains artifacts for building and deploying FDK-compatible [code](./fn-lprint/README.MD).

> [!IMPORTANT]
> This function was designed as a demonstaration of Oracle Autonomous Database User-Defined Functions. 
> Although it's a working code, it was never developed to work in a production-grade environments. 

### Architecture Overview

The code in the repository is compatible with multiple clouds or could be run on-premises. 
However, the primary goal is to minimize Oracle Database code alterations during the cloud migration.
The diagram below depicts the Oracle Autonomous Database Serverless integration with an "on-premises" print device.
On the diagram:

* Oracle Autonomous Database (ADB) provisioned managed service with VCN-only access.
* Function and Printer images are stored in the Oracle Container Registry.
* The printer emulator runs as a single OCI Container Instance with a printer port 9100.
* OCI Function runs in the same compartment with access to the subnet.
* Function presented as a user-defined database function and available as a regular SQL function.  

![image](https://github.com/mikhailidim/oci-adb-udf/assets/10143072/6c92007d-36d7-4100-8606-a04f5fcb032c)

Database code could call the function to send text and basic printer commands to the device using the local IP address and any random port. 
That removes Oracle ADB limitations on accessing network or file resources. 


The  cource code is licensed under [MIT License](./LINCENSE).
 