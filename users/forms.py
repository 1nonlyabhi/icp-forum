from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

import datetime
from .models import Certification, Profile, Education, Project, Semester, current_year
from django.core.exceptions import ValidationError


def start_year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+1)]

def end_year_choices():
    return [(r,r) for r in range(1984, datetime.date.today().year+20)]


start_yr = [r for r in range(1984, datetime.date.today().year+1)]
end_yr = [r for r in range(1984, datetime.date.today().year+20)]



USER_TYPE =(
    ( "Student" , "Student"),
    ( "Faculty" , "Faculty")
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

    def clean(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username).first():
            raise ValidationError("Username exists")
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username = username).first():
            raise ValidationError("Username exists")
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email exists")
        return self.cleaned_data


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstname','lastname','rollno','bio','birth_date','image','location','techskills','extraskills','linkedin', 'twitter', 'github']
        labels = {
        "firstname": "First Name",
        "lastname": "Last Name",
        "rollno": "Roll No",
        "birth_date": "Birth Date (yyyy-mm-dd)",
        "location": "Address",
        "techskills": "Technical Skills",
        "extraskills": "Extra Skills",
        }


class EducationForm(forms.ModelForm):
    startYear = forms.TypedChoiceField(coerce=int, choices=start_year_choices, initial=current_year, label='Start Year')
    endYear = forms.TypedChoiceField(coerce=int, choices=end_year_choices, initial=current_year, label='End Year')

    class Meta:
        model = Education
        fields = ['school', 'degree', 'field', 'startYear', 'endYear', 'percentage']

    


class CertificateForm(forms.ModelForm):

    class Meta:
        model = Certification
        fields = ['name', 'organization', 'expire', 'issueDate', 'expirationDate', 'credentialID', 'credentialURL', 'certificatePDF']
        labels = {
        "expire": "This credential does not expire",
        "issueDate": "Issue Date",
        "expirationDate": "Expiration Date (if any)",
        "credentialID": "Credential ID",
        "credentialURL": "Credential URL",
        "certificatePDF": "Certificate PDF file",
        }
        widgets = {
            'issueDate': forms.SelectDateWidget(years=start_yr),
            'expirationDate': forms.SelectDateWidget(years=end_yr)
        }



class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['name', 'status', 'startDate', 'completionDate', 'associated', 'projectURL', 'description']
        labels = {
        "status": "Currently working on this project",
        "startDate": "Start Date",
        "completionDate": "Completion Date (if any)",
        "associated": "Associated or Worked with",
        "projectURL": "Project URL",
        }
        widgets = {
            'startDate': forms.SelectDateWidget(years=start_yr),
            'completionDate': forms.SelectDateWidget(years=end_yr)
        }


SEM_CHOICES =(
    (1, "1"),
    (2, "2"),
    (3, "3"),
    (4, "4"),
    (5, "5"),
    (6, "6"),
    (7, "7"),
    (8, "8"),
    (9, "9"),
    (10, "10"),
)

EVEN_ODD =(
    ( "Even" , "Even"),
    ( "Odd" , "Odd")
)


class SemesterForm(forms.ModelForm):
    semester = forms.ChoiceField(choices=SEM_CHOICES)
    evenOdd = forms.ChoiceField(label='Even or Odd', choices=EVEN_ODD)

    class Meta:
        model = Semester
        fields = ['semester', 'evenOdd', 'totalSub', 'theorySub', 'practicalSub', 'totalMarksObtained', 'totalMarks', 'carryOverSub', 'sgpa', ]
        labels = {
            "totalSub": "Total Subjects",
            "theorySub": "Theory Subjects",
            "practicalSub": "Practical Subjects",
            "totalMarksObtained": "Total Marks Obtained",
            "totalMarks": "Maximum Marks",
            "carryOverSub": "Carry Over Subjects",
            "sgpa": "SGPA",
        }