from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_iot as iot,
    aws_iam as iam,
)
from constructs import Construct


class IoTStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Crear un bucket de S3
        bucket = s3.Bucket(self, "IoTDataBucket")

        # Crear una política de IAM para permitir que IoT Core publique en el bucket de S3
        role = iam.Role(
            self, "IoTRole", assumed_by=iam.ServicePrincipal("iot.amazonaws.com")
        )

        role.add_to_policy(
            iam.PolicyStatement(
                actions=["s3:PutObject"], resources=[f"{bucket.bucket_arn}/*"]
            )
        )

        # Crear una Thing en IoT
        thing = iot.CfnThing(self, "IoTThing", thing_name="MyIoTThing")

        # Crear una política de IoT
        policy_document = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "iot:Connect",
                        "iot:Publish",
                        "iot:Subscribe",
                        "iot:Receive",
                    ],
                    "Resource": "*",
                }
            ],
        }

        policy = iot.CfnPolicy(
            self,
            "IoTPolicy",
            policy_name="MyIoTPolicy",
            policy_document=policy_document,
        )

        # Carga tu CSR aquí
        csr = """-----BEGIN CERTIFICATE REQUEST-----
MIICtzCCAZ8CAQAwcjELMAkGA1UEBhMCVVMxEzARBgNVBAgMCkNhbGlmb3JuaWEx
FjAUBgNVBAcMDVNhbiBGcmFuY2lzY28xEDAOBgNVBAoMB0V4YW1wbGUxEDAOBgNV
BAsMB1N1cHBvcnQxEjAQBgNVBAMMCWxvY2FsaG9zdDCCASIwDQYJKoZIhvcNAQEB
BQADggEPADCCAQoCggEBAJhGrLsoatEYvGOuQ37AoGvgHVdO1PchsORr2/aG3Nbd
GURqTjubJfWdHK9HhLq300BjfRQzMNy+FcBv/5jRDvqGja8EgpARiwPnwhwHqFoM
9Ym3gWS0MhbD4lb2OBIspL+d9F4bCExdvi/Sc4zHUiMv/N8JSPLxpqy6pwl+dpwG
c5PY8Mmo4ZM4pX4pCG6faUuiUz3ruY78xssH5OYL3ehN/A1Ab0v9TnkifVQcSHGe
cOtgO7orAmTfRjtvhhTzyZXZ7Qz/w2hKRs/09jkcNiq+UDP3MYJIAujZVDaTStNO
Fn+ZUTd7HP0tuYoTYFkAfCFCwu/2BE+GLsJD1KZaXU8CAwEAAaAAMA0GCSqGSIb3
DQEBCwUAA4IBAQBeumgCX75JZ/Dd01oRxuWFZIX5hTQ6M7PPYX8jW4syD2aHyp7E
nrFSkoAGjGICUwSH/WxMAG3DieQG3dxFJTcYjzMgynMiHPlN5FcPIGoUkxVllvzs
PbDx7n6BckWyCDCHmhaSIL7IQN2umESqWVYMDEsrBo/20b8T2WpLdiNm5dP5XJkd
9X06raR7iK4V0PiD2IVoKReQcB+eR2wuVXlCyiipacSEvXrSpxTIhXZ9+vN8P4nu
7U1/2EPWSi2b2xK9OsOS6vQckaBzxwEis7SWb0BiiaO+tme3T5uU1gtKRlIMIDvZ
JbSR7eMLP0cRCW1NBBlkx0zoUO7wDQqagYu8
-----END CERTIFICATE REQUEST-----"""

        # Crear un certificado de IoT utilizando la CSR
        cert = iot.CfnCertificate(
            self, "IoTCertificate", certificate_signing_request=csr, status="ACTIVE"
        )

        # Adjuntar la política al certificado
        iot.CfnPolicyPrincipalAttachment(
            self,
            "PolicyAttachment",
            policy_name=policy.policy_name,
            principal=cert.attr_arn,
        )

        # Adjuntar el certificado a la Thing
        iot.CfnThingPrincipalAttachment(
            self,
            "ThingAttachment",
            thing_name=thing.thing_name,
            principal=cert.attr_arn,
        )

        # Crear una regla de IoT que envía datos a S3
        iot.CfnTopicRule(
            self,
            "IoTRule",
            topic_rule_payload=iot.CfnTopicRule.TopicRulePayloadProperty(
                sql="SELECT * FROM 'temperature/topic'",
                actions=[
                    iot.CfnTopicRule.ActionProperty(
                        s3=iot.CfnTopicRule.S3ActionProperty(
                            bucket_name=bucket.bucket_name,
                            key="iot_data/${timestamp()}.json",
                            role_arn=role.role_arn,
                        )
                    )
                ],
            ),
        )
