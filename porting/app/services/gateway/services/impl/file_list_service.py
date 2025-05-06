from app.services.gateway.services.interfaces.file_list_interface import FileListInterface
from app.services.file.services.interfaces.list_query_interface import ListQueryInterface
from app.core.logging import get_tracer, capture_and_log

tracer = get_tracer("gateway::list_files")

class FileListService(FileListInterface):
    @capture_and_log(tracer)
    async def list_files(self, prefix: str):
        service = ListQueryInterface.get_service()
        return await service.list_files(prefix)
