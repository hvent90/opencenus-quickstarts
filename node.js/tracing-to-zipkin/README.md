### Run it locally
1. Clone the example repository: `git clone https://github.com/hvent90/opencensus-quickstarts`
2. Change to the example directory: `cd opencensus-quickstarts/node.js`
3. Install dependencies: `npm install`
4. Download Zipkin: `curl -sSL https://zipkin.io/quickstart.sh | bash -s`
5. Start Zipkin: `java -jar zipkin.jar`
6. Run the code: `node tracing-to-zipkin/tracingtozipkin.js`
7. Navigate to Zipkin Web UI: http://localhost:9411
8. Click Find Traces, and you should see a trace.
9. Click into that, and you should see the details.

![](node-tracing-zipkin.png)

### How does it work?
```js
// 1. Get the global singleton Tracer object
// 2. Configure 100% sample rate, otherwise, few traces will be sampled.
const tracer = tracing.start({samplingRate: 1}).tracer;

// 3. Configure exporter to export traces to Zipkin.
tracer.registerSpanEventListener(new zipkin.ZipkinTraceExporter({
    url: 'http://localhost:9411/api/v2/spans',
    serviceName: 'node.js-quickstart'
}));

function main() {
  // 4. Create a scoped span, a scoped span will automatically end when closed.
  tracer.startRootSpan({name: 'main'}, rootSpan => {
    for (let i = 0; i < 10; i++) {
      doWork(i);
    }

    // 6b. End the spans
    rootSpan.end();
  });
}
```

#### Using the Tracer
To start a trace, you first need to get a reference to the `Tracer` (3). It can be retrieved as a global singleton.
```js
// 1. Get the global singleton Tracer object
// 2. Configure 100% sample rate, otherwise, few traces will be sampled.
const tracer = tracing.start({samplingRate: 1}).tracer;
```

#### Configure Sampler
Configure 100% sample rate, otherwise, few traces will be sampled.
```js
// 1. Get the global singleton Tracer object
// 2. Configure 100% sample rate, otherwise, few traces will be sampled.
const tracer = tracing.start({samplingRate: 1}).tracer;
```

#### Configure Exporter
OpenCensus can export traces to different distributed tracing stores (such as Zipkin, Jeager, Stackdriver Trace). In (3), we configure OpenCensus to export to Zipkin, which is listening on `localhost` port `9411`, and all of the traces from this program will be associated with a service name `node.js-quickstart`.
```js
// 3. Configure exporter to export traces to Zipkin.
tracer.registerSpanEventListener(new zipkin.ZipkinTraceExporter({
    url: 'http://localhost:9411/api/v2/spans',
    serviceName: 'node.js-quickstart'
}));
```

#### Create a span
To create a span in a trace, we used the `Tracer` to start a new span (4). A span must be closed in order to mark the end of the span.
```js
// 4. Create a scoped span, a scoped span will automatically end when closed.
tracer.startRootSpan({name: 'main'}, rootSpan => {
  for (let i = 0; i < 10; i++) {
    doWork(i);
  }

  rootSpan.end();
});
```

#### Create a child span
The `main` method calls `doWork` a number of times. Each invocation also generates a child span. Take a look at the `doWork` method.
```js
function doWork() {
  // 5. Start another span. In this example, the main method already started a span,
  // so that'll be the parent span, and this will be a child span.
  const span = tracer.startChildSpan('doWork');
  span.start();

  console.log('doing busy work');
  for (let i = 0; i <= 40000000; i++) {} // short delay

  // 6. Annotate our span to capture metadata about our operation
  span.addAnnotation('invoking doWork')
  for (let i = 0; i <= 20000000; i++) {} // short delay

  span.end();
}
```

#### End the spans
We must end the spans so they becomes available for exporting.
```js
// 6a. End the spans
span.end();

// 6b. End the spans
rootSpan.end();
```

#### Create an Annotation
An [annotation](https://opencensus.io/tracing/span/time_events/annotation/) tells a descriptive story in text of an event that occurred during a span’s lifetime.
```js
// 6. Annotate our span to capture metadata about our operation
span.addAnnotation('invoking doWork')
```
