from fastapi import APIRouter

router = APIRouter()

@router.get("/raise-test", tags=["test"])
async def raise_test():
    raise RuntimeError("테스트용 강제 예외 (file)")
