from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routes import router

init_db()

app = FastAPI()

# Servir les fichiers statiques
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer les routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)