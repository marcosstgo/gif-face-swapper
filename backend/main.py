from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
import uuid
from pathlib import Path
import shutil
import math
from PIL import Image, ImageDraw

# ✅ PRIMERO definir la app, LUEGO los endpoints
app = FastAPI(title="GIF Face Swap API", version="1.0.0")

# Configurar CORS para el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar directorios (compatible con Windows)
BASE_DIR = Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs" 
TEMPLATES_DIR = BASE_DIR / "templates"

# Crear directorios si no existen
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Montar directorio estático para templates
app.mount("/templates", StaticFiles(directory=TEMPLATES_DIR), name="templates")

# ========== FUNCIONES AUXILIARES ==========
def create_soccer_celebration():
    """Crear GIF de celebración de futbol"""
    try:
        frames = []
        size = (200, 200)
        
        # Crear 4 frames de animación
        for i in range(4):
            img = Image.new('RGB', size, 'green')  # Campo de futbol verde
            draw = ImageDraw.Draw(img)
            
            # Dibujar líneas del campo
            draw.rectangle([10, 10, 190, 190], outline='white', width=2)
            draw.line([100, 10, 100, 190], fill='white', width=2)
            draw.ellipse([80, 80, 120, 120], outline='white', width=2)
            
            # Figura animada (personaje)
            body_color = 'blue' if i % 2 == 0 else 'darkblue'
            
            # Cabeza
            head_y = 70 + (i * 5)  # Movimiento vertical
            draw.ellipse([90, head_y, 110, head_y+20], fill='beige', outline='black')
            
            # Brazos (movimiento de celebración)
            arm_angle = i * 20
            draw.line([95, 90, 85 - arm_angle//10, 70], fill=body_color, width=3)
            draw.line([105, 90, 115 + arm_angle//10, 70], fill=body_color, width=3)
            
            # Cuerpo
            draw.rectangle([95, 90, 105, 130], fill=body_color)
            
            # Piernas
            leg_offset = (i - 1) * 8
            draw.line([100, 130, 90 + leg_offset, 160], fill='darkblue', width=3)
            draw.line([100, 130, 110 - leg_offset, 160], fill='darkblue', width=3)
            
            # Pelota
            ball_x = 120 + (i * 15)
            draw.ellipse([ball_x, 140, ball_x+10, 150], fill='white')
            
            frames.append(img)
        
        # Guardar GIF
        output_path = TEMPLATES_DIR / "soccer_celebration.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=200,  # ms entre frames
            loop=0,        # loop infinito
            optimize=True
        )
        return True
    except Exception as e:
        print(f"Error creando soccer celebration: {e}")
        return False

def create_dancer_gif():
    """Crear GIF de bailarín"""
    try:
        frames = []
        size = (200, 200)
        
        for i in range(6):
            img = Image.new('RGB', size, 'purple')
            draw = ImageDraw.Draw(img)
            
            # Cabeza
            head_x = 100 + (i-2) * 3  # Movimiento lateral suave
            draw.ellipse([head_x-15, 50, head_x+15, 80], fill='beige')
            
            # Ojos
            draw.ellipse([head_x-8, 60, head_x-4, 64], fill='black')
            draw.ellipse([head_x+4, 60, head_x+8, 64], fill='black')
            
            # Boca (sonrisa que cambia)
            mouth_y = 72 if i % 2 == 0 else 74
            draw.arc([head_x-6, mouth_y, head_x+6, mouth_y+4], 0, 180, fill='red', width=2)
            
            # Cuerpo
            body_color = 'red' if i % 3 == 0 else 'darkred'
            draw.rectangle([head_x-10, 80, head_x+10, 120], fill=body_color)
            
            # Brazos de bailarín
            arm_angle = i * 30
            arm1_x = 80 + int(20 * math.sin(math.radians(arm_angle)))
            arm2_x = 120 - int(20 * math.sin(math.radians(arm_angle)))
            
            draw.line([head_x-10, 90, arm1_x, 70], fill=body_color, width=4)
            draw.line([head_x+10, 90, arm2_x, 70], fill=body_color, width=4)
            
            # Piernas bailando
            leg_offset = int(15 * math.sin(math.radians(arm_angle * 2)))
            draw.line([head_x-5, 120, head_x-15, 150 + leg_offset], fill='blue', width=4)
            draw.line([head_x+5, 120, head_x+15, 150 - leg_offset], fill='blue', width=4)
            
            frames.append(img)
        
        output_path = TEMPLATES_DIR / "dancer.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=150,
            loop=0,
            optimize=True
        )
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
            
            # Cabeza del cantante
            draw.ellipse([80, 50, 120, 90], fill='beige')
            
            # Boca cantando (abre y cierra)
            mouth_open = i % 2 == 0
            if mouth_open:
                # Boca abierta (cantando)
                draw.ellipse([95, 75, 105, 85], fill='red')
            else:
                # Boca cerrada
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
            
            # Notas musicales que aparecen
            if i >= 2:
                for note_i in range(i-1):
                    note_x = 50 + note_i * 20
                    draw.ellipse([note_x, 40, note_x+8, 48], fill='white')
                    draw.line([note_x+8, 44, note_x+15, 35], fill='white', width=2)
            
            frames.append(img)
        
        output_path = TEMPLATES_DIR / "singer.gif"
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            duration=300,
            loop=0,
            optimize=True
        )
        return True
    except Exception as e:
        print(f"Error creando singer: {e}")
        return False

def create_simple_demo_gifs():
    """Crear GIFs simples de demostración"""
    try:
        # GIF 1: Colores cambiantes
        frames1 = []
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange']
        for color in colors:
            img = Image.new('RGB', (150, 150), color)
            frames1.append(img)
        
        demo1_path = TEMPLATES_DIR / "demo_colors.gif"
        frames1[0].save(
            demo1_path,
            save_all=True,
            append_images=frames1[1:],
            duration=300,
            loop=0
        )
        
        # GIF 2: Círculo moviéndose
        frames2 = []
        for i in range(8):
            img = Image.new('RGB', (150, 150), 'white')
            draw = ImageDraw.Draw(img)
            x = 30 + (i * 15)
            draw.ellipse([x, 60, x+30, 90], fill='blue')
            frames2.append(img)
        
        demo2_path = TEMPLATES_DIR / "demo_moving.gif"
        frames2[0].save(
            demo2_path,
            save_all=True,
            append_images=frames2[1:],
            duration=200,
            loop=0
        )
        
        return True
    except Exception as e:
        print(f"Error creando demos simples: {e}")
        return False

# ========== ENDPOINTS ==========

@app.get("/")
async def root():
    return {"message": "GIF Face Swap API está funcionando! 🚀"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.get("/gif-templates")
async def get_gif_templates():
    """Obtener lista de GIF templates disponibles"""
    
    templates = []
    
    # Buscar archivos GIF en el directorio de templates
    for file in TEMPLATES_DIR.glob("*.gif"):
        template_data = {
            "id": file.stem,
            "name": file.stem.replace("_", " ").title(),
            "thumbnail": f"/templates/{file.name}",
            "gif_path": f"/templates/{file.name}",
            "category": "general"
        }
        templates.append(template_data)
    
    # Si no hay templates, crearlos automáticamente
    if not templates:
        print("No hay templates, creando demos automáticamente...")
        create_soccer_celebration()
        create_dancer_gif()
        create_singer_gif()
        
        # Buscar nuevamente
        for file in TEMPLATES_DIR.glob("*.gif"):
            template_data = {
                "id": file.stem,
                "name": file.stem.replace("_", " ").title(),
                "thumbnail": f"/templates/{file.name}",
                "gif_path": f"/templates/{file.name}",
                "category": "general"
            }
            templates.append(template_data)
    
    return templates

@app.get("/create-demos")
async def create_demos_get():
    """Endpoint GET para crear demos (fácil desde navegador)"""
    try:
        # Crear los GIFs
        soccer_success = create_soccer_celebration()
        dancer_success = create_dancer_gif() 
        singer_success = create_singer_gif()
        
        if soccer_success and dancer_success and singer_success:
            return {
                "success": True,
                "message": "GIFs de demostración creados exitosamente",
                "templates": [
                    {"id": "soccer_celebration", "name": "Celebración de Futbol"},
                    {"id": "dancer", "name": "Bailarín"},
                    {"id": "singer", "name": "Cantante"}
                ]
            }
        else:
            # Si fallan los GIFs complejos, crear simples
            simple_success = create_simple_demo_gifs()
            if simple_success:
                return {
                    "success": True,
                    "message": "GIFs simples creados exitosamente",
                    "templates": [
                        {"id": "demo_colors", "name": "Colores Cambiantes"},
                        {"id": "demo_moving", "name": "Círculo en Movimiento"}
                    ]
                }
            else:
                return {"success": False, "error": "No se pudieron crear los GIFs"}
    
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/create-demo-gifs")
async def create_demo_gifs():
    """Endpoint POST para crear demos"""
    return await create_demos_get()

@app.post("/upload-template")
async def upload_template(file: UploadFile = File(...)):
    """Endpoint para subir nuevos GIF templates (admin)"""
    
    if not file.filename.lower().endswith('.gif'):
        raise HTTPException(400, "Solo se permiten archivos GIF")
    
    # Guardar el template
    file_path = TEMPLATES_DIR / file.filename
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {"message": f"Template {file.filename} subido exitosamente"}

@app.post("/simple-swap")
async def simple_face_swap(
    user_face: UploadFile = File(...),
    gif_template: str = Form(...)
):
    """Versión simple del cambio de cara - procesamiento básico"""
    
    # Validar que sea una imagen
    if not user_face.content_type.startswith('image/'):
        raise HTTPException(400, "El archivo debe ser una imagen")
    
    # Generar ID único para este proceso
    file_id = str(uuid.uuid4())
    user_face_path = UPLOAD_DIR / f"{file_id}_face.jpg"
    output_gif_path = OUTPUT_DIR / f"{file_id}_result.gif"
    
    try:
        # Guardar imagen del usuario
        with open(user_face_path, "wb") as buffer:
            content = await user_face.read()
            buffer.write(content)
        
        # Verificar que el template existe
        template_path = TEMPLATES_DIR / f"{gif_template}.gif"
        
        if not template_path.exists():
            # Si no existe, usar el primer GIF disponible
            gif_files = list(TEMPLATES_DIR.glob("*.gif"))
            if gif_files:
                template_path = gif_files[0]
            else:
                raise HTTPException(404, "No hay templates GIF disponibles")
        
        # Copiar el GIF template como resultado (placeholder por ahora)
        shutil.copy2(template_path, output_gif_path)
        
        return {
            "success": True,
            "message": "GIF procesado (modo demo - próximamente IA real)",
            "result_url": f"/download/{output_gif_path.name}",
            "file_id": file_id
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error procesando: {str(e)}")
    
    finally:
        # Limpiar archivo temporal de la cara
        if user_face_path.exists():
            user_face_path.unlink()

@app.get("/download/{filename}")
async def download_file(filename: str):
    """Descargar archivo resultante"""
    file_path = OUTPUT_DIR / filename
    
    if not file_path.exists():
        raise HTTPException(404, "Archivo no encontrado")
    
    return FileResponse(
        path=file_path,
        filename=f"custom_gif_{filename}",
        media_type='image/gif'
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)