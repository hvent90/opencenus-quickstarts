#!/usr/bin/env python

import os
import time
import sys

from opencensus.trace.tracer import Tracer
from opencensus.trace.exporters.zipkin_exporter import ZipkinExporter
from opencensus.trace.samplers import always_on

# 1a. Setup the exporter
ze = ZipkinExporter(service_name="python-quickstart",
                                host_name='localhost',
                                port=9411,
                                endpoint='/api/v2/spans')
# 1b. Set the tracer to use the exporter
# 2. Configure 100% sample rate, otherwise, few traces will be sampled.
# 3. Get the global singleton Tracer object
tracer = Tracer(exporter=ze, sampler=always_on.AlwaysOnSampler())

def main():
    # 4. Create a scoped span. The span will close at the end of the block.
    with tracer.span(name="main") as span:
        for i in range(0, 10):
            doWork()

def doWork():
    # 5. Start another span. Because this is within the scope of the "main" span,
    # this will automatically be a child span.
    with tracer.span(name="doWork"):
        print("doing busy work")
        time.sleep(0.1)

if __name__ == "__main__":
    main()
