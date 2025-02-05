from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_iam as iam
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_stepfunctions as sfn
from aws_cdk import aws_stepfunctions_tasks as tasks
from aws_cdk import aws_lambda_python_alpha
from aws_cdk import Duration

from .settings import settings

class KidsCalendarStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "KidsCalendarQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # create S3 bucket
        bucket = s3.Bucket(
            self, "kids-calendar",
            versioned=True,
            block_public_access=s3.BlockPublicAccess(
                block_public_acls=True,
                block_public_policy=False,  # Allow public bucket policies
                ignore_public_acls=True,
                restrict_public_buckets=False  # Allow public access through bucket policies
            )
        )

        # Add a bucket policy for public read access to specific objects
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                principals=[iam.AnyPrincipal()],
                resources=[bucket.arn_for_objects("district_calendar.ics")]
            )
        )
      
        # create lambda function to download file from predefined URL to this bucket
        lambda_function_download = aws_lambda_python_alpha.PythonFunction(
            self, "kids-calendar-lambda-download",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_handler",
            entry="./resources/download_lambda",
            index="download_lambda.py",
            timeout=Duration.seconds(30),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "SCHOOL_CALENDAR_URL": settings['school_calendar_url']
            },
        )

        # create lambda function to process file
        lambda_function_process = aws_lambda_python_alpha.PythonFunction(
            self, "kids-calendar-lambda-process",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_handler",
            entry="./resources/process_lambda",
            index="process_lambda.py",
            timeout=Duration.seconds(30),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
            },
        )

        # create lambda function to delete old files from this bucket
        lambda_function_delete = aws_lambda_python_alpha.PythonFunction(
            self, "kids-calendar-lambda-delete",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="lambda_handler",
            entry="./resources/delete_lambda",
            index="delete_lambda.py",
            timeout=Duration.seconds(30),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
            },
        )

        # bucket.grant_read_write(lambda_function_download)
        lambda_function_download.add_to_role_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                    "s3:PutObjectAcl",
                    "s3:ListBucket",
                    "s3:DeleteObject"
                ],
                resources=[
                    bucket.bucket_arn,
                    f"{bucket.bucket_arn}/*"
                ]
            )
        )
                
        bucket.grant_read_write(lambda_function_process)
        bucket.grant_read_write(lambda_function_delete)

        # define tast for state machine
        lambda_function_download_task = tasks.LambdaInvoke(
            self, "kids-calendar-lambda-download-task",
            lambda_function=lambda_function_download
        )

        lambda_function_process_task = tasks.LambdaInvoke(
            self, "kids-calendar-lambda-process-task",
            lambda_function=lambda_function_process,
        )

        lambda_function_delete_task = tasks.LambdaInvoke(
            self, "kids-calendar-lambda-delete-task",
            lambda_function=lambda_function_delete,
        )


        # organize lambda functions into sequence using step function
        state_machine = sfn.StateMachine(
            self, "kids-calendar-state-machine",
            definition=sfn.Chain
            .start(lambda_function_download_task)
            .next(lambda_function_process_task)
            .next(lambda_function_delete_task)
        )

        # create scheduler for this state machine and execute every morning at 2AM ET
        scheduler = events.Rule(
            self, "kids-calendar-scheduler",
            schedule=events.Schedule.cron(
                minute="0",
                hour="2",
                month="*",
                week_day="*",
                year="*",
            ),
            targets=[targets.SfnStateMachine(state_machine)],
        )

        # change policy for s3 bucket to make spefied object public
        bucket.add_to_resource_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["s3:GetObject"],
                principals=[iam.AnyPrincipal()],
                resources=[bucket.arn_for_objects("*")],
            )
        )


        