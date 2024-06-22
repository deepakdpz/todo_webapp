from django.shortcuts import render,redirect

from django.views.generic import View

from remainder.forms import Userform,LoginForm,TodoForm

from django.contrib.auth import authenticate,login,logout
from remainder.models import Todos

from django.utils.decorators import method_decorator


def signin_required(fn):

    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("login")
        
        else:
            return fn(request,*args,**kwargs)
    return wrapper    


def owner_permission_required(fn):
    pass
        


class SignUpView(View):

    def get(self,request,*args,**kwargs):

        form=Userform()

        return render(request,"register.html",{"form":form})

    def post(self,request,*args,**kwargs):

        form=Userform(request.POST)

        if form.is_valid():
            form.save()
            print("account created")

            return redirect("register")
        
        else:
            print("failed")
            return render(request,"register.html",{"form":form})
        

class SignInView(View):

    def get(self,request,*args,**kwargs):

        form=LoginForm()

        return render(request,"login.html",{"form":form})   


    def post(self,request,*args,**kwargs):

        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get("password")
            user_object=authenticate(request,username=uname,password=pswd)
            if user_object:
                login(request,user_object)
                print("login successfull")
                return redirect("index")
            
        print("invalid credentials")
        return render(request,"login.html",{"form":form})    
    

@method_decorator(signin_required,name="dispatch")
class SignOutView(View):

    def get(self,request,*args,**kwargs):

        logout(request)
        return redirect("login")    

@method_decorator(signin_required,name="dispatch")
class IndexView(View):

    def get(self,request,*args,**kwargs):
        form=TodoForm()
        qs=Todos.objects.filter(user=request.user).order_by("status")
        return render(request,"index.html",{"form":form,"data":qs})

    def post(self,request,*args,**kwargs):

        form=TodoForm(request.POST)

        if form.is_valid():
            form.instance.user=request.user
            form.save()
            return redirect("index")
        
        else:
            return render(request,"index.html",{"form":form})

@method_decorator(signin_required,name="dispatch")
class TodoDeleteView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        Todos.objects.filter(id=id).delete()
        return redirect("index")


@method_decorator(signin_required,name="dispatch")
class TodoChangeView(View):

    def get(self,request,*args,**kwargs):

        id=kwargs.get("pk")
        Todos.objects.filter(id=id).update(status=True)
        return redirect("index")    
