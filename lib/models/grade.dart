class Grade {
  final int id;
  final String name;

  Grade({
    required this.id,
    required this.name,
  });

  factory Grade.fromJson(Map<String, dynamic> json) {
    return Grade(
      id: json['id'] as int,
      name: json['name'] as String,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
    };
  }
}
