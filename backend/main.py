from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.detect import router as detect_router
from app.routes.detect_ws import router as detect_ws_router

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(detect_router)
app.include_router(detect_ws_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)