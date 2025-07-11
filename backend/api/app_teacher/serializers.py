from rest_framework import serializers
from .models import Teacher
import re


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"
        read_only_fields = ["teacher_id", "created_at", "updated_at"]

    # def validate_email(self, value):
    #     """Kiểm tra định dạng email hợp lệ."""
    #     if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
    #         raise serializers.ValidationError("Email không hợp lệ.")
    #     return value

    # def validate_phone(self, value):
    #     """Kiểm tra định dạng số điện thoại (phù hợp với số VN: 10 chữ số, bắt đầu bằng 0 hoặc +84)."""
    #     if not re.match(r'^(0|\+84)\d{9}$', value):
    #         raise serializers.ValidationError("Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại Việt Nam (10 chữ số, bắt đầu bằng 0 hoặc +84).")
    #     return value

    # def validate_first_name(self, value):
    #     """Kiểm tra first_name không rỗng."""
    #     if not value.strip():
    #         raise serializers.ValidationError("Tên không được để trống.")
    #     return value

    # def validate_last_name(self, value):
    #     """Kiểm tra last_name không rỗng."""
    #     if not value.strip():
    #         raise serializers.ValidationError("Họ không được để trống.")
    #     return value

    # def validate_specialization(self, value):
    #     """Kiểm tra specialization không rỗng."""
    #     if not value.strip():
    #         raise serializers.ValidationError("Chuyên ngành không được để trống.")
    #     return value

    # def validate_degree(self, value):
    #     """Kiểm tra degree hợp lệ."""
    #     if value not in dict(Teacher.DEGREE_CHOICES).keys():
    #         raise serializers.ValidationError("Học vị không hợp lệ.")
    #     return value

    # def validate_status(self, value):
    #     """Kiểm tra status hợp lệ."""
    #     if value not in dict(Teacher.STATUS_CHOICES).keys():
    #         raise serializers.ValidationError("Trạng thái không hợp lệ.")
    #     return value

    # def validate_years_of_experience(self, value):
    #     """Kiểm tra years_of_experience là số không âm."""
    #     if value < 0:
    #         raise serializers.ValidationError("Số năm kinh nghiệm không được nhỏ hơn 0.")
    #     return value

    # def validate(self, data):
    #     """Kiểm tra thêm các ràng buộc liên quan."""
    #     # Kiểm tra teacher_id duy nhất khi tạo mới
    #     if not self.instance and 'teacher_id' in data:
    #         if Teacher.objects.filter(teacher_id=data['teacher_id']).exists():
    #             raise serializers.ValidationError({"teacher_id": "Mã giảng viên đã tồn tại."})

    #     # Kiểm tra email duy nhất
    #     if 'email' in data and Teacher.objects.exclude(teacher_id=data.get('teacher_id', '')).filter(email=data['email']).exists():
    #         raise serializers.ValidationError({"email": "Email đã được sử dụng."})

    #     # Kiểm tra phone duy nhất
    #     if 'phone' in data and Teacher.objects.exclude(teacher_id=data.get('teacher_id', '')).filter(phone=data['phone']).exists():
    #         raise serializers.ValidationError({"phone": "Số điện thoại đã được sử dụng."})

    #     return data
