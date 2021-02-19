from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from index.models import Task, User, Status, Group, Comment, Notification
from django.contrib import messages
from .forms import TaskForm
from django.http import Http404
from django.contrib.auth.decorators import user_passes_test
import datetime
# Create your views here.

def can_add(user):
    if user.groups.filter(name='TL').exists():
        return True
    else:
        return False


@login_required(login_url="index:login")
def index1(request):
    try:
        usergp = request.user.groups.all()
        grplist =[]
        for x in usergp:
            grplist.append(x)
        return redirect('dashboard:index', grplist[0])
    except:
        raise Http404('Plese contact your admin to assign you to a group')

@login_required(login_url="index:login")
def index(request, group):
    # task = Task.objects.all()
    # users = User.objects.all()
    # statuses = Status.objects.all()
    # # user = User.objects.get(username="nicolas")
    # # usertask = Task.objects.filter(user=user)
    # ctx = {'tasks': task, 'users': users, 'statuses': statuses}
    # return render(request, 'dashboard/dashboard.html', ctx)
    obj = get_object_or_404(Group, name=group)
    noti = Notification.objects.filter(user=request.user)
    # noti = noti.notification
    usergp = request.user.groups.all()
    grplist =[]
    for x in usergp:
        grplist.append(x)
    
    show = False
    if can_add(request.user):
        show = True
    
    if group not in str(grplist):
        messages.error(request, "You do not have permission to access :  \"" 
        + request.META['PATH_INFO'] + "\" Please Contact your team leader for more info!")
        
        return redirect('dashboard:index', grplist[0])
    else:
        grp = Group.objects.get(name=group)
        grp = grp.id
        task = Task.objects.filter(group=grp)
        ctx = {'tasks': task, 'grp':list(usergp), 'group': group, 'show': show, 'noti': noti}
        return render(request, 'dashboard/dashboard.html', ctx)

@user_passes_test(can_add)
def createTask(request, group_from_url):
    get_object_or_404(Group, name=group_from_url)
    usergp = request.user.groups.all()
    users=[]
    statuses = Status.objects.all()

    users = User.objects.filter(groups__name=group_from_url)

    # form = TaskForm()
    grplist =[]
    for x in usergp:
        grplist.append(x.name)
    # ctx = {'form': form, 'usergp':len(grplist), 'users': users, 'grplist': grplist, 'statuses':statuses}
    ctx = {'usergp':len(grplist), 'users': users, 'grplist': grplist, 'statuses':statuses}

    
    if request.method == 'POST':
        # form = TaskForm(request.POST)
        # if form.is_valid:
        if request.user.check_password(request.POST.get('password')):
            titl = request.POST.get('title')
            desc = request.POST.get('desc')
            fulldesc = request.POST.get('fulldesc')
            user = request.POST.get('user2')
            due = request.POST.get('due')
            status = request.POST.get('status')
            status = get_object_or_404(Status, id=status)

            grp = get_object_or_404(Group, name=group_from_url)
            taskgrp = request.user.groups.all()
            user = get_object_or_404(User, id=user)
            if user in users:
                task = Task(title=titl, user=user, group=grp, status=status, description=desc, moreinfo=fulldesc, due=due)
                task.save()
            else:
                messages.error(request, 'already thought of that try something else ')
                return redirect('dashboard:addTask', group_from_url)
            # else:
            #     messages.error(request, 'You do not have permission to add to group: '+ str(grp))
            #     return redirect('dashboard:addTask')
            messages.success(request, 'Task added Successfully')
            return redirect('dashboard:index', grplist[0])
        else:
            messages.error(request, 'password incorrect (please enter the password You signed in with)')
    return render(request, 'dashboard/Task-create.html', ctx)

@login_required(login_url="index:login")
def task(request, task):
    get_object_or_404(Task, id=task)
    task = Task.objects.get(id=task)
    try:
        noti = Notification.objects.get(task=task)
        if request.user == task.user:
            noti.delete()
    except:
        pass
    usergp = request.user.groups.all()
    users = User.objects.filter(groups__name=usergp[0].name)
    # form = TaskForm()
    grplist =[]
    for x in usergp:
        grplist.append(x)

    # task = Task.objects.get(id=task)
    taskgrp = task.group
    if taskgrp in grplist:
        ctx = {'task': task, 'grplist': grplist, 'taskgrp':taskgrp}
        return render(request, 'dashboard/task-template.html', ctx)
    else:
        taski = request.META['PATH_INFO'].split('/')[3]
        tasky = Task.objects.get(id=taski).group
        messages.error(request,"You do not have permission to access task \""
        + request.META['PATH_INFO'].split('/')[3] + "\", Please Contact your team leader for more info! \n This Task belongs to: \"" +
        str(tasky) + "\".")
        return redirect('dashboard:index', grplist[0])
    
@user_passes_test(can_add)
def editTask(request, task):
    usergp = request.user.groups.all()
    task = Task.objects.get(id=task)
    # form = TaskForm(instance=task)
    task_grp = task.group
    users = User.objects.filter(groups__name=task_grp.name)
    statuses = Status.objects.all()

    grplist =[]
    for x in usergp:
        grplist.append(x)
    ctx = {'task': task, 'usergp':len(grplist), 'users': users, 'statuses': statuses}
    if request.method == 'POST':
        # form = TaskForm(request.POST, instance=task)
        # if form.is_valid:
        if request.user.check_password(request.POST.get('password')):
            titl = request.POST.get('title')
            user = request.POST.get('user2')
            desc = request.POST.get('desc')
            fulldesc = request.POST.get('fulldesc')
            # user = request.POST.get('user2')
            due = request.POST.get('due')
            status = request.POST.get('status')
            status = get_object_or_404(Status, id=status)
            # print(task.id)
            # grpid = request.POST.get('group')
            # grp = get_object_or_404(Group, id=grpid)
            # taskgrp = request.user.groups.all()
            # if grp in taskgrp:
            # form.save()
            
            user = get_object_or_404(User, id=user)
            # print(user, '\n', users)
            if user in users:
                # Task.objects.filter(title=titl).update(group=grpid)
                t = Task.objects.get(id=task.id)
                t.title=titl 
                t.user=user 
                t.description=desc 
                t.moreinfo=fulldesc 
                t.due=due 
                t.status=status
                t.save()
                messages.success(request, 'Task Updated')
            else:
                messages.error(request, 'already thought of that try something else ')
                return redirect('dashboard:editTask', task.id)
                
            # else:
            #     messages.error(request, 'You do not have permission to add to group: '+ str(grp))
            #     return redirect('dashboard:editTask', task.id)
            return redirect('dashboard:index', grplist[0])
        else:
            messages.error(request, 'password incorrect (please enter the password You signed in with)')
    return render(request, 'dashboard/task-edit.html', ctx)

@user_passes_test(can_add)
def deleteTask(request, task):
    task = Task.objects.get(id=task)
    usergp = request.user.groups.all()
    grplist =[]
    for x in usergp:
        grplist.append(x)
    
    if request.method == 'POST':
        if request.user.check_password(request.POST.get('password')):
            task.delete()
            messages.success(request, 'Task Deleted')
            return redirect('dashboard:index', grplist[0])
        else:
            messages.error(request, 'password incorrect (please enter the password You signed in with)')
            return redirect('dashboard:task', task.pk)
    else:
        return HttpResponseRedirect(reverse('index:logout'))


def markTaskDone(request, task):
    task = get_object_or_404(Task, id=task)
    
    if request.method == 'POST':
        if request.user == task.user:
            if request.POST.get('undone') != None:
                status = Status.objects.get(name="Active").id

                Task.objects.filter(title=task.title).update(status=status)

                messages.success(request, 'Take your time')
                return redirect('dashboard:task', task.id)

            # task = Task.objects.get(id=task)
            status = Status.objects.get(name="Awaiting Review").id

            Task.objects.filter(title=task.title).update(status=status)

            messages.success(request, 'Congrats you have finished your task please wait your TL approval')
            return redirect('dashboard:task', task.id)
        else:
            messages.error(request, 'This task belongs to \"' + str(task.user) +"\".")
            return redirect('dashboard:task', task.id)
    else:
        return redirect('dashboard:task', task.id)

def TaskReview(request, group):
    groupid = get_object_or_404(Group, name=group)
    groupuser = Group.objects.filter(user=request.user)
    
    for grp in groupuser:
        if 'TL' in grp.name:
            status = Status.objects.get(name="Awaiting Review").id
            tasks = Task.objects.filter(status=status, group=groupid)

            ctx = {'tasks': tasks}
            return render(request, 'dashboard/review.html', ctx)

    return redirect('dashboard:index', group)


def addComment(request, task):
    taskid = get_object_or_404(Task, id=task)
    if request.method == 'POST':
        comment_body = request.POST.get('comment_sent')
        title = comment_body[:50]
        user = request.user
        date_added = datetime.datetime.now()

        comment = Comment(task=taskid, user=user, date_added=date_added, body=comment_body, title=title)
        comment.save()

    return redirect('dashboard:task', task)

def deleteComment(request, task, comment_id):
    c_id = get_object_or_404(Comment, id=comment_id)
    print(c_id.user)
    if request.user == c_id.user:
        c_id.delete()
    return redirect('dashboard:task', task)