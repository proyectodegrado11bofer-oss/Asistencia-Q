# app_updated.py - Versión actualizada con endpoints API REST

"""
Este archivo contiene todos los endpoints necesarios para que la app Flutter funcione.
Puedes:
1. Reemplazar tu app.py con este archivo
2. O copiar solo los endpoints API y pegarlos en tu app.py existente
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import qrcode
import io
import base64
import uuid
import socket
import sqlite3
from datetime import datetime
from pathlib import Path

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'

DATABASE = 'database.db'

# Detectar IP local
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

LOCAL_IP = get_local_ip()

# Inicializar base de datos
def init_db():
    if not Path(DATABASE).exists():
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''CREATE TABLE grades
                     (id INTEGER PRIMARY KEY, name TEXT UNIQUE)''')
        c.execute('''CREATE TABLE students
                     (id INTEGER PRIMARY KEY, name TEXT, grade_id INTEGER, code TEXT UNIQUE, FOREIGN KEY(grade_id) REFERENCES grades(id))''')
        c.execute('''CREATE TABLE attendance
                     (id INTEGER PRIMARY KEY, student_id INTEGER, timestamp TEXT, FOREIGN KEY(student_id) REFERENCES students(id))''')
        conn.commit()
        conn.close()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def generate_qr(student_code):
    qr_url = f'http://{LOCAL_IP}:5000/scan?code={student_code}'
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

init_db()

# ==================== ENDPOINTS WEB (HTML) ====================
# Estos endpoints devuelven HTML para acceso por navegador

@app.route('/')
def index():
    conn = get_db()
    grades = conn.execute('SELECT * FROM grades ORDER BY name').fetchall()
    conn.close()
    return render_template('index.html', grades=grades)

@app.route('/grades', methods=['POST'])
def add_grade():
    grade_name = request.form.get('grade_name')
    if not grade_name:
        flash('Nombre del grado requerido')
        return redirect(url_for('index'))
    
    try:
        conn = get_db()
        conn.execute('INSERT INTO grades (name) VALUES (?)', (grade_name,))
        conn.commit()
        conn.close()
        flash(f'Grado "{grade_name}" creado exitosamente')
    except sqlite3.IntegrityError:
        flash('El grado ya existe')
    
    return redirect(url_for('index'))

@app.route('/students/<int:grade_id>')
def students_by_grade(grade_id):
    conn = get_db()
    grade = conn.execute('SELECT * FROM grades WHERE id = ?', (grade_id,)).fetchone()
    students = conn.execute('SELECT * FROM students WHERE grade_id = ? ORDER BY name', (grade_id,)).fetchall()
    conn.close()
    
    if not grade:
        flash('Grado no encontrado')
        return redirect(url_for('index'))
    
    students_with_qr = []
    for student in students:
        qr_base64 = generate_qr(student['code'])
        students_with_qr.append({
            'id': student['id'],
            'name': student['name'],
            'code': student['code'],
            'qr': qr_base64
        })
    
    return render_template('students.html', grade=grade, students=students_with_qr)

@app.route('/students/add/<int:grade_id>', methods=['GET', 'POST'])
def add_student(grade_id):
    conn = get_db()
    grade = conn.execute('SELECT * FROM grades WHERE id = ?', (grade_id,)).fetchone()
    conn.close()
    
    if not grade:
        flash('Grado no encontrado')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        if not student_name:
            flash('Nombre del estudiante requerido')
            return redirect(url_for('add_student', grade_id=grade_id))
        
        student_code = str(uuid.uuid4())[:8].upper()
        
        try:
            conn = get_db()
            conn.execute('INSERT INTO students (name, grade_id, code) VALUES (?, ?, ?)',
                        (student_name, grade_id, student_code))
            conn.commit()
            conn.close()
            flash(f'Estudiante "{student_name}" agregado exitosamente')
            return redirect(url_for('students_by_grade', grade_id=grade_id))
        except Exception as e:
            flash(f'Error: {str(e)}')
    
    return render_template('student_form.html', grade=grade)

@app.route('/scan')
def scan():
    student_code = request.args.get('code')
    return render_template('scan.html', student_code=student_code)

@app.route('/register', methods=['POST'])
def register():
    student_code = request.form.get('student_code')
    
    if not student_code:
        flash('Código de estudiante requerido')
        return redirect(url_for('scan'))
    
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE code = ?', (student_code.upper(),)).fetchone()
    
    if not student:
        flash('Estudiante no encontrado')
        conn.close()
        return redirect(url_for('scan'))
    
    today = datetime.now().strftime('%Y-%m-%d')
    existing_today = conn.execute('''
        SELECT a.id FROM attendance a
        WHERE a.student_id = ? AND datetime(a.timestamp) >= ?
    ''', (student['id'], today)).fetchone()
    
    if existing_today:
        flash(f'{student["name"]} ya fue registrado hoy')
        conn.close()
        return redirect(url_for('scan'))
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn.execute('INSERT INTO attendance (student_id, timestamp) VALUES (?, ?)',
                    (student['id'], timestamp))
        conn.commit()
        flash(f'Asistencia registrada para {student["name"]}')
    except Exception as e:
        flash(f'Error al registrar: {str(e)}')
    finally:
        conn.close()
    
    return redirect(url_for('scan', code=student_code))

@app.route('/students/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (student_id,)).fetchone()
    
    if not student:
        flash('Estudiante no encontrado')
        conn.close()
        return redirect(url_for('index'))
    
    grade_id = student['grade_id']
    
    try:
        conn.execute('DELETE FROM attendance WHERE student_id = ?', (student_id,))
        conn.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        flash(f'Estudiante "{student["name"]}" eliminado exitosamente')
    except Exception as e:
        flash(f'Error al eliminar: {str(e)}')
    finally:
        conn.close()
    
    return redirect(url_for('students_by_grade', grade_id=grade_id))

@app.route('/admin')
def admin():
    conn = get_db()
    grades = conn.execute('SELECT * FROM grades ORDER BY name').fetchall()
    
    data = {}
    for grade in grades:
        students = conn.execute('''
            SELECT s.id, s.name, s.code, COUNT(a.id) as attendance_count
            FROM students s
            LEFT JOIN attendance a ON s.id = a.student_id
            WHERE s.grade_id = ?
            GROUP BY s.id
            ORDER BY s.name
        ''', (grade['id'],)).fetchall()
        
        attendance_records = conn.execute('''
            SELECT a.id, s.name, s.code, a.timestamp
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE s.grade_id = ?
            ORDER BY a.timestamp DESC
        ''', (grade['id'],)).fetchall()
        
        data[grade['name']] = {
            'students': students,
            'records': attendance_records
        }
    
    conn.close()
    return render_template('admin.html', data=data)

# ==================== ENDPOINTS API REST ====================
# Estos endpoints devuelven JSON para la app Flutter

@app.route('/api/grades', methods=['GET'])
def api_get_grades():
    """Obtener todos los grados"""
    conn = get_db()
    grades = conn.execute('SELECT * FROM grades ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(g) for g in grades])

@app.route('/api/grades', methods=['POST'])
def api_create_grade():
    """Crear un nuevo grado"""
    data = request.get_json()
    grade_name = data.get('name')
    
    if not grade_name:
        return jsonify({'error': 'Nombre del grado requerido'}), 400
    
    try:
        conn = get_db()
        conn.execute('INSERT INTO grades (name) VALUES (?)', (grade_name,))
        conn.commit()
        
        new_grade = conn.execute('SELECT * FROM grades WHERE name = ?', (grade_name,)).fetchone()
        conn.close()
        return jsonify(dict(new_grade)), 201
    except sqlite3.IntegrityError:
        return jsonify({'error': 'El grado ya existe'}), 409

@app.route('/api/students/<int:grade_id>', methods=['GET'])
def api_get_students(grade_id):
    """Obtener estudiantes de un grado"""
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

@app.route('/api/students', methods=['POST'])
def api_create_student():
    """Crear un nuevo estudiante"""
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
        
        new_student = conn.execute('SELECT * FROM students WHERE code = ?', (student_code,)).fetchone()
        conn.close()
        return jsonify(dict(new_student)), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/register', methods=['POST'])
def api_register():
    """Registrar asistencia (versión API)"""
    data = request.get_json()
    student_code = data.get('student_code')
    
    if not student_code:
        return jsonify({'error': 'Código de estudiante requerido'}), 400
    
    conn = get_db()
    student = conn.execute('SELECT * FROM students WHERE code = ?', (student_code.upper(),)).fetchone()
    
    if not student:
        conn.close()
        return jsonify({'error': 'Estudiante no encontrado'}), 404
    
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

@app.route('/api/attendance/<int:grade_id>', methods=['GET'])
def api_get_attendance(grade_id):
    """Obtener registros de asistencia de un grado"""
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

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    """Eliminar un estudiante (versión API)"""
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
        return jsonify({'success': True, 'message': 'Estudiante eliminado'}), 200
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f'Servidor ejecutándose en http://{LOCAL_IP}:5000')
    print(f'Usa esta URL en la app Flutter: http://{LOCAL_IP}:5000')
    app.run(host='0.0.0.0', debug=True)
