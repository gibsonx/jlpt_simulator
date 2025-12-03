import os

from celery import Celery
from graphs.common.TaskRunner import TaskRunner
from graphs.common.Schema import ExamType
from dotenv import load_dotenv
load_dotenv()

#################################################
# Azure Service Bus connection (Basic/Standard) #
#################################################
# Replace with your values
# NAMESPACE = "jlpt-mq.servicebus.windows.net"
# QUEUE_NAME = "jlpt"
# SAS_POLICY = "RootManageSharedAccessKey"
# SAS_KEY = os.environ['MQ_SAS_KEY']
#
# # Broker URL using AMQP transport
# broker_url = f"azureservicebus://{SAS_POLICY}:{SAS_KEY}@{NAMESPACE}/{QUEUE_NAME}?ssl=True"
#
# # For results, still use Redis (or DB) – Service Bus does not store results
# RESULTS_DB = os.path.join(os.environ['PROJECT_PATH'], "celery_results.sqlite")
#
# backend_url = f"db+sqlite:///{RESULTS_DB}"

# Redis connection values
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ['MQ_SAS_KEY']

# Redis URI (password optional)
redis_base = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

# Use separate DBs
broker_url = f"{redis_base}/0"   # Celery broker messages
backend_url = f"{redis_base}/1"  # Celery results storage

celery = Celery(
    "exam_runner",
    broker=broker_url,
    backend=backend_url,
)

celery.conf.update(
    task_acks_late=False,                 # ACK at task receipt → never run twice
    task_reject_on_worker_lost=False,     # do NOT requeue if worker dies
    task_acks_on_failure_or_timeout=False,
    broker_transport_options={
        "visibility_timeout": 3600 * 48,       # safe window, but irrelevant with acks_late=False
        "retry_on_startup": False,
        "worker_prefetch_multiplier": 1
    },
    broker_connection_retry_on_startup=False,
)

@celery.task(bind=True)
def run_exam_task(self, level: str, exam_type: ExamType):
    task_uuid = self.request.id
    runner = TaskRunner(level=level, exam_type=exam_type, task_id=task_uuid)
    runner.run()