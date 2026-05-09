# Asistencia QR - Aplicación Android

Aplicación móvil para gestionar asistencia de estudiantes mediante códigos QR. Desarrollada con Flutter.

## Características

- 📱 Escaneo de códigos QR
- 📊 Registro de asistencia en tiempo real
- ⚙️ Configuración remota del servidor
- 🔦 Control de linterna para mejor escaneo
- 📱 Interfaz intuitiva y fácil de usar

## Requisitos

### Para desarrollar
- Flutter SDK (>=3.0.0)
- Android SDK (mínimo API 21)
- Kotlin 1.7.10 o superior
- Un dispositivo Android o emulador

### Para ejecutar
- Android 5.0 (API 21) o superior
- Acceso a la red para conectar con el servidor Flask

## Instalación

### 1. Clonar o descargar el proyecto
```bash
cd asistencia_qr_flutter
```

### 2. Instalar dependencias
```bash
flutter pub get
```

### 3. Conectar dispositivo
```bash
flutter devices
```

### 4. Ejecutar la app
```bash
flutter run
```

### 5. Compilar APK
Para crear un APK listo para producción:
```bash
flutter build apk --release
```

El APK se encontrará en: `build/app/outputs/flutter-apk/app-release.apk`

## Configuración

### Conectar con el servidor Flask

1. Asegúrate que el servidor Flask está corriendo:
   ```bash
   python app.py
   ```

2. En la app, ve a **Configuración**

3. Ingresa la URL del servidor Flask:
   - En red local: `http://192.168.1.X:5000`
   - Cambia `192.168.1.X` por la IP de tu PC

4. Guarda la configuración

## Uso

### Escanear QR
1. Abre la app
2. Presiona "Escanear QR"
3. Apunta la cámara al código QR del estudiante
4. La asistencia se registrará automáticamente

### Activar linterna
- Presiona el botón de rayo en la esquina superior derecha para activar la linterna

## Estructura del Proyecto

```
lib/
├── main.dart           # Punto de entrada
├── models/            # Modelos de datos
│   ├── grade.dart
│   ├── student.dart
│   └── attendance_record.dart
├── services/          # Servicios (API, etc)
│   └── api_service.dart
└── screens/           # Pantallas de la app
    ├── home_screen.dart
    ├── scanner_screen.dart
    └── settings_screen.dart
```

## Dependencias Principales

- `mobile_scanner`: Escaneo de códigos QR
- `http`: Comunicación con API Flask
- `shared_preferences`: Almacenamiento local
- `provider`: Gestión de estado

## Troubleshooting

### La app no puede conectar con el servidor
- Verifica que el servidor Flask esté ejecutándose
- Asegúrate que ambos dispositivos están en la misma red
- Comprueba la URL configurada en Configuración

### La cámara no funciona
- Verifica que la app tiene permiso de cámara
- Reinicia la app
- Verifica en Configuración > Aplicaciones > Asistencia QR > Permisos

### El escaneo no detecta códigos
- Asegúrate que la linterna está activada si hay poca luz
- Acerca más el código QR a la cámara
- Intenta en una área mejor iluminada

## Versión del Backend

Esta app requiere una versión mejorada del backend con API REST. Consulta `../app.py` para las instrucciones de actualización.

## Licencia

Este proyecto es de código abierto.

## Autor

Desarrollado para simplificar la gestión de asistencia estudiantil.
