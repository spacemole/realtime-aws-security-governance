from aws_cdk import (
    Stack,
    aws_cloudtrail as cloudtrail_,
    aws_kms as kms,
    aws_s3 as  s3_,
    RemovalPolicy,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_sqs as sqs_,
    aws_ses as ses_,
    aws_resourcegroups as resourcegroups_,
    CfnTag as cfntag_,
    aws_iam as iam_
)

from constructs import Construct

class ProjectCdkStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #creating cloudcustodian policy for the role
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/PolicyDocument.html
        cloudcustodianpolicyrol=iam_.PolicyDocument(
            statements= [iam_.PolicyStatement(
                actions=[
                        "cloudwatch:PutMetricData",
                        "ec2:DescribeNetworkInterfaces",
                        "ec2:DeleteNetworkInterface",
                        "ec2:CreateNetworkInterface",
                        "events:PutRule",
                        "events:PutTargets",
                        "iam:PassRole",
                        "lambda:CreateFunction",
                        "lambda:TagResource",
                        "lambda:CreateEventSourceMapping",
                        "lambda:UntagResource",
                        "lambda:PutFunctionConcurrency",
                        "lambda:DeleteFunction",
                        "lambda:UpdateEventSourceMapping",
                        "lambda:InvokeFunction",
                        "lambda:UpdateFunctionConfiguration",
                        "lambda:UpdateAlias",
                        "lambda:UpdateFunctionCode",
                        "lambda:AddPermission",
                        "lambda:DeleteAlias",
                        "lambda:DeleteFunctionConcurrency",
                        "lambda:DeleteEventSourceMapping",
                        "lambda:RemovePermission",
                        "lambda:CreateAlias",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                        "logs:CreateLogGroup"                    
                         ],
                resources=["*"]
            )]
        )
        #creating the iam role
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/Role.html
        lambda_role = iam_.Role(self, "CloudCustodianRole",
            assumed_by=iam_.ServicePrincipal("lambda.amazonaws.com"),
            description="Cloud Custodian Role to Execute Lambda Function",
            inline_policies={"cloudcustodianpolicyrol":cloudcustodianpolicyrol}
        )
       
        #attach policies to the role
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_iam/ManagedPolicy.html
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonEC2FullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("IAMFullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonSESFullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchLogsFullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("ResourceGroupsandTagEditorFullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"))
            
        #creating bucket to store logs
        #https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-s3.Bucket.html
        trail_bucket = s3_.Bucket(self,"newbucket",removal_policy=RemovalPolicy.DESTROY)
        #creating cloudtrail
        #https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-cloudtrail.Trail.html
        trail = cloudtrail_.Trail(self, id="newtrail")
        #attaching an bucket to the trail
        #https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-cloudtrail.Trail.html
        trail.add_s3_event_selector([cloudtrail_.S3EventSelector(
            bucket=trail_bucket
            )],
            read_write_type=cloudtrail_.ReadWriteType.WRITE_ONLY)
        #adding policy to trail to remove it
        trail.apply_removal_policy(RemovalPolicy.DESTROY)
        #creating sns
        #https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-sns.Topic.html
        topic = sns_.Topic(self, 'CloudCustodianSns')
        #creating sqs
        #https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-sqs.Queue.html
        queue = sqs_.Queue(self, 'CloudCustodianSqs')
        #sqs subscription
        #https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_sns_subscriptions.SqsSubscription.html
        topic.add_subscription(subscriptions_.SqsSubscription(queue))
        #sns email subscription
        topic.add_subscription(subscriptions_.EmailSubscription("evelyncaviedesa@gmail.com"))
        #ses verify identities
        #https://docs.aws.amazon.com/cdk/api/v1/docs/aws-ses-readme.html
        ses_.CfnEmailIdentity(self,"receipt",email_identity="103483662@student.swin.edu.au")
        ses_.CfnEmailIdentity(self,"sender",email_identity="evelyncaviedesa@gmail.com")
        #resource groups
        #https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_aws-resourcegroups.CfnGroup.html
        #https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.CfnTag.html
        #this tag will be in both policies
        resourcegroups_.CfnGroup(self, "securityIssue",name="securityIssue",resource_query=resourcegroups_.CfnGroup.ResourceQueryProperty(
            query=resourcegroups_.CfnGroup.QueryProperty(tag_filters=[resourcegroups_.CfnGroup.TagFilterProperty(key="Security-issue",values=["detected"])]),type="TAG_FILTERS_1_0"))
        #this tag is for security group policy
        resourcegroups_.CfnGroup(self, "sg-Open",name="sg-Open",resource_query=resourcegroups_.CfnGroup.ResourceQueryProperty(
            query=resourcegroups_.CfnGroup.QueryProperty(tag_filters=[resourcegroups_.CfnGroup.TagFilterProperty(key="sg-Open-security",values=["detected"])]),type="TAG_FILTERS_1_0"))
        #this tag is for s3 Bucket policy
        resourcegroups_.CfnGroup(self, "s3-Encryption",name="s3-Encryption",resource_query=resourcegroups_.CfnGroup.ResourceQueryProperty(
            query=resourcegroups_.CfnGroup.QueryProperty(tag_filters=[resourcegroups_.CfnGroup.TagFilterProperty(key="s3-Encryption",values=["detected"])]),type="TAG_FILTERS_1_0"))        