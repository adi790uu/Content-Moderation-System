from prometheus_client import Counter, Gauge

REQUEST_COUNT = Counter("api_requests_total", "Total number of API requests")
HEALTH_STATUS = Gauge(
    "api_health_status",
    "Health status of the API Gateway",
)
