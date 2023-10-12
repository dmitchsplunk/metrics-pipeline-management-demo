# metrics-pipeline-management-demo

Prerequisites: 

- Python 3.x
- Splunk Distribution of OpenTelemetry Collector running on localhost 

git clone https://github.com/dmitchsplunk/metrics-pipeline-management-demo.git

cd metrics-pipeline-management-demo

python3 -m venv .

source ./bin/activate

pip install "splunk-opentelemetry[all]"

splunk-py-trace-bootstrap

export OTEL_SERVICE_NAME=metrics-pipeline-demo

splunk-py-trace python3 app.py