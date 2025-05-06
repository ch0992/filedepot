from app.services.data.services.interfaces.table_insert_service_interface import TableInsertServiceInterface
from app.common.broker.interfaces.message_producer_interface import MessageProducerInterface
from opentelemetry import trace
from app.services.log.exceptions import capture_and_log
from typing import Dict, Any

tracer = trace.get_tracer("data")

class TableInsertService(TableInsertServiceInterface):
    def __init__(self, producer: MessageProducerInterface):
        self._producer = producer

    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, str]:
        topic = f"iceberg-insert-{table}"
        try:
            with tracer.start_as_current_span("data.table_insert") as span:
                await self._producer.produce(topic, payload)
                span.set_attribute("kafka.topic", topic)
                return {"status": "queued", "topic": topic}
        except Exception as e:
            capture_and_log(e, trace.get_current_span())
            raise
