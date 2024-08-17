## Line Print Cloud Function 

This project contains a Fn compatible function, prepared and tested to run as a serverless Oracle Cloud Infrastructure function. The function demonstrates Oracle Autonomous Database integration capabilities. Function accepts requests to the netowrk devices and forwards strings of text and pseudo  Printer Job Language ([PJL](https://en.wikipedia.org/wiki/Printer_Job_Language)) commands to alter device configuration or request status. 
The function is designed and tested againts a [basic network printer simulator](../onprem-ascii-device). 

[!IMPORTANT]
This function was designed as a demonstaration of Oracle Autonomous Database User-Defined Functions. 
Although it's a working code, it was never developed to work in a production-grade environments. 

### Deployment and prerequesits 

 Before use the function code, you may ned to:

 OCI Prerequesites:

 - Have access to the Oracle Cloud tenancy 
 - Have access to the rquired Oracle Cloud components 
 - Have appropriate policeis configured

More details on Getting started with Cloud functions in OCI [Functions Quick Start](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartcloudshell.htm) guide.

Target Prerequesites:

 - Have network from function network to the selected target. 

### How to run Line Print Function

According to [Oracle Documentation](https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsinvokingfunctions.htm#rawrequestinvoke), to execute function you could use:

- Using the Fn Project CLI.
- Using the Oracle Cloud Infrastructure CLI.
- Using the Oracle Cloud Infrastructure SDKs.
- Making a signed HTTP request to the function's invoke endpoint.

#### Using Fn Project CLI 

To run funcvtion with Fn CLI: 

1. Clone this repository to the OCI Cloud Shell or to your local device

    ```shell
    $ git clone https://github.com/mikhailidim/oci-adb-udf.git
    $ cd oci-adb-udf/fn-lprint
    ```
    
3. Checlk your access to OCI 

    ```shell
    # Login to your OCI account if needed
    $ oci session authenticate
    # List existing applications 
    $ fn list apps 
    ```
    
3.  Buld and deploy function

    ```shell
    $ fn build
    $ fn deploy --app your-appkication-name
    $
    ```
    
4.  After successful deployment call function

    ```shell
    $  echo '{"device":"YOUR-TEST-DEVICE-IP:LISTEN-PORT","text":"Hello","timeout":10,"font":"random"}' \
       |fn invoke your-app-name fn-lprint 
    ```
    
#### Using the Oracle Cloud Infrastructure CLI.
You can call an OCI Function without FN CLi, but you need to know the OCI ID for the function before pacing a call. 

1. Identify application and function IDs. Replace compartment ID with the compartment of your function.  

    ```shell
    $ export COMP_ID="ocid1.compartment.oc1.. *********rndm"
    $ export APP_NAME="YOUR-APP-NAME"
    $ export APP_ID=$(oci fn application list --compartment-id=$COMP_ID --display-name=$APP_NAME |jq '.data[0].id' -r)
    $ export FN_ID=$(oci fn function list --application-id=$APP_ID |jq '.data[0].id' -r)
    ```
   
2. Invoke function with the identified OCID. 

    ```shell
    $ oci fn function invoke --function-id $FN_ID --body \
      '{"device":"YOUR-TEST-DEVICE-IP:LISTEN-PORT","text":"Hello","timeout":10,"font":"random"}' \
      --file fn_response.json  
    ```
    
During the call OCI passes value of the argument _body_ as function arguments and stores function reply to the file fn_response.json (as in example above). If you need to send respons eto standard output use - as a fine name. 

#### Making a signed HTTP request to the function's invoke endpoint.

Every OCI function has an access endpoit. You could use it to place a raw HTTP calls. 

1. Find the function endpoint. Toge a funcion OCID use commands from previous steps. 

    ```shell 
     $ export FN_URL=$(oci fn function get --function-id $fn_id |jq '.data."invoke-endpoint"' -r)
    ```
    
2. Call function, using raw request command

    ```shell
     $ oci raw-request --http-method POST --target-uri $FN_URL \ 
       --request-body '{"device":"YOUR-TEST-DEVICE-IP:LISTEN-PORT","text":"Hello","timeout":10,"font":"random"}'
    ```
    
### Functional Description and Usage






