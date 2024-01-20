from fastapi import FastAPI
from .routers import user,auction, auction_constants




app = FastAPI(
    title='AfriBids',
    version='1.0'
)


app.include_router(user.router)
app.include_router(auction.router)
app.include_router(auction_constants.router)

@app.get("/")
async def root():
    return {'message':'Hello from AfriBids!!'}


