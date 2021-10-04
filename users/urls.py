from django.urls.conf import path

from users import views
from .views import CertificateCreateView, CertificateDeleteView, CertificateUpdateView, EducationCreateView, EducationDeleteView, EducationUpdateView, ProfileUpdateView, ProjectCreateView, ProjectDeleteView, ProjectUpdateView, SemesterCreateView, SemesterDeleteView, SemesterUpdateView, resume

urlpatterns = [
    path('<str:username>/sem-result/',views.result, name='sem-result'),
    path('<str:username>/resume/',views.resume, name='resume'),
    path('profile/<int:pk>/update/', ProfileUpdateView.as_view(), name='profile-update'),

    path('education/new/', EducationCreateView.as_view(), name='education-create'),
    path('education/<int:pk>/update/', EducationUpdateView.as_view(), name='education-update'),
    path('education/<int:pk>/del/', EducationDeleteView.as_view(), name='education-delete'),

    path('certificate/new/', CertificateCreateView.as_view(), name='certificate-create'),
    path('certificate/<int:pk>/update/', CertificateUpdateView.as_view(), name='certificate-update'),
    path('certificate/<int:pk>/del/', CertificateDeleteView.as_view(), name='certificate-delete'),

    path('project/new/', ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('project/<int:pk>/del/', ProjectDeleteView.as_view(), name='project-delete'),
    
    path('semester/new/', SemesterCreateView.as_view(), name='semester-create'),
    path('semester/<int:pk>/update/', SemesterUpdateView.as_view(), name='semester-update'),
    path('semester/<int:pk>/del/', SemesterDeleteView.as_view(), name='semester-delete'),
]
