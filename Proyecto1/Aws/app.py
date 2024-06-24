from aws_cdk import App
from lib.iot_stack import IoTStack

app = App()
IoTStack(app, "IoTStack1")
app.synth()
