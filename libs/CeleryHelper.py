import os

from celery import Celery
from graphs.common.TaskRunner import TaskRunner
from graphs.common.Schema import ExamType


# Azure Service Bus connection (Basic/Standard)
# Replace with your values
NAMESPACE = "jlpt-mq.servicebus.windows.net"
QUEUE_NAME = "jlpt"
SAS_POLICY = "RootManageSharedAccessKey"
SAS_KEY = os.environ['MQ_SAS_KEY']

# Broker URL using AMQP transport
broker_url = f"azureservicebus://{SAS_POLICY}:{SAS_KEY}@{NAMESPACE}/{QUEUE_NAME}?ssl=True"

# For results, still use Redis (or DB) – Service Bus does not store results
RESULTS_DB = os.path.join(os.environ['PROJECT_PATH'], "celery_results.sqlite")

backend_url = f"db+sqlite:///{RESULTS_DB}"

celery = Celery(
    "exam_runner",
    broker=broker_url,
    backend=backend_url
)

# Optional: auto-retry configuration for tasks
celery.conf.task_default_retry_delay = 5  # seconds between retries
celery.conf.task_annotations = {
    '*': {'max_retries': 3, 'autoretry_for': (Exception,), 'retry_backoff': True}
}

@celery.task
def run_exam_task(level: str, exam_type:ExamType, task_uuid: str):
    """
    Celery task wrapping the run_exam function.
    """
    runner = TaskRunner(level=level, exam_type=exam_type, task_id=task_uuid)
    runner.run()