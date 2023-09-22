from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .utils import sendotp
from datetime import datetime
from pyotp import totp
import pyotp
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
import json
import pprint
import google.generativeai as palm

palm.configure(api_key="AIzaSyAgL6CKRbjUaJ52mS_vJx9Fn7k87tIG93U")
models=[m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model=models[0].name
print(model)
current_stt='''You are a legal documentation generator and extractor. You will not assume any details. You will return a contract with max token limit of 3050. 
Use Legal Jargon. You present the output in terms as a legal document. Solve the following prompt:'''

# Create your views here.
def registerPage(request):
    form=CreateUserForm()
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if(request.method=="POST"):
            form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(request, 'Account was Created '+user)
            return redirect('login')
    context={'form':form}
    return render(request, 'chatbot/register.html', context)

def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request, username=username, password=password)
        if user is not None:
            request.session['src-mail']="aayushfabwani2@gmail.com"
            user=get_object_or_404(User,username=username)
            request.session['dest-mail']=user.email
            # login(request, user)
            request.session['username']=username
            # return redirect('home')
            sendotp(request)
            return redirect('otp')
        else:
            messages.info(request,'Username OR password is incorrect')
            return render(request, 'chatbot/login.html')
    context={}
    return render(request, 'chatbot/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def otp(request):
    if(request.method=="POST"):
        otp=request.POST['otp']
        username=request.session['username']
        otp_secret_key=request.session['otp_secret_key']
        otp_valid_until=request.session['otp_valid_date']
        if otp_secret_key and otp_valid_until is not None:
            valid_until=datetime.fromisoformat(otp_valid_until)
            if valid_until>datetime.now():
                totp=pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    user=get_object_or_404(User,username=username)
                    login(request,user)
                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']
                    return redirect('home')
                else:
                    user=get_object_or_404(User,username=username)
                    login(request,user)
                    return redirect('home')
            else:
                pass
        else:
            pass
    return render(request,"chatbot/otp.html")


@login_required(login_url='login')
def home(request):
    return render(request,'chatbot/home.html')

def get_chat_response(userText):
    prompt=current_stt+userText
    completion=palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0,
        max_output_tokens=1500,
    )
    return completion.result

def process(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            # Extract userText and other data from the JSON payload
            model = data.get('model', '')
            userText = data.get('prompt', '')
            output=get_chat_response(userText)
            
            response_data = {'message': output}
            return JsonResponse(response_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)