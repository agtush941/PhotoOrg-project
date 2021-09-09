from django.shortcuts import render, redirect
from .models import Photo, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
@login_required(login_url = 'login')
def gallery(request):
    user = request.user
    category = request.GET.get('category')
    query = request.GET.get('query')
    
    if category ==  None and query == None:
        images = Photo.objects.filter(category__user = user)
    elif category != None:
        images = Photo.objects.filter(category__name = category,category__user = user)
    else:
        images = Photo.objects.filter(desc__contains = query,category__user = user)

    
    categories = Category.objects.filter(user = user)
    context = { 'images' : images,'categories': categories}

    return render(request,'photos/gallery.html',context)





@login_required(login_url = 'login')
def addPhoto(request):
    user = request.user
    categories = Category.objects.filter(user = user)

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != "none":
            category = Category.objects.get(id = data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name = data['category_new'],user = user)    
        else:
            category = None

        photo = Photo.objects.create(category=category,desc = data['desc'],image = image)
        return redirect('gallery')

    context = { 'categories': categories}
    return render(request,'photos/add.html',context)

@login_required(login_url = 'login')
def viewPhoto(request,pk):
    image = Photo.objects.get(id = pk)
    return render(request,'photos/photo.html',{'image' : image})

def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('gallery')
    page = 'login'
    return render(request,'photos/login_register.html',{'page' : page})

def logoutUser(request):
    return redirect('login')    

def registerUser(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            

            user = authenticate(request,username = user.username,password = request.POST['password1'])
            if user is not None:
                login(request,user)
                return redirect('gallery')

    page = 'register'
    form = UserCreationForm()
    context = {'form': form,'page' : page}
    return render(request,'photos/login_register.html',context)

@login_required(login_url = 'login')
def deletePhoto(request,pk):
    Photo.objects.get(id = pk).delete()
    return redirect('gallery')