from django.shortcuts import render, redirect
from .models import Receipe
from django.contrib.auth.models import User
# login used as a session 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="/login")
def receipes(request):
    if request.method == "POST":
        receipe_name = request.POST.get('receipe_name')
        receipe_description = request.POST.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description=receipe_description,
            receipe_image=receipe_image
        )
        # Here Page will get redirected and dosen't hold data of previous form
        return redirect('receipes')

    queryset = Receipe.objects.all()
    return render(request, 'Pages/recepies.html', {'receipes': queryset})

@login_required(login_url="/login")
def receipes_list(request):
    context = {'context': Receipe.objects.all()}
    return render(request, 'Pages/recepies_List.html', context=context)

@login_required(login_url="/login")
def delete_receipe(request, id):
    querySet=Receipe.objects.get(id=id)
    querySet.delete()
    return redirect('/recepies_list')

@login_required(login_url="/login")
def update_receipe(request, id):
    querySet = Receipe.objects.get(id=id)
    context = {'recepie': querySet}
    
    if request.method == "POST":
        data = request.POST

        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        if receipe_name:  # Only update if not None or empty string
            querySet.receipe_name = receipe_name

        if receipe_description:
            querySet.receipe_description = receipe_description

        if receipe_image:
            querySet.receipe_image = receipe_image

        querySet.save()
        return redirect('/recepies_list')
    
    return render(request,'Pages/update_recepies.html',context=context)        

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username  
        except User.DoesNotExist:
            messages.error(request, "Email doesn't exist")
            return redirect("/login")

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Incorrect password")
            return redirect("/login")
        else:
            login(request, user)
            return redirect('receipes')
    return render(request, 'Pages/Login_Page.html')

def register(request):
    if request.method=="POST":
        username=request.POST.get('username')
        email=request.POST.get('email') 
        password=request.POST.get('password')
        
        user=User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request,"Username already taken")
            return redirect("/register")
        
        userEmail=User.objects.filter(email=email)
        
        if userEmail.exists():
            messages.info(request,"Email is already present")
            return redirect("/register")
        
        user=User.objects.create(username=username,email=email)
        # Now password encryption
        user.set_password(password)
        user.save()
        return redirect('receipes')

    return render(request,'Pages/Register.html')

@login_required(login_url="/login")
def logout_page(request):
    logout(request)
    return redirect("/login")