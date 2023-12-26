from django.shortcuts import render,redirect

from django.views.generic import View

from mobile.models import Mobiles

from mobile.forms import MobileForm,RegistrationForm,LoginForm

from django.contrib import messages


from django.contrib.auth import authenticate,login,logout

from django.utils.decorators import method_decorator


from django.contrib.auth.models import User

def signin_required(fn):#it is function decorator -it should convert to method decorator-so we have a packge at utils.py,there a decorator file there(method decorator)so frst import utils.py
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"!! Invalid entry....first you have to login")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper

@method_decorator(signin_required,name="dispatch")
class MobileListView(View):
    def get(self,request,*args,**kwargs):
        qs=Mobiles.objects.all()
        #filter using brand
        if "brand" in request.GET:
            brand=request.GET.get("brand")
            #__iexact is given to avoid case sensitivity
            qs=qs.filter(brand__iexact=brand)
            #filter using display
        if "display" in request.GET:
            display=request.GET.get("display")
            qs=qs.filter(display__iexact=display)
            #filtering using amount
        if "price_lt" in request.GET:
            amount=request.GET.get("price_lt")
            qs=qs.filter(price__lte=amount)
        return render(request,"mob_list.html",{"data":qs})
    
#http://127.0.0.1:8000/mobiledetails/2 --to run the page give this url

@method_decorator(signin_required,name="dispatch")
class MobileDetailsbyidView(View):
    def get(self,request,*args,**kwargs):
        print("aaaa",kwargs)
        #to extract the int from url get int value from kwargs dic
        #check wheather user logined or not, if login then only fetch details else redirect to login.html
        if not request.user.is_authenticated:
            return redirect("signin")
        
        id=kwargs.get("pk")
        qs=Mobiles.objects.get(id=id)
        print("anjuuuuu1")
        return render(request,"mob_detailsbylist.html",{"data":qs})
    
#delete
#http://127.0.0.1:8000/mobiles/id/remove

@method_decorator(signin_required,name="dispatch")
class MobileDelete(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Mobiles.objects.get(id=id).delete()
        messages.success(request,"selected mobile data deleted successfully....")

        #we have to redirect to list view name of list view in urls.py is: mobile-all
        return redirect("mobile-all")
#create
#http://127.0.0.1:8000/mobiles/create

@method_decorator(signin_required,name="dispatch")
class MobileCreateView(View):
    
    def get(self,request,*args,**kwargs):
        form=MobileForm()
        return render(request,"mob-add.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=MobileForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request,"mobile data created successfully....")
            return redirect('mobile-all')
        else:
            messages.error(request,"can't create mobile data,...error....")
            return render(request,"mob-add.html",{"form":form})

#update an object
##http://127.0.0.1:8000/mobiles/id/create

@method_decorator(signin_required,name="dispatch")
class MobileUpdateView(View):
    def get(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(instance=obj)
        return render(request,"mob-update.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(request.POST,instance=obj,files=request.FILES)
        if (form.is_valid()):
            form.save()
            messages.success(request,"mobile data updated successfully....")
            return redirect("mobile-all")
        else:
            messages.error(request,"can't update mobile data....error...")
            return render(request,"mob-update.html",{"form":form})


#registration
class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
        

    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            #form.save() to encryprt password we use the below logic,form.cleandata()
            User.objects.create_user(**form.cleaned_data) #** is used to unpack the pass.pass encrypted using sha
          
            messages.success(request,"registraion form created successfully...........")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"registraion form failed to create ...........")
            return render(request,"register.html",{"form":form})
 #login       
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            paswd=form.cleaned_data.get("password")
            print("......",uname,paswd)
            user_object=authenticate(request,username=uname,password=paswd)
            if user_object:
                print("valid credentials")
                #start session
                login(request,user_object)
                print(request.user)  #fetch user details
                return redirect("mobile-all")
            else:
                print("invalid credentials")
            return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})
        
#signout
@method_decorator(signin_required,name="dispatch")        
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
        
