from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Đang học'),
        ('inactive', 'Tạm nghỉ'),
        ('graduated', 'Đã tốt nghiệp'),
        ('suspended', 'Bị đình chỉ'),
        ('on_leave', 'Nghỉ phép'),
    ]
    
    FACULTY_CHOICES = [
        ('cntt', 'Công nghệ thông tin'),
        ('kt', 'Kinh tế'),
        ('nn', 'Ngoại ngữ'),
        ('kh', 'Khoa học xã hội'),
        ('khac', 'Khác'),
    ]
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Tài khoản')
    student_id = models.AutoField(primary_key=True, verbose_name='Mã sinh viên')
    first_name = models.CharField(max_length=100, verbose_name='Tên')
    last_name = models.CharField(max_length=100, verbose_name='Họ')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Số điện thoại')
    date_of_birth = models.DateField(verbose_name='Ngày sinh')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Giới tính')
    address = models.TextField(verbose_name='Địa chỉ')
    city = models.CharField(max_length=100, verbose_name='Thành phố')
    state = models.CharField(max_length=100, verbose_name='Tỉnh/Thành')
    postal_code = models.CharField(max_length=20, verbose_name='Mã bưu điện')
    country = models.CharField(max_length=100, default='Việt Nam', verbose_name='Quốc gia')
    
    # Thông tin học tập
    enrollment_date = models.DateField(verbose_name='Ngày nhập học')
    graduation_date = models.DateField(null=True, blank=True, verbose_name='Ngày tốt nghiệp')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')
    major = models.CharField(max_length=100, verbose_name='Chuyên ngành')
    minor = models.CharField(max_length=100, blank=True, null=True, verbose_name='Chuyên ngành phụ')
    gpa = models.DecimalField(max_digits=3, decimal_places=2, default=0.00, verbose_name='Điểm trung bình')
    credits_earned = models.PositiveIntegerField(default=0, verbose_name='Số tín chỉ đã tích lũy')
    credits_attempted = models.PositiveIntegerField(default=0, verbose_name='Số tín chỉ đã đăng ký')
    
    # Thông tin liên hệ khẩn cấp
    emergency_contact_name = models.CharField(max_length=100, verbose_name='Tên người liên hệ khẩn cấp')
    emergency_contact_phone = models.CharField(max_length=15, verbose_name='Số điện thoại khẩn cấp')
    emergency_contact_relationship = models.CharField(max_length=50, verbose_name='Mối quan hệ')
    
    # Thông tin bổ sung
    profile_picture = models.ImageField(upload_to='student_profiles/', null=True, blank=True, verbose_name='Ảnh đại diện')
    student_id_card = models.CharField(max_length=20, unique=True, verbose_name='Mã thẻ sinh viên')
    blood_type = models.CharField(max_length=5, blank=True, null=True, verbose_name='Nhóm máu')
    medical_conditions = models.TextField(blank=True, null=True, verbose_name='Tình trạng sức khỏe')
    allergies = models.TextField(blank=True, null=True, verbose_name='Dị ứng')
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày xóa')
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='deleted_students', verbose_name='Người xóa')
    is_deleted = models.BooleanField(default=False, verbose_name='Đã xóa')
    
    # Quan hệ
    class_assigned = models.ManyToManyField('app_class.Class', related_name='students', blank=True, verbose_name='Lớp học')
    subjects = models.ManyToManyField('app_subject.Subject', related_name='students', blank=True, verbose_name='Môn học')
    scores = models.ManyToManyField('app_score.Score', related_name='students', blank=True, verbose_name='Điểm số')
    
    # Cập nhật tên trường
    faculty = models.CharField(max_length=50, choices=FACULTY_CHOICES, verbose_name='Khoa')
    is_active = models.BooleanField(default=True, verbose_name='Đang hoạt động')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_students')
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def calculate_gpa(self):
        # Triển khai tính điểm trung bình
        pass
    
    class Meta:
        verbose_name = "Sinh viên"
        verbose_name_plural = "Sinh viên"
        ordering = ['last_name', 'first_name']
        permissions = [
            ("can_view_student_details", "Có thể xem thông tin sinh viên"),
            ("can_manage_student", "Có thể quản lý sinh viên"),
            ("can_view_student_grades", "Có thể xem điểm sinh viên"),
            ("can_manage_student_enrollment", "Có thể quản lý đăng ký của sinh viên"),
        ]

    @property
    def full_name(self):
        return self.get_full_name()
