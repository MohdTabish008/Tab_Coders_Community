from django.shortcuts import render , HttpResponse , redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from blog.models import Post
# Html pages
def home(request):
    homePosts = Post.objects.all()[:4]
    context = {'homePosts' : homePosts}
    return render(request,'home/home.html',context)
    

def about(request):
    return render(request, 'home/about.html')


def contact(request):
    if  request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone , content)
        if len(name)<2 or len(email)<7 or len(phone)<8 or len(content)<3:
            messages.error(request, "Please Provide Valid Details!")
        else:    
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request,'Message has been Sent!')
    return render(request, 'home/contact.html')

def search(request):
    query = request.GET['query']
    if len(query)>60:
        allPosts = Post.objects.none()
    else:    
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, " No Search Results to Display,Please Provide Valid Search")    
    param = {'allPosts' : allPosts , 'query': query}
    return render(request, 'home/search.html' , param) 

#Authentication APIs:

def handleSignup(request):
    if request.method == "POST":
        #get post parameters from signup modals
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname'] 
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        #check errorneous inputs
        #username must be < 10 charachters
        if len(username) > 10 :
            messages.error(request, "username must be have less than 10 charachters")
            return redirect('home')
        #only alpha numeric name allowed
        if not username.isalnum() :
            messages.error(request, "username must be have letters and alphabets only")
            return redirect('home') 
        #conforming passwords
        if pass1 != pass2 :
            messages.error(request, "make sure passwords match")
            return redirect('home')       

        #user creation
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Tab_Coder account Created Successfully!")
        return redirect('home')
    else:
        return HttpResponse('404-Not Found')    


def handleLogin(request):
    if request.method == "POST":
        #get credentials from login modal
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)
            
        if user is not None:
            login(request ,user)
            messages.success(request,'Successfully Logged In!')
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials Provided, Please Try Again!')    
            return redirect('home')
        
    return HttpResponse('404-Not Found')    

        


def handleLogout(request):
    logout(request)
    messages.success(request,'Logged out Successfully!')
    return redirect('home')