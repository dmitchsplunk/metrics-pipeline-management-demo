from random import randint
from time import sleep
from uuid import uuid4
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter


provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("mytracer")


def process_orders():

    for x in range(100000):
        process_order()
        # wait for 100ms before processing another order
        sleep(0.1)

    return


def process_order():
    with tracer.start_as_current_span("process_order") as span:
        current_span = trace.get_current_span()

        customer_type = get_customer_type()
        user_id = get_user_id()
        payment_type = get_payment_type()

        current_span.set_attribute("customerType", customer_type)
        current_span.set_attribute("userId", user_id)
        current_span.set_attribute("paymentType", payment_type)

        print("Processing order with customerType: {}, userId: {}, paymentType: {}".format(customer_type, user_id, payment_type))

    return


def get_payment_type():
    payment_type = randint(1, 3)
    if (payment_type == 1):
        return "credit"
    if (payment_type == 2):
        return "paypal"
    if (payment_type == 3):
        return "giftcard"


def get_customer_type():
    payment_type = randint(1, 3)
    if (payment_type == 1):
        return "bronze"
    if (payment_type == 2):
        return "silver"
    if (payment_type == 3):
        return "gold"


def get_user_id():
    return str(uuid4())


if __name__ == "__main__":
    process_orders()