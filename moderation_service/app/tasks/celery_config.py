from kombu import Exchange, Queue

broker_url = "amqp://guest:guest@localhost:5672//"

task_queues = [
    Queue(
        "moderation_queue",
        Exchange("moderation_exchange"),
        routing_key="moderation",
        queue_arguments={
            "x-dead-letter-exchange": "dlx",
            "x-dead-letter-routing-key": "dead_letter",
        },
    ),
]

task_default_queue = "moderation_queue"
task_default_exchange = "moderation_exchange"
task_default_routing_key = "moderation"

task_acks_late = True
