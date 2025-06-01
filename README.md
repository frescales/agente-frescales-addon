# Agente FRESCALES – Add-on para Home Assistant

🧠 **Agente FRESCALES** es un complemento personalizado para Home Assistant que permite el control inteligente de sistemas agrícolas a través de sensores, actuadores y lógica autónoma basada en IA.

> Desarrollado para monitoreo, control de riego, iluminación, automatización basada en humedad, clima, y más.

---

## 🚀 Características principales

- Acceso completo a entidades de Home Assistant (switches, luces, scripts, scenes)
- Control manual y automático del sistema de riego
- Integración con sensores reales o simulados
- Acceso a datos históricos desde InfluxDB
- API REST documentada vía Swagger (`/docs`)
- Integración con Supabase y Tailscale
- Totalmente local, sin depender de Nabu Casa ni servicios externos

---

## 📦 Requisitos

- Home Assistant OS (recomendado)
- Docker habilitado (si se instala manualmente)
- InfluxDB configurado y accesible
- Clave de acceso larga de Home Assistant (para control de entidades)

---

## 🧰 Instalación desde GitHub

1. Abre Home Assistant
2. Ve a **Supervisor → Add-on Store**
3. Haz clic en **⋮ (tres puntos)** → **Repositorios**
4. Agrega esta URL:

https://github.com/frescales/agente-frescales-addon


5. Instala el complemento “Agente FRESCALES”
6. Inicia el complemento y haz clic en el botón **Abrir Interfaz Web**

---

## 📘 Documentación interactiva

Una vez iniciado, accede a:

http://TU-IP-LOCAL:8000/docs


Aquí puedes:

- Probar comandos (`GET`, `POST`)
- Encender/apagar luces y riego
- Leer estados de sensores
- Ejecutar lógica desde un frontend visual

---

## 🔐 Seguridad

Para proteger la interacción con Home Assistant, se requiere un **Long-Lived Access Token**, el cual debe configurarse en el archivo `.env` con:

```env

Estructura del proyecto
HA_BASE_URL=http://172.30.32.1:8123
HA_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6...


agente-frescales-addon/
├── repository.yaml
├── agente_frescales/
│   ├── config.yaml
│   ├── Dockerfile
│   ├── main.py
│   └── ...

👨‍💻 Autor
Oscar Peña
FRESCALES C.A.
📧 oscar@frescales.com

🪪 Licencia
Este proyecto es libre para uso educativo y privado. Contactar al autor para licencias comerciales o extensiones personalizadas.
