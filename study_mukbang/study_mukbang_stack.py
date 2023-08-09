from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_s3 as _s3,
    aws_s3_notifications,
    RemovalPolicy
)
from constructs import Construct

class StudyMukbangStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        s3_layer_artifact = _s3.Bucket.from_bucket_arn(self, "nextlabawsbucket", bucket_arn="arn:aws:s3:::nextlabawsbucket")
        s3_event_source = _s3.Bucket(self, "study-mukbang-bucket")

        layer_fixtures = _lambda.LayerVersion(
            self, 'fixtures_layer',
            code=_lambda.Code.from_asset("layers/fixtures"),
            description="study_mukbang_layer_fixtures",
            removal_policy=RemovalPolicy.DESTROY,
        )

        layer_organs = _lambda.LayerVersion(
            self, 'organs_layer',
            code=_lambda.Code.from_asset("layers/organs"),
            description="study_mukbang_layer_organs",
            removal_policy=RemovalPolicy.DESTROY,
        )

        layer_from_s3 = _lambda.LayerVersion(
            self, 'from_s3_layer',
            code=_lambda.S3Code(bucket=s3_layer_artifact, key="studycam/ch2.zip"),
            description="study_mukbang_layer_from_s3",
            removal_policy=RemovalPolicy.DESTROY,
        )

        function_1 = _lambda.Function(
            self, "function1",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="app.handler",
            code=_lambda.Code.from_asset("libpython"),
            layers=[layer_fixtures, layer_from_s3]
        )

        function_2 = _lambda.Function(
            self, "function2",
            runtime=_lambda.Runtime.PYTHON_3_10,
            handler="triggered.handler",
            code=_lambda.Code.from_asset("libpython"),
            layers=[layer_organs, layer_from_s3]
        )

        # create s3 notification for lambda function
        notif = aws_s3_notifications.LambdaDestination(function_2)
        # assign notification for the s3 event type (ex: OBJECT_CREATED)
        s3_event_source.add_event_notification(
            _s3.EventType.OBJECT_CREATED, notif,
            _s3.NotificationKeyFilter(suffix="*.json"),
        )

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "StudyMukbangQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
