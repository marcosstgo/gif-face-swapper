import React, { useState, useEffect } from 'react'
import './App.css'

// Configuración para URLs
const getApiBaseUrl = () => {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:3000/api';
  }
  return window.location.origin + '/api';
};

const API_BASE_URL = getApiBaseUrl();

function App() {
  const [templates, setTemplates] = useState([])
  const [selectedTemplate, setSelectedTemplate] = useState(null)
  const [userImage, setUserImage] = useState(null)
  const [resultGif, setResultGif] = useState(null)
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')

  // Cargar templates al iniciar
  useEffect(() => {
    fetchTemplates()
  }, [])

  const fetchTemplates = async () => {
    try {
      console.log('🔍 Buscando templates en:', `${API_BASE_URL}/gif-templates`)
      const response = await fetch(`${API_BASE_URL}/gif-templates`)
      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`)
      }
      
      const data = await response.json()
      setTemplates(data)
      setMessage(`✅ ${data.length} templates cargados`)
      console.log('📦 Templates recibidos:', data)
    } catch (error) {
      console.error('❌ Error cargando templates:', error)
      setMessage('❌ Error cargando templates: ' + error.message)
    }
  }

  const handleImageUpload = (event) => {
    const file = event.target.files[0]
    if (file) {
      if (!file.type.startsWith('image/')) {
        setMessage('❌ Por favor sube una imagen válida')
        return
      }

      const reader = new FileReader()
      reader.onload = (e) => {
        setUserImage(e.target.result)
        setMessage('✅ Foto cargada correctamente')
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSwapFace = async () => {
    if (!selectedTemplate) {
      setMessage('❌ Por favor selecciona un GIF template')
      return
    }

    if (!userImage) {
      setMessage('❌ Por favor sube tu foto')
      return
    }

    setLoading(true)
    setMessage('🔄 Procesando tu GIF...')

    try {
      const formData = new FormData()
      
      const blob = await fetch(userImage).then(r => r.blob())
      const file = new File([blob], 'user_face.jpg', { type: 'image/jpeg' })
      
      formData.append('user_face', file)
      formData.append('gif_template', selectedTemplate)

      const result = await fetch(`${API_BASE_URL}/simple-swap`, {
        method: 'POST',
        body: formData,
      })

      if (!result.ok) {
        throw new Error(`Error HTTP: ${result.status}`)
      }

      const data = await result.json()
      
      if (data.success) {
        setResultGif(`${window.location.origin}${data.result_url}`)
        setMessage('✅ ¡Tu GIF está listo!')
      } else {
        setMessage('❌ Error procesando el GIF: ' + (data.message || 'Error desconocido'))
      }
    } catch (error) {
      console.error('❌ Error:', error)
      setMessage('❌ Error de conexión: ' + error.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>GIF Face Swapper</h1>
        <p>Cambia caras en GIFs con IA - Versión Pública</p>
        {message && <div className="message">{message}</div>}
      </header>

      <div className="app-container">
        {/* Paso 1: Seleccionar Template */}
        <section className="section">
          <h2>1. Elige un GIF Template</h2>
          <div className="templates-grid">
            {Array.isArray(templates) && templates.map(template => (
              <div
                key={template.id}
                className={`template-card ${selectedTemplate === template.id ? 'selected' : ''}`}
                onClick={() => {
                  setSelectedTemplate(template.id)
                  setMessage(`✅ Seleccionado: ${template.name}`)
                }}
              >
                <img 
                  src={`${window.location.origin}${template.thumbnail}`} 
                  alt={template.name}
                  onError={(e) => {
                    e.target.src = 'https://via.placeholder.com/150x150/667eea/white?text=GIF+Template'
                  }}
                />
                <span>{template.name}</span>
              </div>
            ))}
          </div>

          {(!Array.isArray(templates) || templates.length === 0) && (
            <div className="no-templates">
              <p>No hay templates disponibles o error cargando.</p>
              <button onClick={fetchTemplates} className="button">
                🔄 Recargar Templates
              </button>
              <button onClick={() => window.open(`${API_BASE_URL}/create-demos`, '_blank')} className="button">
                🎬 Crear Demos
              </button>
            </div>
          )}
        </section>

        {/* Paso 2: Subir Foto */}
        <section className="section">
          <h2>2. Sube Tu Foto</h2>
          <div className="upload-section">
            {userImage ? (
              <div className="image-preview">
                <img src={userImage} alt="Tu foto" />
                <button 
                  onClick={() => setUserImage(null)}
                  className="secondary-button"
                >
                  Cambiar Foto
                </button>
              </div>
            ) : (
              <label className="upload-area">
                <input
                  type="file"
                  accept="image/*"
                  onChange={handleImageUpload}
                  style={{ display: 'none' }}
                />
                <div className="upload-box">
                  <div className="upload-icon">📷</div>
                  <p>Haz clic para subir tu foto</p>
                  <small>JPEG, PNG - Máx 5MB</small>
                </div>
              </label>
            )}
          </div>
        </section>

        {/* Paso 3: Procesar */}
        <section className="section">
          <h2>3. Crear Tu GIF</h2>
          <button
            className={`process-button ${loading ? 'loading' : ''}`}
            onClick={handleSwapFace}
            disabled={!selectedTemplate || !userImage || loading}
          >
            {loading ? '⏳ Procesando...' : '✨ Crear Mi GIF'}
          </button>
          
          <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
            <p><strong>Debug Info:</strong></p>
            <p>API URL: {API_BASE_URL}</p>
            <p>Templates: {Array.isArray(templates) ? templates.length : 'Error'}</p>
            <p>Selected: {selectedTemplate || 'Ninguno'}</p>
          </div>
        </section>

        {/* Resultado */}
        {resultGif && (
          <section className="section result-section">
            <h2>🎉 ¡Tu GIF Personalizado!</h2>
            <div className="result-container">
              <img src={resultGif} alt="GIF resultado" className="result-gif" />
              <div className="result-actions">
                <a href={resultGif} download="mi_gif_personalizado.gif">
                  <button className="download-button">📥 Descargar GIF</button>
                </a>
                <button 
                  onClick={() => {
                    setResultGif(null)
                    setMessage('Listo para crear otro GIF')
                  }}
                  className="secondary-button"
                >
                  🆕 Crear Otro
                </button>
              </div>
            </div>
          </section>
        )}
      </div>

      <footer className="app-footer">
        <p>GIF Face Swapper v1.0 - Demo Pública | {window.location.hostname}</p>
      </footer>
    </div>
  )
}

export default App