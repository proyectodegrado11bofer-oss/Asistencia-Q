class AttendanceRecord {
  final int id;
  final String studentName;
  final String studentCode;
  final DateTime timestamp;

  AttendanceRecord({
    required this.id,
    required this.studentName,
    required this.studentCode,
    required this.timestamp,
  });

  factory AttendanceRecord.fromJson(Map<String, dynamic> json) {
    return AttendanceRecord(
      id: json['id'] as int,
      studentName: json['name'] as String,
      studentCode: json['code'] as String,
      timestamp: DateTime.parse(json['timestamp'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': studentName,
      'code': studentCode,
      'timestamp': timestamp.toIso8601String(),
    };
  }
}
