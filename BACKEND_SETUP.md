# Actualización del Backend Flask para API REST

Para que la aplicación Flutter funcione correctamente, necesitas actualizar tu backend Flask con endpoints API REST.

## Cambios necesarios en `app.py`

Agrega los siguientes endpoints a tu `app.py` existente:

```python
from flask import jsonify

# Endpoint para obtener todos los grados
@app.route('/api/grades', methods=['GET'])
def api_get_grades():
    conn = get_db()
    grades = conn.execute('SELECT * FROM grades ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(g) for g in grades])

# Endpoint para crear un grado
@app.route('/api/grades', methods=['POST'])
def api_create_grade():
    data = request.get_json()
    grade_name = data.get('name')
    
    if not grade_name:
        return jsonify({'error': 'Nombre del grado requerido'}), 400
    
    try:
        conn = get_db()
        conn.execute('INSERT INTO grades (name) VALUES (?)', (grade_name,))
        conn.commit()
        
        # Obtener el grado creado
        new_grade = conn.execute('SELECT * FROM grades WHERE name = ?', (grade_name,)).fetchone()
        conn.close()
        return jsonify(dict(new_grade)), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El grado ya existe'}), 409

# Endpoint para obtener estudiantes por grado
@app.route('/api/students/<int:grade_id>', methods=['GET'])
def api_get_students(grade_id):
    conn = get_db()
    students = conn.execute('''
        SELECT s.id, s.name, s.grade_id, s.code, COUNT(a.id) as attendance_count
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        WHERE s.grade_id = ?
        GROUP BY s.id
        ORDER BY s.name
    ''', (grade_id,)).fetchall()
    conn.close()
    return jsonify([dict(s) for s in students])

# Endpoint para crear un estudiante
@app.route('/api/students', methods=['POST'])
def api_create_student():
    data = request.get_json()
    grade_id = data.get('grade_id')
    student_name = data.get('name')
    
    if not student_name:
        return jsonify({'error': 'Nombre del estudiante requerido'}), 400
    
    student_code = str(uuid.uuid4())[:8].upper()
    
    try:
        conn = get_db()
        conn.execute('INSERT INTO students (name, grade_id, code) VALUES (?, ?, ?)',
                    (student_name, grade_id, student_code))
        conn.commit()
        
        # Obtener el estudiante creado
        new_student = conn.execute('SELECT * FROM students WHERE code = ?', (student_code,)).fetchone()
        conn.close()
        return jsonify(dict(new_student)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint para registrar asistencia (versión API)
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    student_code = data.get('student_code')
    
    if not student_code:
        return jsonify({'error': 'Código de estudiante requerido'}), 400
    
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE code = ?', (student_code.upper(),)).fetchone()
    
    if not student:
        conn.close()
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    
    # Verificar si el estudiante ya fue registrado hoy
    today = datetime.now().strftime('%Y-%m-%d')
    existing_today = conn.execute('''
        SELECT a.id FROM attendance a
        WHERE a.student_id = ? AND datetime(a.timestamp) >= ?
    ''', (student['id'], today)).fetchone()
    
    if existing_today:
        conn.close()
        return jsonify({
            'error': 'Ya registrado',
            'message': f'{student["name"]} ya fue registrado hoy'
        }), 409
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn.execute('INSERT INTO attendance (student_id, timestamp) VALUES (?, ?)',
                    (student['id'], timestamp))
        conn.commit()
        conn.close()
        return jsonify({
            'success': True,
            'message': f'Asistencia registrada para {student["name"]}'
        }), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

# Endpoint para obtener registros de asistencia
@app.route('/api/attendance/<int:grade_id>', methods=['GET'])
def api_get_attendance(grade_id):
    conn = get_db()
    records = conn.execute('''
        SELECT a.id, s.name, s.code, a.timestamp
        FROM attendance a
        JOIN students s ON a.student_id = s.id
        WHERE s.grade_id = ?
        ORDER BY a.timestamp DESC
    ''', (grade_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in records])

# Endpoint para eliminar estudiante (versión API)
@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    if not student:
        conn.close()
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    
    try:
        conn.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
        conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': f'Estudiante eliminado'}), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500
```

## Instalación

1. Agrega estos endpoints a tu archivo `app.py`
2. Reinicia el servidor Flask:
   ```bash
   python app.py
   ```

## Verificación

Puedes probar los endpoints con curl:

```bash
# Obtener grados
curl http://192.168.1.X:5000/api/grades

# Crear grado
curl -X POST http://192.168.1.X:5000/api/grades \
  -H "Content-Type: application/json" \
  -d '{"name": "1ro A"}'

# Registrar asistencia
curl -X POST http://192.168.1.X:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"student_code": "ABC123XY"}'
```

## Notas Importantes

- Los endpoints API devuelven JSON en lugar de HTML
- Mantienen la misma lógica de validación
- Son compatibles con la app Flutter
- Los endpoints web originales (que devuelven HTML) pueden seguir existiendo para acceso por navegador
