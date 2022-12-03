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
    CfnTag as cfntag_
)

from constructs import Construct

class ProjectCdkStack(Stack):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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
        resourcegroups_.CfnGroup(self, "EncryptionGroup",name="EncryptionPolicy",resource_query=resourcegroups_.CfnGroup.ResourceQueryProperty(
            query=resourcegroups_.CfnGroup.QueryProperty(tag_filters=[resourcegroups_.CfnGroup.TagFilterProperty(key="Encryption",values=["no-encryption"])]),type="TAG_FILTERS_1_0"))
        resourcegroups_.CfnGroup(self, "OpenSecGroup",name="SecurityGroupPolicy",resource_query=resourcegroups_.CfnGroup.ResourceQueryProperty(
            query=resourcegroups_.CfnGroup.QueryProperty(tag_filters=[resourcegroups_.CfnGroup.TagFilterProperty(key="Open-security",values=["Detected"])]),type="TAG_FILTERS_1_0"))