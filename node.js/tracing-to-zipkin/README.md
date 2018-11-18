### Run it locally
1. Clone the example repository: `git clone https://github.com/hvent90/opencensus-quickstarts`
2. Change to the example directory: `cd opencensus-quickstarts/node.js`
3. Install dependencies: `npm install`
4. Download Zipkin: `curl -sSL https://zipkin.io/quickstart.sh | bash -s`
5. Start Zipkin: `java -jar zipkin.jar`
6. Run the code: `node tracingtozipkin.js`
7. Navigate to Zipkin Web UI: http://localhost:9411
8. Click Find Traces, and you should see a trace.
9. Click into that, and you should see the details.
