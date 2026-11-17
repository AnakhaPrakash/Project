from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.shortcuts import redirect
from  django.core.files.storage import FileSystemStorage
from django.conf import settings
from .models import *
import os
from ML import test
from django.contrib import messages
from ML.test import predict  
from django.http import JsonResponse
from .models import patient_result, Recommendation

def first(request):
    return render(request,'index.html')

def index(request):
    return render(request,'index.html') 
   
def userss(request):
    return render(request,'adduser.html') 

def login(request):
    return render(request,'login.html')
    
     
def logint(request):
    email = request. POST.get('email')
    password = request.POST.get('password')
    
    if email == 'admin@gmail.com' and password == 'admin':
        request.session['logintdetail'] = email
        request.session['logint'] = 'admin'
        return render(request, 'index.html')
                            
    elif patient.objects.filter(email=email,password=password).exists():
        userdetails=patient.objects.get(email=email, password=password)
        request.session['uid'] = userdetails.id
        
        return render(request,'index-user.html')        
    elif expert_tbl.objects.filter(email=email,password=password, status="accepted").exists():
        userdetails=expert_tbl.objects.get(email=email, password=password)
        request.session['eid'] = userdetails.id
        
        return render(request,'index.html')        
    
    else:
        return render(request, 'login.html', {'status': 'INVALID USERID OR PASSWORD'})     
             

        
def logout(request):
    session_keys = list(request.session.keys())
    for key in session_keys:
        del request.session[key]
    return redirect(first)      


def adduser(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        age=request.POST.get('age')
        gender=request.POST.get('gender')
        phone=request.POST.get('phone')
        blood=request.POST.get('bloodgroup')
        pass2=request.POST.get('pass2')

        if pass1 != pass2:
            return render(request,"adduser.html",{'message':'password doesnt match'})

        emp=patient(name=name,email=email,password=pass1, age=age, gender=gender , blood_group=blood, phone=phone)    
        emp.save()
        messages.success(request, "Registration successfully completed")
        return redirect('login')


def expert(request):
    return render(request,'expert.html')

def addexpert(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('pass1')
        name=request.POST.get('name')
        phone=request.POST.get('phone')
     
        experience=request.POST.get('experience')
        place=request.POST.get('place')
        # department=request.POST.get('department')
        myfiles=request.FILES['certificate']
        fs=FileSystemStorage()
        filepath=fs.save(myfiles.name,myfiles)
        # filepath= "Testing"
        ins=expert_tbl(name=name, email=email, phone=phone,
                    password=password, experience=experience,
                    place=place,
                    certificate=filepath,status='pending')
        ins.save()
        messages.success(request, "Registration successfully completed")
        return redirect('login')
        
    return render(request,'add_expert.html',{'message':"Successfully Registered"})
      


def prediction(request):
    return render(request,'predictions.html')       


# def pred(request):
#     if request.method == 'POST':
#         u_id = request.session['uid']
#         myfile = request.FILES['image']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)

#         # Delete previous input if exists
#         try:
#             os.remove("media/input/test/test.jpg")
#         except:
#             pass

#         fs.save('input/test/{}'.format("test.jpg"), myfile)

#         # Prediction
#         result = test.predict()  
#         print("*****************************")
#         print(result)


#         emp = patient_result(image=filename, result=result, u_id=u_id , created_at = timezone.now())
#         emp.save()
#         return redirect('viewresult')

#     return render(request, 'predictions.html')

def pred(request):
    if request.method == 'POST':
        u_id = request.session.get('uid')
        myfile = request.FILES.get('image')

        if not myfile:
            return render(request, 'predictions.html', {'error': 'No file uploaded'})

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_path = fs.path(filename)

        # Delete previous input if exists
        test_image_path = "media/input/test/test.jpg"
        if os.path.exists(test_image_path):
            os.remove(test_image_path)

        fs.save('input/test/test.jpg', myfile)

        # Check if the file exists before prediction
        if not os.path.exists(test_image_path):
            return render(request, 'predictions.html', {'error': 'File not saved correctly'})

        # Run Prediction
        try:
            result = predict(test_image_path)  # Ensure this function is correct
            print("Prediction Result:", result)
        except Exception as e:
            return render(request, 'predictions.html', {'error': f'Prediction failed: {str(e)}'})

        # Save result to database
        emp = patient_result(image=filename, result=result, u_id=u_id, created_at=timezone.now())
        emp.save()

        return redirect('viewresult')

    return render(request, 'predictions.html')







def viewresult(request):
    # Get the latest result for the user
    u_id = request.session['uid']
    latest_result = patient_result.objects.filter(u_id=u_id).order_by('-created_at').first()
    # print(latest_result)

    if latest_result:
        recommendation = Recommendation.objects.filter(
            severity_level=latest_result.result
        ).order_by('-created_at').first()
        
        context = {
            'result': latest_result,
            'recommendation': recommendation}
        print(context)


        return render(request, 'viewresult.html', context)
    else:
        return render(request, 'index.html')   
   

       
def viewuser(request):
    sel=patient.objects.all()
    return render(request,'viewuser.html',{'res':sel}) 

def viewexpert(request):
    sel=expert_tbl.objects.all()
    return render(request,'view_expert.html',{'res':sel})            

def viewresults(request):
    sel=patient_result.objects.all()
    return render(request,'viewresults.html',{'res':sel})      


def diet(request):
    res = patient_result.objects.all()  
    return render(request, 'diet.html', {'res': res})
   
   
def rec(request):    
    return render(request, 'recommend.html')


   
from django.shortcuts import render
from django.utils import timezone  
from .models import Recommendation  

def addrec(request):  
    if request.method == 'POST':
        e_id = request.session.get('eid', 'Unknown')  
        diet = request.POST.get('diet')
        severity = request.POST.get('severity')
        lifestyle = request.POST.get('lifestyle')  


        rec = Recommendation(
            severity_level=severity,
            diet=diet,
            lifestyle=lifestyle,
            created_by_name=e_id,
            created_at=timezone.now() 
        )
        rec.save()

        return render(request, 'index.html', {'res': "Recommendations added successfully"})

    return render(request, 'index.html', {'res': "Invalid request"})

from urllib.parse import urlencode
import pycurl

def sends_mail(mail,msg):
	crl = pycurl.Curl()
	crl.setopt(crl.URL, 'https://alc-training.in/gateway.php')
	data = {'email': mail,'msg':msg}
	pf = urlencode(data)

	# Sets request method to POST,
	# Content-Type header to application/x-www-form-urlencoded
	# and data to send in request body.
	crl.setopt(crl.POSTFIELDS, pf)
	crl.perform()
	crl.close()

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        # Check if the email exists in the database
        if patient.objects.filter(email=email).exists():
            user = patient.objects.get(email=email)  # Fetch user details
            
            # WARNING: Ensure passwords are not stored in plain text!
            # If passwords are hashed, you cannot retrieve them.
            # Instead, generate a password reset link or temporary password.
            msg = f"Your email: {user.email}\nYour password: {user.password}"
            
            sends_mail(user.email, msg)
            
            return redirect('login')
        else:
            return redirect('forget_password')

    return render(request, 'forget_password.html')



def feedback(request):
    return render(request,'feedback.html')

def addfeedback(request):
    user=request.session['uid']
    user_instance = get_object_or_404(patient, id=user) 
    if request.method=='POST':
        a=request.POST.get('message')
        ins=feed_tbl(message=a,user=user_instance)
        ins.save()
        messages.success(request, "Feedback successfully completed")

    return render(request,'feedback.html')

def viewfeedback(request):
    sel=feed_tbl.objects.all()
    return render(request,'viewfeedback.html',{'res':sel}) 

def viewrequest(request):
    sel=expert_tbl.objects.filter(status="pending")
    return render(request,'view_request.html',{'res':sel}) 

def accept(request,id):
    sel=get_object_or_404(expert_tbl, id=id)
    sel.status="accepted"
    sel.save()
    # comptb=expert_tbl.objects.get(id=id)
    # userid=expert_tbl.userid
    # x=expert_tbl.objects.get(id=eid)
    email=sel.email
    sends_mail(email,'Request Accepted')
    # return redirect(viewcomplaint)
    return redirect('viewrequest')

def reject(request,id):
    sel=get_object_or_404(expert_tbl, id=id)
    sel.status="rejected"
    sel.save()
    # comptb=expert_tbl.objects.get(id=id)
    # userid=expert_tbl.userid
    # x=expert_tbl.objects.get(id=eid)
    email=sel.email
    sends_mail(email,'Request Rejected')
    # retur
    return redirect('viewrequest')

def viewrecomment(request):
    sel=Recommendation.objects.all()
    return render(request,'viewrecomment.html',{'res':sel})
              

def edit_recommendation(request, id):
    recommendation = get_object_or_404(Recommendation, id=id)

    if request.method == "POST":
        severity_level = request.POST.get("severity_level")
        diet = request.POST.get("diet")
        lifestyle = request.POST.get("lifestyle")

        recommendation.severity_level = severity_level
        recommendation.diet = diet
        recommendation.lifestyle = lifestyle
        recommendation.save()

        messages.success(request, "Recommendation updated successfully!")
        return redirect("recommendations_list")  # Change this to your list view name

    return render(request, "edit.html", {"recommendation": recommendation})




from django.http import JsonResponse
from django.shortcuts import render
from ML.chatbot_logic import get_chatbot_response


# Load chatbot page
def chatbot(request):
    return render(request, 'chatbot.html')

# Process chatbot responses
def chatbot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')
        bot_reply = get_chatbot_response(user_message)
        return JsonResponse({'response': bot_reply})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

