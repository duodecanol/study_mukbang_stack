import aws_cdk as core
import aws_cdk.assertions as assertions

from study_mukbang.study_mukbang_stack import StudyMukbangStack

# example tests. To run these tests, uncomment this file along with the example
# resource in study_mukbang/study_mukbang_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = StudyMukbangStack(app, "study-mukbang")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
