from fastapi import FastAPI
from .routers import user,auction, auction_constants
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title='AfriBids',
    version='1.0'
)

origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(user.router)
app.include_router(auction.router)
app.include_router(auction_constants.router)

@app.get("/")
async def root():
    return {'message':'Hello from AfriBids!!'}


