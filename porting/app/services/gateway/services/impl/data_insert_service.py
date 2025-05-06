from app.services.gateway.services.interfaces.data_insert_interface import DataInsertInterface
from app.services.data.client import DataServiceClient
from typing import Dict, Any

class DataInsertService(DataInsertInterface):
    async def insert(self, table: str, payload: Dict[str, Any]) -> Dict[str, str]:
        # 실제로는 gRPC/HTTP 등으로 data 서비스에 요청
        # 여기서는 HTTP 비동기 예시
        return await DataServiceClient().insert(table, payload)
