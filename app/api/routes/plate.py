from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_plates():
    return {"message": "Hello World"}
