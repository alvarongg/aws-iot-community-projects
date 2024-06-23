from aws_cdk import aws_s3 as s3, aws_iot as iot, core


class IoTStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear un bucket de S3
        bucket = s3.Bucket(self, "IoTDataBucket")

        # Crear una política de IoT
        policy = iot.CfnPolicy(
            self,
            "IoTPolicy",
            policy_document={
                "Version": "2012-10-17",
                "Statement": [
                    {"Effect": "Allow", "Action": ["iot:Publish"], "Resource": ["*"]}
                ],
            },
        )

        # Crear un certificado de IoT
        cert = iot.CfnCertificate(self, "IoTCertificate", status="ACTIVE")

        # Crear una regla de IoT que envía datos a S3
        iot.CfnTopicRule(
            self,
            "IoTRule",
            topic_rule_payload={
                "sql": "SELECT * FROM 'iot/topic'",
                "actions": [
                    {
                        "s3": {
                            "bucketName": bucket.bucket_name,
                            "key": "iot_data/${timestamp()}.json",
                            "roleArn": "arn:aws:iam::${AWS::AccountId}:role/service-role/iot-s3-role",
                        }
                    }
                ],
            },
        )
