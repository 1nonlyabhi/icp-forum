from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.db.models.base import Model
from django.db.models.fields.related import ForeignKey
from django.forms.fields import DateField
from django.utils.translation import ugettext_lazy as _
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator



def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year()+4)(value)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollno = models.IntegerField(null=True)
    usertype = models.CharField(max_length=15, default="Student")
    firstname = models.CharField(max_length=32, blank=False, null=True)
    lastname = models.CharField(max_length=32, blank=True, null=True)
    verified = models.BooleanField(default=False)
    bio = models.TextField(max_length=1024, blank=True, null=True)
    extraskills = models.CharField(max_length=255, blank=True)
    techskills = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    github = models.URLField(blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(default='default.png', upload_to='uploads/profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def birthyear(self):
        return self.birth_date.strftime('%Y')

    @property
    def followers(self):
        return Follow.objects.filter(follow_user=self.user).count()

    @property
    def following(self):
        return Follow.objects.filter(user=self.user).count()
    

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.firstname == None:
            self.firstname = self.user.username
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Follow(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    follow_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)




class Education(models.Model):
    
    class Degree(models.TextChoices):
        BTECH = 'B.Tech', _('B.Tech')
        DIPLOMA = 'Diploma', _('Diploma')
        INTERMEDIATE = 'Intermediate', _('Intermediate')
        HIGHSCHOOL = 'High School', _('High School')

    class Field(models.TextChoices):
        COMPUTER = 'Computer Science & Engineering', _('Computer Science & Engineering')
        CIVIL = 'Civil Engineering', _('Civil Engineering')
        ELECTRONICS = 'Electronics and Communication', _('Electronics and Communication')
        MECHANICAL = 'Mechanical Engineering', _('Mechanical Engineering')
        SCIENCE = 'Applied Science', _('Applied Science')
        MATHS = 'Mathematics Major', _('Mathematics Major')


    school = models.CharField(max_length=255, blank=False, null=True)
    degree = models.CharField(max_length=15, choices=Degree.choices, default=Degree.BTECH)
    field = models.CharField(max_length=30, choices=Field.choices, default=Field.SCIENCE)
    startYear = models.IntegerField(_('startyear'), validators=[MinValueValidator(1984), max_value_current_year])
    endYear = models.IntegerField(_('endyear'), validators=[MinValueValidator(1984), max_value_current_year])
    percentage = models.DecimalField(max_digits=4, decimal_places=2, validators=[MaxValueValidator(100)])
    holder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.holder.username}\'s {self.degree}'




class Certification(models.Model):
    name = models.CharField(max_length=255, blank=False, null=True)
    organization = models.CharField(max_length=255, blank=False, null=True)
    expire = models.BooleanField(default=False)
    issueDate = models.DateField(default=datetime.date.today)
    expirationDate = models.DateField(blank=True, null=True)
    credentialID = models.CharField(max_length=32, blank=True, null=True)
    credentialURL = models.URLField(blank=True)
    certificatePDF = models.FileField(null=True, upload_to='uploads/pdf_files')
    holder = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.holder.username}\'s -> Cerificate: {self.name}'



class Project(models.Model):

    class Degree(models.TextChoices):
        ODD = 'BE', _('B.Tech')
        EVEN = 'DC', _('Diploma')


    name = models.CharField(max_length=255, blank=False, null=True)
    status = models.BooleanField(default=False)
    startDate = models.DateField(default=datetime.date.today)
    completionDate = models.DateField(blank=True, null=True)
    associated = models.CharField(max_length=255, blank=False, null=True)
    projectURL = models.URLField(blank=True)
    description = models.TextField(max_length=1024, blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.holder.username}\'s -> Project: {self.name}'



class Semester(models.Model):
    semester = models.IntegerField(_('semester'), validators=[MinValueValidator(0), MaxValueValidator(10)])
    evenOdd = models.CharField(max_length=7)
    totalSub = models.IntegerField(_('totalsubjects'), validators=[MinValueValidator(0), MaxValueValidator(12)])
    theorySub = models.IntegerField()
    practicalSub = models.IntegerField()
    totalMarksObtained = models.IntegerField()
    totalMarks = models.IntegerField()
    carryOverSub = models.IntegerField()
    sgpa = models.DecimalField(max_digits=3, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.holder.username}\'s -> Project: {self.name}'
