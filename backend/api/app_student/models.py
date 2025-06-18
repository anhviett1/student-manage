from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import date
from django.utils.translation import gettext_lazy as _

from ..app_home.models import Department, User

User = get_user_model()

class Student(models.Model):
    """
    Model đại diện cho sinh viên trong hệ thống
    Kế thừa từ BaseModel để có các trường cơ bản
    """
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
    
    # Thông tin cơ bản
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    student_id = models.CharField(max_length=20, unique=True, verbose_name=_('Student ID'))
    first_name = models.CharField(
        max_length=100,
        verbose_name='Tên',
        default='Tên'
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name='Họ',
        default='Họ'
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        default='student@example.com'
    )
    phone = models.CharField(
        max_length=15,
        blank=True,
        verbose_name='Số điện thoại',
        default=''
    )
    date_of_birth = models.DateField(
        verbose_name='Ngày sinh',
        default=date.today,
        help_text='Định dạng: YYYY-MM-DD'
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name='Giới tính',
        default='M'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Đang hoạt động'
    )
    
    # Thông tin địa chỉ
    address = models.TextField(
        verbose_name='Địa chỉ',
        default='Địa chỉ mặc định'
    )
    city = models.CharField(
        max_length=100,
        verbose_name='Thành phố',
        default='Hà Nội'
    )
    state = models.CharField(
        max_length=100,
        verbose_name='Tỉnh/Thành',
        default='Hà Nội'
    )
    postal_code = models.CharField(
        max_length=20,
        verbose_name='Mã bưu điện',
        default='100000'
    )
    country = models.CharField(
        max_length=100,
        default='Việt Nam',
        verbose_name='Quốc gia'
    )
    
    # Thông tin học tập
    enrollment_date = models.DateField(verbose_name=_('Enrollment Date'))
    graduation_date = models.DateField(null=True, blank=True, verbose_name=_('Graduation Date'))
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Đang học'),
            ('graduated', 'Đã tốt nghiệp'),
            ('suspended', 'Bị đình chỉ'),
            ('withdrawn', 'Đã rút học bạ'),
        ],
        default='active',
        verbose_name=_('Status')
    )
    major = models.CharField(
        max_length=100,
        verbose_name='Chuyên ngành',
        default='Chưa xác định'
    )
    minor = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Chuyên ngành phụ'
    )
    gpa = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        verbose_name='Điểm trung bình'
    )
    credits_earned = models.PositiveIntegerField(
        default=0,
        verbose_name='Số tín chỉ đã tích lũy'
    )
    credits_attempted = models.PositiveIntegerField(
        default=0,
        verbose_name='Số tín chỉ đã đăng ký'
    )
    
    # Thông tin liên hệ khẩn cấp
    emergency_contact_name = models.CharField(
        max_length=100,
        verbose_name='Tên người liên hệ khẩn cấp',
        default='Người thân'
    )
    emergency_contact_phone = models.CharField(
        max_length=15,
        verbose_name='Số điện thoại khẩn cấp',
        default='0123456789'
    )
    emergency_contact_relationship = models.CharField(
        max_length=50,
        verbose_name='Mối quan hệ',
        default='Gia đình'
    )
    
    # Thông tin bổ sung
    profile_picture = models.ImageField(
        upload_to='student_profiles/',
        null=True,
        blank=True,
        verbose_name='Ảnh đại diện'
    )
    student_id_card = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Mã thẻ sinh viên',
        default='SV001'
    )
    blood_type = models.CharField(
        max_length=5,
        blank=True,
        null=True,
        verbose_name='Nhóm máu'
    )
    medical_conditions = models.TextField(
        blank=True,
        null=True,
        verbose_name='Tình trạng sức khỏe'
    )
    allergies = models.TextField(
        blank=True,
        null=True,
        verbose_name='Dị ứng'
    )
    
    # Thông tin hệ thống
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo', null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Ngày cập nhật')
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name='Ngày xóa')
    is_deleted = models.BooleanField(default=False, verbose_name='Đã xóa')
    
    # Quan hệ
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    class_assigned = models.ManyToManyField(
        'app_class.Class',
        related_name='student_classes',
        blank=True,
        verbose_name='Lớp học'
    )
    subjects = models.ManyToManyField(
        'app_subject.Subject',
        related_name='student_subjects',
        blank=True,
        verbose_name='Môn học'
    )
    scores = models.ManyToManyField(
        'app_score.Score',
        related_name='student_score_sets',
        blank=True,
        verbose_name='Điểm số'
    )
    
    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name()}"
    
    def get_full_name(self):
        """Lấy họ và tên đầy đủ của sinh viên"""
        return f"{self.first_name} {self.last_name}"
    
    def calculate_gpa(self):
        """Tính điểm trung bình của sinh viên"""
        if not self.scores.exists():
            return 0.00
        
        total_points = 0
        total_credits = 0
        
        for score in self.scores.all():
            if score.grade_point and score.subject.credits:
                total_points += score.grade_point * score.subject.credits
                total_credits += score.subject.credits
        
        if total_credits > 0:
            self.gpa = round(total_points / total_credits, 2)
            self.save(update_fields=['gpa'])
        
        return self.gpa
    
    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['student_id']
        permissions = [
            ("can_view_student_details", "Có thể xem thông tin sinh viên"),
            ("can_manage_student", "Có thể quản lý sinh viên"),
            ("can_view_student_grades", "Có thể xem điểm sinh viên"),
            ("can_manage_student_enrollment", "Có thể quản lý đăng ký của sinh viên"),
        ]
    
    @property
    def full_name(self):
        """Property để lấy họ và tên đầy đủ"""
        return self.get_full_name()