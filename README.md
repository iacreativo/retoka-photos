---
title: Retoka · Fotos de Identificación México
emoji: 🪪
colorFrom: gray
colorTo: blue
sdk: gradio
sdk_version: 6.19.0
app_file: app.py
pinned: false
license: apache-2.0
short_description: Fotos de identificación mexicanas con IA
---

# Retoka · Fotos de Identificación México

Genera fotos tipo credencial, pasaporte o visa para trámites mexicanos a partir de una foto del niño o adulto. Usa el modelo `hivision_modnet` para segmentar el retrato y reemplaza el fondo por el color oficial requerido (blanco, azul, gris).

## Características

- Tamaños preconfigurados para México: infantil/credencial, pasaporte, visa
- Modelos de segmentación intercambiables
- Detección de rostro con `mtcnn`
- Login protegido por contraseña (Gradio `auth`)
- UI en español con soporte multi-idioma

## Uso

1. Abre la URL del Space
2. Inicia sesión con las credenciales que configuraste
3. Sube una foto frontal con buena luz
4. Elige tamaño y color de fondo
5. Descarga el resultado

## Variables de entorno (opcional)

Configúralas en **Settings → Variables and secrets** del Space:

| Variable | Default | Descripción |
|---|---|---|
| `RETOKA_USER` | `admin` | Usuario principal |
| `RETOKA_PASS` | `retoka2026` | Contraseña principal |
| `RETOKA_USERS` | (vacío) | Usuarios extra: `user1:pass1,user2:pass2` |