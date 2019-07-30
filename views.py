from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from speciality.models import Speciality
from user_auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .forms import UserUpdateForm, ProfileUpdateForm, NewTopicForm
from django.views.generic import View
from django.contrib.auth.models import User
from soft_skills.models import Skill
from DH.models import Employee_levels
from dateutil.parser import parse
# Create your views here.
def index(request):
    return render(request, 'user_auth/index.html')


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        context = {'form': form}
        return render(request, 'registration/register.html', context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')


class ProfileView(View):
    def get(self, request, username):
        u_profile = UserUpdateForm(instance=request.user)
        p_profile = ProfileUpdateForm(instance=request.user.profile)
        skills = Skill.objects.filter(user=User.objects.get(username=username))
        form = {'u_profile': u_profile, 'p_profile': p_profile, 'username': User.objects.get(username=username),
                'skills': skills}
        return render(request, 'user_auth/profile.html', form)

    def post(self, request,username):
        u_profile = UserUpdateForm(request.POST, instance=request.user)
        p_profile = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_profile.is_valid() and p_profile.is_valid():
            u_profile.save()
            p_profile.save(request)
            return redirect('/')

@login_required
def new_level(request,username):
    ##board = get_object_or_404(Employee_levels, employee=request.user)
    user = User.objects.first()  # TODO: get the currently logged in user
   # HOUR_CHOICES = [(dt.time(hour=x), '{:02d}:00'.format(x)) for x in range(9,18)]
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
#        print(form.errors)
        if form.is_valid():
            a = Employee_levels.objects.filter(test_time=form.cleaned_data.get('test_time'),test_date=form.cleaned_data.get('test_date'))

            if(len(a)==0):
                post = Employee_levels.objects.create(
                    test_date=form.cleaned_data.get('test_date'),
                    test_time=form.cleaned_data.get('test_time'),
                    speciality = request.user.profile.speciality,
                    type_of_test=False,
                    employee=request.user
                )
            #messages.success(request, 'Your request is successfully added.')
            return render(request, 'user_auth/profile.html')#, {'messages':messages})

    else:
        form = NewTopicForm()
    return render(request, 'user_auth/new_level.html')



    # def clean_date_one(request):
    #     date = form.cleaned_data['test_date']
    #     for dates in
    #
    #     #if date <
