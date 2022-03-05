from django.core import paginator
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import ProjectForm, ReviewForm
from .models import Project, Tag
from .utils import searchProjects, createPagination

def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, paginator, projects  = createPagination(request,projects,6)
    
    values = {
        'projects': projects,
        'search_query': search_query,
        'paginator': paginator,
        'custom_range': custom_range}
    return render(request, 'projects/projects.html', context=values)

def project(request, pk):
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    form = ReviewForm()
    object = {
        'project': project,
        'tags': tags,
        'form': form
        }

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = project
            review.owner = request.user.profile
            review.save()

            project.getVoteCount
            project.reviewers
            messages.success(request, "Your review was successfully submitted")
            return redirect('project', pk=project.id)

    return render(request, 'projects/single_project.html', context=object)

@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')

    context = {
        'form': form
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
 
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        print(newtags)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {
        'form': form,
        'project': project
    }
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == "POST":
        project.delete()
        return redirect('projects')

    context = {
        'object': project
    }
    return render(request, 'delete_template.html', context)
 