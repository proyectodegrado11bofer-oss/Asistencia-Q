import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import '../services/api_service.dart';

class ScannerScreen extends StatefulWidget {
  const ScannerScreen({Key? key}) : super(key: key);

  @override
  State<ScannerScreen> createState() => _ScannerScreenState();
}

class _ScannerScreenState extends State<ScannerScreen> {
  late MobileScannerController controller;
  bool isProcessing = false;

  @override
  void initState() {
    super.initState();
    controller = MobileScannerController();
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  Future<void> _handleScannedCode(String code) async {
    if (isProcessing) return;

    setState(() {
      isProcessing = true;
    });

    try {
      // Extraer el código del estudiante del QR
      String studentCode = code;
      if (code.contains('code=')) {
        studentCode = code.split('code=').last;
      }

      final success = await ApiService.registerAttendance(studentCode);

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: const Text('¡Asistencia registrada exitosamente!'),
            backgroundColor: Colors.green,
            duration: const Duration(seconds: 2),
          ),
        );

        // Permitir escanear otro después de 2 segundos
        await Future.delayed(const Duration(seconds: 2));
        if (mounted) {
          setState(() {
            isProcessing = false;
          });
        }
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Error: ${e.toString()}'),
            backgroundColor: Colors.red,
            duration: const Duration(seconds: 3),
          ),
        );
        setState(() {
          isProcessing = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Escanear Código QR'),
        backgroundColor: Colors.blue[700],
      ),
      body: Stack(
        children: [
          MobileScanner(
            controller: controller,
            onDetect: (capture) {
              if (!isProcessing) {
                final List<Barcode> barcodes = capture.barcodes;
                for (final barcode in barcodes) {
                  if (barcode.rawValue != null) {
                    _handleScannedCode(barcode.rawValue!);
                  }
                }
              }
            },
          ),
          Positioned(
            top: 20,
            right: 20,
            child: FloatingActionButton(
              mini: true,
              onPressed: () => controller.toggleTorch(),
              backgroundColor: Colors.blue[700],
              child: const Icon(Icons.flashlight_on),
            ),
          ),
          Positioned(
            bottom: 0,
            left: 0,
            right: 0,
            child: Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: Colors.black.withOpacity(0.7),
                borderRadius: const BorderRadius.only(
                  topLeft: Radius.circular(20),
                  topRight: Radius.circular(20),
                ),
              ),
              child: Text(
                isProcessing ? 'Procesando...' : 'Acerca el código QR a la cámara',
                style: const TextStyle(
                  color: Colors.white,
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
                textAlign: TextAlign.center,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
