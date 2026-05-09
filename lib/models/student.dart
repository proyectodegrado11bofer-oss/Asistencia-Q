class Student {
  final int id;
  final String name;
  final int gradeId;
  final String code;
  final int? attendanceCount;

  Student({
    required this.id,
    required this.name,
    required this.gradeId,
    required this.code,
    this.attendanceCount,
  });

  factory Student.fromJson(Map<String, dynamic> json) {
    return Student(
      id: json['id'] as int,
      name: json['name'] as String,
      gradeId: json['grade_id'] as int,
      code: json['code'] as String,
      attendanceCount: json['attendance_count'] as int?,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'grade_id': gradeId,
      'code': code,
      'attendance_count': attendanceCount,
    };
  }
}
