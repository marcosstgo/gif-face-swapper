from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
import os
from pathlib import Path
import shutil
import uuid
from PIL import Image, ImageDraw
import math

app = FastAPI(title="GIF Face Swap Public App")

# Permitir todos los orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar directorios
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs" 
TEMPLATES_DIR = BASE_DIR / "templates"
FRONTEND_DIR = BASE_DIR.parent / "frontend" / "dist"

# Crear directorios si no existen
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Servir archivos estáticos del frontend
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    @app.get("/")
    def root():
        return {"message": "Frontend no construido. Ejecuta 'npm run build' en frontend/"}

# Montar directorios estáticos
app.mount("/templates", StaticFiles(directory=TEMPLATES_DIR), name="templates")

# ========== FUNCIONES DE GIFs ==========
def create_soccer_celebration():
    """Crear GIF de celebración de futbol"""
    try:
        frames = []
        size = (200, 200)
        
        for i in range(4):
            img = Image.new('RGB', size, 'green')
            draw = ImageDraw.Draw(img)
            
            # Líneas del campo
            draw.rectangle([10, 10, 190, 190], outline='white', width=2)
            draw.line([100, 10, 100, 190], fill='white', width=2)
            draw.ellipse([80, 80, 120, 120], outline='white', width=2)
            
            # Personaje
            body_color = 'blue' if i % 2 == 0 else 'darkblue'
            head_y = 70 + (i * 5)
            draw.ellipse([90, head_y, 110, head_y+20], fill='beige', outline='black')
            
            # Brazos
            arm_angle = i * 20
            draw.line([95, 90, 85 - arm_angle//10, 70], fill=body_color, width=3)
            draw.line([105, 90, 115 + arm_angle//10, 70], fill=body_color, width=3)
            
            # Cuerpo y piernas
            draw.rectangle([95, 90, 105, 130], fill=body_color)
            leg_offset = (i - 1) * 8
            draw.line([100, 130, 90 + leg_offset, 160], fill='darkblue', width=3)
            draw.line([100, 130, 110 - leg_offset, 160], fill='darkblue', width=3)
            
            # Pelota
            ball_x = 120 + (i * 15)
            draw.ellipse([ball_x, 140, ball_x+10, 150], fill='white')
            
            frames.append(img)
        
        output_path = TEMPLATES_DIR / "soccer_celebration.gif"
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=200, loop=0)
        return True
    except Exception as e:
        print(f"Error creando soccer: {e}")
        return False

def create_dancer_gif():
    """Crear GIF de bailarín"""
    try:
        frames = []
        size = (200, 200)
        
        for i in range(6):
            img = Image.new('RGB', size, 'purple')
            draw = ImageDraw.Draw(img)
            
            head_x = 100 + (i-2) * 3
            draw.ellipse([head_x-15, 50, head_x+15, 80], fill='beige')
            draw.ellipse([head_x-8, 60, head_x-4, 64], fill='black')
            draw.ellipse([head_x+4, 60, head_x+8, 64], fill='black')
            
            mouth_y = 72 if i % 2 == 0 else 74
            draw.arc([head_x-6, mouth_y, head_x+6, mouth_y+4], 0, 180, fill='red', width=2)
            
            body_color = 'red' if i % 3 == 0 else 'darkred'
            draw.rectangle([head_x-10, 80, head_x+10, 120], fill=body_color)
            
            arm_angle = i * 30
            arm1_x = 80 + int(20 * math.sin(math.radians(arm_angle)))
            arm2_x = 120 - int(20 * math.sin(math.radians(arm_angle)))
            
            draw.line([head_x-10, 90, arm1_x, 70], fill=body_color, width=4)
            draw.line([head_x+10, 90, arm2_x, 70], fill=body_color, width=4)
            
            leg_offset = int(15 * math.sin(math.radians(arm_angle * 2)))
            draw.line([head_x-5, 120, head_x-15, 150 + leg_offset], fill='blue', width=4)
            draw.line([head_x+5, 120, head_x+15, 150 - leg_offset], fill='blue', width=4)
            
            frames.append(img)
        
        output_path = TEMPLATES_DIR / "dancer.gif"
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=150, loop=0)
        return True
    except Exception as e:
        print(f"Error creando dancer: {e}")
        return False

def create_singer_gif():
    """Crear GIF de cantante"""
    try:
        frames = []
        size = (200, 200)
        
        for i in range(5):
            img = Image.new('RGB', size, 'darkblue')
            draw = ImageDraw.Draw(img)
            
            # Micrófono
            draw.ellipse([140, 60, 160, 80], fill='gray')
            draw.line([150, 80, 150, 120], fill='gray', width=3)
            
            # Cabeza
            draw.ellipse([80, 50, 120, 90], fill='beige')
            
            # Boca
            mouth_open = i % 2 == 0
            if mouth_open:
                draw.ellipse([95, 75, 105, 85], fill='red')
            else:
                draw.line([95, 80, 105, 80], fill='red', width=2)
            
            # Ojos
            draw.ellipse([88, 60, 92, 64], fill='black')
            draw.ellipse([108, 60, 112, 64], fill='black')
            
            # Cuerpo
            draw.rectangle([85, 90, 115, 130], fill='gold')
            
            # Brazos
            arm_move = i * 5
            draw.line([85, 100, 65 - arm_move, 110], fill='gold', width=4)
            draw.line([115, 100, 135 + arm_move, 90], fill='gold', width=4)
            
            frames.append(img)
        
        output_path = TEMPLATES_DIR / "singer.gif"
        frames[0].save(output_path, save_all=True, append_images=frames[1:], duration=300, loop=0)
        return True
    except Exception as e:
        print(f"Error creando singer: {e}")
        return False

# ========== ENDPOINTS API ==========

@app.get("/api/health")
def health():
    return {"status": "public", "message": "App pública funcionando"}

@app.get("/api/gif-templates")
async def get_gif_templates():
    """Obtener templates disponibles"""
    templates = []
    
    # Crear templates si no existen
    if not list(TEMPLATES_DIR.glob("*.gif")):
        print("Creando templates de demostración...")
        create_soccer_celebration()
        create_dancer_gif()
        create_singer_gif()
    
    for file in TEMPLATES_DIR.glob("*.gif"):
        templates.append({
            "id": file.stem,
            "name": file.stem.replace("_", " ").title(),
            "thumbnail": f"/templates/{file.name}",
            "gif_path": f"/templates/{file.name}",
            "category": "general"
        })
    
    print(f"Devolviendo {len(templates)} templates")
    return templates

@app.post("/api/simple-swap")
async def simple_face_swap(user_face: UploadFile = File(...), gif_template: str = Form(...)):
    """Procesar GIF con cara del usuario"""
    
    if not user_face.content_type.startswith('image/'):
        raise HTTPException(400, "El archivo debe ser una imagen")
    
    file_id = str(uuid.uuid4())
    user_face_path = UPLOAD_DIR / f"{file_id}_face.jpg"
    output_gif_path = OUTPUT_DIR / f"{file_id}_result.gif"
    
    try:
        # Guardar imagen
        with open(user_face_path, "wb") as buffer:
            content = await user_face.read()
            buffer.write(content)
        
        # Usar template
        template_path = TEMPLATES_DIR / f"{gif_template}.gif"
        if not template_path.exists():
            gif_files = list(TEMPLATES_DIR.glob("*.gif"))
            if gif_files:
                template_path = gif_files[0]
            else:
                raise HTTPException(404, "No hay templates disponibles")
        
        # Copiar GIF (placeholder)
        shutil.copy2(template_path, output_gif_path)
        
        return {
            "success": True,
            "message": "GIF procesado!",
            "result_url": f"/api/download/{output_gif_path.name}",
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error: {str(e)}")
    finally:
        if user_face_path.exists():
            user_face_path.unlink()

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Descargar resultado"""
    file_path = OUTPUT_DIR / filename
    if not file_path.exists():
        raise HTTPException(404, "Archivo no encontrado")
    
    return FileResponse(file_path, filename=f"mi_gif_{filename}")

# Endpoint para crear templates manualmente
@app.get("/api/create-demos")
async def create_demos():
    """Crear templates manualmente"""
    try:
        create_soccer_celebration()
        create_dancer_gif()
        create_singer_gif()
        return {"success": True, "message": "Templates creados"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    print("🚀 Iniciando aplicación pública en http://0.0.0.0:3000")
    print("🌐 Accesible desde: http://TU_IP_PUBLICA:3000")
    print("📱 Y localmente: http://localhost:3000")
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")