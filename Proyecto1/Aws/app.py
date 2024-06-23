from aws_cdk import core
from iot_stack import IoTStack

app = core.App()
IoTStack(app, "IoTStack")
app.synth()
