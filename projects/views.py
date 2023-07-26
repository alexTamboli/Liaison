from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

from .models import Project, Tag
from .utils import searchProjects, paginateProjects

from .forms import ProjectForm, ReviewForm
from config import Constants



def projects(request):
    projects, search_query = searchProjects(request)
    custom_range, projects, paginator = paginateProjects(request, projects, Constants.PAGINATOR_PROJECTS_RESULTS)
    context = {
        'projects': projects,
        'search_query': search_query,
        'paginator': paginator,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()
    
    # Check and add "http://" prefix for demo_link and source_link,  
    # beacuse if no http is there, it will append like http://127.0.0.1/...existingurl/{projectObj.demo_link}
    if projectObj.demo_link and not projectObj.demo_link.startswith('http'):
        projectObj.demo_link = f'http://{projectObj.demo_link}'
    if projectObj.source_link and not projectObj.source_link.startswith('http'):
        projectObj.source_link = f'http://{projectObj.source_link}'
        
        
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()
        projectObj.getVoteCount
        messages.success(request, 'Your review was successfully submitted.')
        
        return redirect('project', pk=projectObj.id)
        
    context = {
        'project': projectObj,
        'form': form
    }
    return render(request, 'projects/project.html', context)


@login_required(login_url="login")
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
                
            messages.success(request, "Your project has been added")
            return redirect('account')
    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project  = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(',', ' ').split()
        
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            
            messages.success(request, "Your project has been updated succesfully")
            return redirect('account')
    context = {'form': form, 'project': project}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
    context = {
        'object': project
    }
    
    return render(request, 'delete_template.html', context)