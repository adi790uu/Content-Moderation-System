from prometheus_client import Counter, Gauge

REQUEST_COUNT = Counter("api_requests_total", "Total number of API requests")
GATEWAY_HEALTH_STATUS = Gauge(
    "api_gateway_health_status",
    "Health status of the API Gateway",
)

MODERATION_SERVICE_HEALTH_STATUS = Gauge(
    "moderation_service_health_status",
    "Health status of the Moderation Service",
)
