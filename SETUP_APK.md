# 🚀 Guía Completa: Convertir a APK para Android

Esta guía te llevará paso a paso para compilar la app Flutter en un archivo APK listo para instalar en Android.

## Paso 1: Instalar Flutter

### Windows
1. Descarga Flutter desde: https://flutter.dev/docs/get-started/install/windows
2. Extrae el archivo descargado (ej: `C:\flutter`)
3. Agrega Flutter al PATH:
   - Abre "Variables de entorno" (Environment Variables)
   - Edita la variable PATH
   - Agrega: `C:\flutter\bin`
   - Agrega: `C:\flutter\bin\cache\dart-sdk\bin`

4. Abre una terminal PowerShell y ejecuta:
   ```bash
   flutter --version
   ```

5. Ejecuta el doctor de Flutter:
   ```bash
   flutter doctor
   ```

## Paso 2: Instalar Android SDK

1. Descarga Android Studio desde: https://developer.android.com/studio
2. Instala Android Studio (elige ruta por defecto)
3. Abre Android Studio y completa la instalación
4. En Preferences > Appearance & Behavior > System Settings > Android SDK:
   - Selecciona: SDK Platform 34 (o superior)
   - Selecciona: Google Play Services
   - Click en "Apply" y "OK"

## Paso 3: Aceptar licencias de Android

En PowerShell, ejecuta:
```bash
flutter doctor --android-licenses
```

Presiona `y` para aceptar todas las licencias.

## Paso 4: Preparar el proyecto

1. Abre PowerShell en la carpeta `asistencia_qr_flutter`
2. Ejecuta:
   ```bash
   flutter pub get
   ```

3. Verifica que todo está bien:
   ```bash
   flutter doctor
   ```

## Paso 5: Configurar la app

Antes de compilar, actualiza el backend Flask (ve a BACKEND_SETUP.md):

```bash
# En tu PC donde está el servidor Flask
python app.py
```

## Paso 6: Compilar APK

### Opción A: APK de debug (para pruebas)
```bash
flutter build apk
```

El APK se guardará en:
```
build/app/outputs/flutter-apk/app-debug.apk
```

### Opción B: APK de release (para producción)
```bash
flutter build apk --release
```

El APK se guardará en:
```
build/app/outputs/flutter-apk/app-release.apk
```

## Paso 7: Instalar en el dispositivo

### Opción A: Instalación directa con adb
```bash
# Conecta el dispositivo Android por USB
# Habilita "Depuración USB" en Configuración > Opciones de desarrollador

adb install build/app/outputs/flutter-apk/app-release.apk
```

### Opción B: Instalación manual
1. Copia el archivo `app-release.apk` al dispositivo
2. Toca el archivo APK para instalar
3. Confirma la instalación

### Opción C: Ejecutar en emulador
```bash
flutter emulators --launch <emulator_name>
flutter run --release
```

## Paso 8: Usar la app

1. Abre la app "Asistencia QR"
2. Ve a Configuración
3. Ingresa la URL de tu servidor Flask:
   ```
   http://192.168.X.X:5000
   ```
   (Reemplaza con la IP de tu PC)

4. ¡Comienza a escanear códigos QR!

## 📱 Compartir la app

El archivo `app-release.apk` puede:
- Enviarse por correo
- Compartirse por WhatsApp
- Subirse a Google Play Store (requiere cuenta de desarrollador)
- Distribuirse por Telegram, Drive, etc.

## 🐛 Solución de Problemas

### "flutter: command not found"
- Asegúrate que Flutter está en el PATH
- Reinicia PowerShell después de actualizar PATH
- Reinicia tu PC

### "Android SDK not found"
```bash
flutter config --android-sdk-path "C:\Program Files\Android\Sdk"
```

### "No connected devices"
- Conecta el dispositivo Android por USB
- Habilita "Depuración USB" en el dispositivo
- Ejecuta: `adb devices`

### "Build failed"
1. Limpia el proyecto:
   ```bash
   flutter clean
   ```
2. Obtén dependencias nuevamente:
   ```bash
   flutter pub get
   ```
3. Intenta compilar de nuevo:
   ```bash
   flutter build apk --release
   ```

## 📊 Información de la app

- **Nombre**: Asistencia QR
- **Versión**: 1.0.0
- **Tamaño aproximado**: 50-80 MB
- **API mínima**: Android 5.0 (API 21)
- **Permisos**: Cámara, Internet

## 🔒 Seguridad

Para distribución en producción:
1. Crea una clave de firma (keystore):
   ```bash
   keytool -genkey -v -keystore ~/key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias key
   ```

2. Crea `android/key.properties`:
   ```
   storePassword=tu_password
   keyPassword=tu_password
   keyAlias=key
   storeFile=key.jks
   ```

3. Compila con firma:
   ```bash
   flutter build apk --release
   ```

## 📞 Soporte

Si tienes problemas:
1. Verifica que el servidor Flask está ejecutándose
2. Comprueba la URL de conexión
3. Verifica que ambos dispositivos están en la misma red
4. Revisa los logs: `flutter logs`
