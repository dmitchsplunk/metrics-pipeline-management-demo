from random import randint
from time import sleep
from uuid import uuid4

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
   ConsoleMetricExporter,
   PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter


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
tracer = trace.get_tracer("order-service")

metric_reader = PeriodicExportingMetricReader(OTLPMetricExporter())
provider = MeterProvider(metric_readers=[metric_reader])

metrics.set_meter_provider(provider)
meter = metrics.get_meter("my.meter.name")

order_counter = meter.create_counter(
   "order.counter", unit="1", description="Counts the number of orders processed"
)

def process_orders():

    for x in range(5000):
        process_order()

    return


def process_order():

    customer_type = get_customer_type()
    user_id = get_user_id()
    payment_type = get_payment_type()

    print("Processing order with customerType: {}, userId: {}, paymentType: {}".format(customer_type, user_id, payment_type))
    # wait for 100ms before processing another order
    sleep(0.1)

    order_counter.add(1, {
        "customer.type": customer_type,
        "user.id": user_id,
        "payment.type": payment_type
    })

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
