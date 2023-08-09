from pathlib import Path
import subprocess

def handler(event, context):
    """
    Lambda function handler
    """
    print("Lambda running")
    print(event)
    print(context.__dict__)

    command = 'ls -lahR /opt'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        print(error.decode())
    print(output.decode())

