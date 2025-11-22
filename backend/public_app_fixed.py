import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# ... (todo tu código existente)

if __name__ == "__main__":
    # Railway asigna el puerto automáticamente
    port = int(os.getenv("PORT", 3000))
    host = "0.0.0.0"
    
    print(f"🚀 Iniciando en {host}:{port}")
    uvicorn.run(
        app, 
        host=host, 
        port=port,
        # Configuración optimizada para producción
        access_log=False,
        timeout_keep_alive=5
    )