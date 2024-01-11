from fastapi import APIRouter



router = APIRouter(
    prefix='/auctions',
    tags=['Auctions']
)


@router.get("/")
async def all_auctions():
    return {'message':'All auctions!'}
