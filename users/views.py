from django.shortcuts import render, HttpResponse
from .forms import CertificateForm, EducationForm, ProjectForm, SemesterForm, UserRegisterForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .decorators import unauthenticated_user, allowed_users

from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.decorators import method_decorator
from blog.views import is_users
from .models import Education, Certification, Profile, Project, Semester

from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text

from django_project.settings import EMAIL_HOST_USER


@login_required
def resume(request, username, **kwargs):
    if request.method == 'GET':
        visible_user = User.objects.get(username=username)
        userdetail = User.objects.get(username=visible_user)
        profiledetail = Profile.objects.get(user=visible_user)
        educationdetail = Education.objects.filter(holder=visible_user).order_by('-startYear')
        certificatedetail = Certification.objects.filter(holder=visible_user).order_by('-issueDate')
        projectdetail = Project.objects.filter(owner=visible_user).order_by('-startDate')
        semesterdetail = Semester.objects.filter(owner=visible_user).order_by('-semester')
    return render(request,'users/resume.html', {'userdetail': userdetail, 'profiledetail': profiledetail, 'educationdetail':educationdetail, 'certificatedetail':certificatedetail, 'projectdetail': projectdetail, 'semesterdetail': semesterdetail})


@login_required
def result(request, username, **kwargs):
    if request.method == 'GET':
        visible_user = User.objects.get(username=username)
        semesterdetail = Semester.objects.filter(owner=visible_user)
    return render(request,'users/sem-result.html', {'semesterdetail': semesterdetail})


@unauthenticated_user
def register(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, EMAIL_HOST_USER, [to_email])
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}, Please get verified yourself by further procedures to enter the platform.')
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})



def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



@login_required
@allowed_users(allowed_roles=['student', 'teacher'])
def profile(request):
    if request.method == 'GET':
        pform = Profile.objects.get(user=request.user)
        eform = Education.objects.filter(holder=request.user)
        cform = Certification.objects.filter(holder=request.user)
        prform = Project.objects.filter(owner=request.user)
        sform = Semester.objects.filter(owner=request.user)

    return render(request, 'users/profile.html', {'pform': pform, 'eform': eform, 'cform': cform, 'prform': prform, 'sform': sform})



@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'users/add-update.html'
    success_url = '/profile'
    success_message = "%(username)s profile has been updated"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().user, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_line'] = 'Edit profile details'
        return context



@login_required
def SearchView(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        print(query)
        results = User.objects.filter(username__contains=query)
        context = {
            'results':results
        }
        return render(request, 'users/search_result.html', context)



@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class EducationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Education
    template_name = 'users/delete.html'
    context_object_name = 'education'
    success_url = '/profile'

    def test_func(self):
        return is_users(self.get_object().holder, self.request.user)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class EducationCreateView(LoginRequiredMixin, CreateView):
    model = Education
    form_class = EducationForm
    template_name = 'users/add-update.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.holder = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add education'
        return data


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class EducationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Education
    form_class = EducationForm
    template_name = 'users/add-update.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.holder = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().holder, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_line'] = 'Edit educational details'
        return context


# Certificate view

@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class CertificateDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Certification
    template_name = 'users/delete.html'
    context_object_name = 'certificate'
    success_url = '/profile'

    def test_func(self):
        return is_users(self.get_object().holder, self.request.user)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class CertificateCreateView(LoginRequiredMixin, CreateView):
    model = Certification
    form_class = CertificateForm
    template_name = 'users/add-update.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.holder = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add certificate'
        return data


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class CertificateUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Certification
    form_class = CertificateForm
    template_name = 'users/add-update.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.holder = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().holder, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_line'] = 'Edit certificate'
        return context


# Project view

@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    template_name = 'users/delete.html'
    context_object_name = 'project'
    success_url = '/profile'

    def test_func(self):
        return is_users(self.get_object().owner, self.request.user)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'users/add-update.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add project'
        return data


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'users/add-update.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().owner, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_line'] = 'Edit project'
        return context

    

# semester view


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class SemesterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Semester
    template_name = 'users/delete.html'
    context_object_name = 'semester'
    success_url = '/profile'

    def test_func(self):
        return is_users(self.get_object().owner, self.request.user)


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class SemesterCreateView(LoginRequiredMixin, CreateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'users/add-update.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag_line'] = 'Add semester result'
        return data


@method_decorator(allowed_users(allowed_roles=['student', 'teacher']), name='dispatch')
class SemesterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Semester
    form_class = SemesterForm
    template_name = 'users/add-update.html'
    success_url = '/profile'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().owner, self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_line'] = 'Edit semester result'
        return context