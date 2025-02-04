import aws_cdk as core
import aws_cdk.assertions as assertions

from kids_calendar.kids_calendar_stack import KidsCalendarStack

# example tests. To run these tests, uncomment this file along with the example
# resource in kids_calendar/kids_calendar_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = KidsCalendarStack(app, "kids-calendar")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
