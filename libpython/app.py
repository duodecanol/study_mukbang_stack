from pathlib import Path
from pprint import pprint

def handler(event, context):
    """
    Lambda function handler
    """
    print("Lambda running")
    pprint(event)
    pprint(context)

    opt = Path("/opt")
    pprint(list(opt.iterdir()))
