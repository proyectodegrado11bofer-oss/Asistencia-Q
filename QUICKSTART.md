# ⚡ Guía Rápida - Asistencia QR para Android

## 📋 Resumen

Tu app Flask ha sido convertida a una aplicación Android moderna usando **Flutter**. Aquí te mostramos cómo convertirla en APK e instalarla en tu dispositivo.

## 🎯 5 Pasos Principales

### 1️⃣ Actualizar el Backend Flask

Tu servidor actual necesita endpoints API REST para que la app Flutter funcione.

**Opción A: Reemplazar completo**
```bash
cp asistencia_qr_flutter/app_updated.py asistencia_qr/app.py
python asistencia_qr/app.py
```

**Opción B: Copiar solo los endpoints**
- Ve a `asistencia_qr_flutter/BACKEND_SETUP.md`
- Copia los endpoints `@app.route('/api/...')`
- Pégalos en tu `app.py`

### 2️⃣ Instalar Flutter

```bash
# 1. Descarga desde https://flutter.dev/docs/get-started/install/windows
# 2. Extrae en C:\flutter
# 3. Agrega C:\flutter\bin al PATH (Variables de entorno)
# 4. Reinicia PowerShell
# 5. Verifica:
flutter --version
flutter doctor
```

### 3️⃣ Compilar la App

En PowerShell, en la carpeta `asistencia_qr_flutter`:

```bash
# Instalar dependencias
flutter pub get

# Compilar APK (versión de pruebas)
flutter build apk

# O compilar APK final
flutter build apk --release
```

El archivo APK estará en:
```
build/app/outputs/flutter-apk/app-release.apk
```

### 4️⃣ Instalar en tu dispositivo

**Opción A: Con USB (recomendado)**
```bash
# Conecta tu Android por USB
# Habilita "Depuración USB" en Configuración > Opciones de desarrollador

adb install build/app/outputs/flutter-apk/app-release.apk
```

**Opción B: Descarga manual**
- Copia `app-release.apk` a tu dispositivo
- Toca el archivo para instalar

### 5️⃣ Usar la App

1. Abre "Asistencia QR" en tu Android
2. Ve a ⚙️ Configuración
3. Ingresa URL: `http://192.168.X.X:5000` (con la IP de tu PC)
4. ¡Escanea códigos QR!

## 📱 Archivos Importantes

```
asistencia_qr_flutter/
├── README.md              ← Documentación general
├── SETUP_APK.md          ← Guía detallada para crear APK
├── BACKEND_SETUP.md      ← Cómo actualizar el backend
├── app_updated.py        ← Backend con endpoints API listos
├── pubspec.yaml          ← Configuración del proyecto
└── lib/
    ├── main.dart         ← Punto de entrada
    ├── screens/          ← Pantallas de la app
    ├── models/           ← Estructuras de datos
    └── services/         ← Comunicación con API
```

## 🔧 Requisitos

- Windows 10+
- Flutter SDK
- Android SDK (min API 21)
- Dispositivo Android 5.0+ o emulador
- Servidor Flask ejecutándose

## ❓ Preguntas Comunes

### ¿Puedo compartir el APK?
**Sí**, el archivo `app-release.apk` se puede:
- Enviar por email
- Compartir por WhatsApp
- Subir a Google Drive
- Instalar en cualquier Android

### ¿Qué pasa si cambio la IP del servidor?
Ve a Configuración en la app y actualiza la URL.

### ¿La app funciona sin internet?
No, necesita conectar con el servidor Flask. Deben estar en la misma red.

### ¿Puedo instalar en iOS también?
Sí, el mismo código Flutter funciona para iOS. Solo necesitas macOS y Xcode.

## 📞 Soporte Rápido

| Problema | Solución |
|----------|----------|
| `flutter: command not found` | Agrega Flutter al PATH y reinicia |
| Cámara no funciona | Activa permiso en Configuración > Aplicaciones |
| No conecta con servidor | Verifica URL en Configuración, usa misma red |
| Build falla | `flutter clean` y luego `flutter build apk --release` |

## 🚀 Próximos Pasos

1. **Lee** `SETUP_APK.md` para instrucciones detalladas
2. **Lee** `BACKEND_SETUP.md` para actualizar el backend
3. **Ejecuta** los comandos de compilación
4. **Instala** en tu dispositivo
5. **Prueba** con los códigos QR de tus estudiantes

## 📊 Comparativa

| Aspecto | Antes (Web) | Ahora (Android) |
|---------|-----------|-----------------|
| Plataforma | Navegador | Aplicación nativa |
| Cámara | Webcam | Cámara del teléfono |
| Portabilidad | PC/Laptop | Cualquier Android |
| Velocidad | Depende de red | Más rápida |
| Interfaz | Web | Móvil optimizada |
| Linterna | No | Sí (activable) |

¡Ahora tienes tu app de asistencia en Android! 🎉
