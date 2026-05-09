import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/models.dart';

class ApiService {
  static String _baseUrl = 'http://192.168.1.100:5000';
  static const String _baseUrlKey = 'api_base_url';

  // Obtener la URL base guardada
  static Future<String> getBaseUrl() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_baseUrlKey) ?? _baseUrl;
  }

  // Configurar URL base
  static Future<void> setBaseUrl(String url) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_baseUrlKey, url);
    _baseUrl = url;
  }

  // Obtener todos los grados
  static Future<List<Grade>> getGrades() async {
    try {
      final url = await getBaseUrl();
      final response = await http.get(
        Uri.parse('$url/'),
      );

      if (response.statusCode == 200) {
        // Aquí se devuelve HTML, necesitamos parsear o usar un endpoint API
        throw Exception('Se debe crear endpoint API para grados');
      } else {
        throw Exception('Error al obtener grados');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  // Obtener estudiantes por grado
  static Future<List<Student>> getStudentsByGrade(int gradeId) async {
    try {
      final url = await getBaseUrl();
      final response = await http.get(
        Uri.parse('$url/api/students/$gradeId'),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => Student.fromJson(json)).toList();
      } else {
        throw Exception('Error al obtener estudiantes');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  // Registrar asistencia
  static Future<bool> registerAttendance(String studentCode) async {
    try {
      final url = await getBaseUrl();
      final response = await http.post(
        Uri.parse('$url/api/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'student_code': studentCode}),
      );

      if (response.statusCode == 200) {
        return true;
      } else {
        throw Exception('Error al registrar asistencia');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  // Obtener registros de asistencia
  static Future<List<AttendanceRecord>> getAttendanceRecords(int gradeId) async {
    try {
      final url = await getBaseUrl();
      final response = await http.get(
        Uri.parse('$url/api/attendance/$gradeId'),
      );

      if (response.statusCode == 200) {
        final List<dynamic> data = jsonDecode(response.body);
        return data.map((json) => AttendanceRecord.fromJson(json)).toList();
      } else {
        throw Exception('Error al obtener registros');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  // Crear grado
  static Future<Grade> createGrade(String name) async {
    try {
      final url = await getBaseUrl();
      final response = await http.post(
        Uri.parse('$url/api/grades'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'name': name}),
      );

      if (response.statusCode == 201) {
        return Grade.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Error al crear grado');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  // Agregar estudiante
  static Future<Student> addStudent(int gradeId, String name) async {
    try {
      final url = await getBaseUrl();
      final response = await http.post(
        Uri.parse('$url/api/students'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'grade_id': gradeId,
          'name': name,
        }),
      );

      if (response.statusCode == 201) {
        return Student.fromJson(jsonDecode(response.body));
      } else {
        throw Exception('Error al agregar estudiante');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }

  // Eliminar estudiante
  static Future<bool> deleteStudent(int studentId) async {
    try {
      final url = await getBaseUrl();
      final response = await http.delete(
        Uri.parse('$url/api/students/$studentId'),
      );

      if (response.statusCode == 200) {
        return true;
      } else {
        throw Exception('Error al eliminar estudiante');
      }
    } catch (e) {
      throw Exception('Error de conexión: $e');
    }
  }
}
