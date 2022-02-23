from multiprocessing import context
from optparse import Values
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Message
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import *


# Create your views here.
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            token = request.POST['csrfmiddlewaretoken']
            try:
                user = User.objects.get(username=username)
            except:
                messages.error(request, "User doesn't exists.")

            user = authenticate(request,username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'account')
            else:
                messages.error(request,"Username or password is incorrect")

        return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, "User has been successfully logout.")
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'Account has been created successfully.')
            # return redirect('login')

            login(request,user)
            return redirect('edit-account')

        else:
            messages.error(request, 'Something went wrong.')

    context = {
        'page': page,
        'form': form
        }
    return render(request, 'users/login_register.html', context)

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, paginator, profiles  = createPagination(request,profiles,3)
    values = {
        'profiles': profiles,
        'search_query': search_query,
        'custom_range': custom_range,
        'paginator': paginator
    }
    return render(request, 'users/profiles.html', context=values)

def profile(request, pk):
    profile = Profile.objects.get(id=pk)
    values = {
        'profile': profile
    }
    return render(request, 'users/user_profile.html', context=values)

@login_required(login_url='login')
def userAccount(request):
    account = request.user.profile
    values = {
        'account': account,
        }
    return render(request, 'users/account.html', context=values)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    values = {
        'form': form
    }
    return render(request, 'users/profile_form.html', context=values)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request,"Skill has been created successfully!")
            return redirect('account')
    values = {
        "form": form
    }
    return render(request, 'users/skill_form.html', context=values)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method == "POST":
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request,"Skill has been updated successfully!")
            return redirect('account')
    values = {
        "form": form
    }
    return render(request, 'users/skill_form.html', context=values)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if request.method == "POST":
        skill.delete()
        messages.info(request,"Skill has been deleted!")
        return redirect('account')
    values = {
        "object": skill
    }
    return render(request, 'delete_template.html', context=values)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read=False).count()
    values = {
        'messageRequest': messageRequest,
        'unreadCount': unreadCount
        }

    return render(request, 'users/inbox.html', context=values)

@login_required(login_url='login')
def singleMessage(request, pk):
    profile = request.user.profile
    userMessage = profile.messages.get(id=pk)
    values = {
        'userMessage': userMessage
    }
    if userMessage.is_read == False:
        userMessage.is_read = True
        userMessage.save()
    return render(request, 'users/message.html', context=values)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()

            messages.success(request, "Message has been sent to the user.")
            return redirect("profile", pk=recipient.id)

    values = {
        'recipient': recipient,
        'form': form
    }

    return render(request, 'users/message_form.html', context=values)