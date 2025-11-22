@echo off
echo 🚀 Instalando GIF Face Swapper para Windows...

:: Crear entorno virtual
python -m venv venv
echo ✅ Entorno virtual creado

:: Activar entorno virtual
call venv\Scripts\activate

:: Instalar dependencias básicas
pip install --upgrade pip setuptools wheel

:: Instalar dependencias una por una
pip install fastapi==0.104.1
pip install uvicorn==0.24.0
pip install python-multipart==0.0.6
pip install opencv-python==4.8.1.78
pip install pillow==10.1.0
pip install numpy==1.24.3
pip install aiofiles==23.2.1

echo ✅ Dependencias del backend instaladas

:: Crear directorios necesarios
mkdir backend\uploads 2>nul
mkdir backend\outputs 2>nul
mkdir backend\templates 2>nul
mkdir backend\models 2>nul

echo ✅ Directorios creados
echo.
echo 📁 Coloca tus GIFs templates en backend\templates\
echo 🎬 Para ejecutar el backend: uvicorn main:app --reload --port 8000
echo.
pause