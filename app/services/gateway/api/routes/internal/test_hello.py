from fastapi import APIRouter

router = APIRouter()

@router.get("/internal-test/hello", summary="헬로우 테스트 API", tags=["internal"], description="단순 헬로우 월드 반환.")
async def hello():
    return {"message": "hello world"}
