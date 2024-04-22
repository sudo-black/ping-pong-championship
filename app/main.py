import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import referee, player, auth

app = FastAPI()

# CORS (Cross-Origin Resource Sharing) settings if needed
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Update with specific origins if necessary
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],
# )

# Include authentication routes
app.include_router(auth.router)

# Include referee routes
app.include_router(referee.router)

# Include player routes
app.include_router(player.router)


@app.get("/health")
async def root():
    return {"message": "I'm, alive!!!"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=4000)
