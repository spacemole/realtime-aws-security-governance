# Real-time AWS Security Governance
>A real-time Cloud Custodian security check implamentation for AWS.



## About the project
This project contains resources configured for enabaling real-time security notifications for AWS infastructures using cloud custodian.

##### What is Cloud Custodian?
Cloud custodian is a tool for managing resources on cloud computing platforms. Users create YML formatted policy files that are run by the software to generate simple scripts that replace ad-hoc implementations for automating infastructure. Policy files have 3 main sections: 
- Events: The cloud event that needs to be monitored (e.g. securitgy group is modified)
- Filters: The specific configureations of the event that should be acted on.
- Actions: The actions that should be carried out when filterd events are detected. 

Cloud custodian can work in a variaty of modes and applications. Traditional policys are run either once on command execution or on a time interval. As this implamentation is focused on security, minimal delay is required to decrese timeframe before a security issue occours and is detected.

Because of this "cloud-trail" mode was used, which allows scripts to execute in as close to real time as possible. AWS event bridge rules asses events logged in AWS cloud trail and trigger AWS Lambda funcitons as events meet the policys criteria.

The AWS Lambda function analyses the events actions and filter agains uncompliant configurations. When an event meets criterea it is tagged, and an email is sent to the administrators via AWS Sns.


## Installation Guide
The following stages must be completed

- Install cloud custodian
- AWS resources set-up 
- Configure Custodian mailer




#### **Installing Cloud Custodian**

Cloud custodian can be installed from most systems, including Linux, OSX, Windows and Docker.
Follow the following link to the [cloud custodian instalation documetation](https://cloudcustodian.io/docs/quickstart/index.html) and install on your system.

#### **AWS resources set-up**

AWS resources needed for this implementation have been pre-configured and can be deployed using the CloudFormation template or CDK stack. To find the files, open the folder [cloudformationAWS](https://github.com/spacemole/realtime-aws-security-governance/tree/main/cloudformation).

To use the template, open the [CloudFormation Console](https://console.aws.amazon.com/cloudformation/), and create a new stack.

To deploy the resources through the stack, copy the code into the cdk project, and run the command:
 ```
 cdk deploy
 ```


#### **Configure Custodian Mailer**
Custodian Mailer is an additional tool that can be installed to allow notifications through cloud custodian policies.
Follow the email section of the [guide](https://cloudcustodian.io/docs/tools/c7n-mailer.html) on the cloud custodian documentation.

To set up the mailer tool, open the [mailer.yml](https://github.com/spacemole/realtime-aws-security-governance/blob/main/Email/mailer.yml) file and edit it, and run the command:
```
 c7n-mailer --config mailer.yml --update-lambda
 ```

Cloud Custodian Mailer uses a template to create the email, to edit it open the [email.html.j2](https://github.com/spacemole/realtime-aws-security-governance/blob/main/Email/email.html.j2).

#### **Running YML policy**
##### Run cloud custodian on chosen system with following commands:

```python {cmd}
python -m venv custodian
.\custodian\Scripts\Activate.ps1
```

##### Copy policy YAML files to directory.
Copy securityGroup.yml and s3Encryption.yml into the directory of the terminal window, or navigate in the terminal to the folder containing them.

##### Prepare command

Running policies requires users unique AWS access key and secrete for access. To find your own access key, visit the [AWS documentation](https://docs.aws.amazon.com/powershell/latest/userguide/pstools-appendix-sign-up.html) for instructions.

- Add your unique access key and secret to the following commands, replaceing the placeholder text. 
- Replace region placeholder with aws region you wish to monitor.
- Replace filename placeholder with name of policy filename.

Policiy execution command:
```bash {cmd}
$Env:AWS_ACCESS_KEY_ID="INSERT_KEY_HERE"; $Env:AWS_SECRET_ACCESS_KEY="INSERT_KEY_HERE" ; $Env:AWS_DEFAULT_REGION="INSERT_REGION_HERE" ; custodian run --output-dir=. INSERT_FILENAME_HERE.yml
```

Example command:
```bash {cmd}
$Env:AWS_ACCESS_KEY_ID="AKIJDNEC6PMV4E2RJN4F"; $Env:AWS_SECRET_ACCESS_KEY="XecbrS5sv7JdocZuLHevHtLp+G86RwCd24f28RWj" ; $Env:AWS_DEFAULT_REGION="ap-southeast-2" ; custodian run --output-dir=. securitygroup.yml
```


##### Run policy execution command

Run edited command in the terminal. An AWS lambda funtion and AWS event bridge rule will be generated from this policy.

To run additional policys, such as the s3Encryption ploicy, replace the filename of the policy execution command and run again. This will generate its own AWS lambda funtion and AWS event bridge rule. 



