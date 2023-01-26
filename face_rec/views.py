from django.shortcuts import render,redirect
from .models import Administraion
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
import cv2
from .models import Enroll
import numpy as np
import face_recognition
import os
from playsound import playsound
from .forms import EnrollForm
import re
import csv
from django.dispatch import receiver
import datetime

def encodings(images):
    encodelist = []
    for img in images:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)

    return encodelist




def Login(request):

    if request.method =='POST':
        print('True')

        user = request.POST['username']
        passd = request.POST['passwd']
        user = authenticate(request,username=user, password=passd)

        if user is not None:
            login(request, user)
            return redirect('home/')
        else:
            messages.success(request, 'Username or Password is not Valid')
            redirect(Login)

    return render(request,'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Succesfully Loged out')
    credential=[]
    return redirect('login')
def signup(request):
    if request.method=='POST':
        UserName = request.POST['User_name']
        fi_name = request.POST['f_name']
        la_name = request.POST['l_name']
        paswd_ = request.POST['passwd']
        passwd_c = request.POST['passwd_c']
        if UserName and fi_name and la_name != '':

            if not re.match('^[A-Za-z]+$', fi_name):
                messages.success(request, 'First Name and Last Name must Contain Letters')
                redirect('signup')

            elif not re.match('^[A-Za-z]+$', la_name):
                    messages.success(request, 'First Name and Last Name must Contain Letters')
                    redirect('signup')
            elif User.objects.filter(username=UserName):
                messages.success(request, 'User Already Exist')
                redirect('signup')
            elif not re.match('^[A-Za-z0-9_-]*$', UserName):
                messages.success(request, 'Username is not Valid')
                redirect('signup')
            else:
                if re.match('^[0-9]*$', UserName) or  re.match('^[_-]*$', UserName):
                    messages.success(request, 'Username is not Valid')
                    redirect('signup')
                else:
                    if paswd_ == passwd_c:

                        obj = User.objects.create_user(username=UserName, first_name=fi_name, last_name=la_name, password=paswd_)
                        obj.save()
                        messages.success(request, 'Succesfully SignUp')
                        return redirect('login')
                    else:
                        messages.success(request, 'Password Not Matched')
                        redirect('signup')
        else:
            messages.success(request, 'Fields are Empty')
            redirect(signup)
    return render(request,'signup.html')
@login_required(login_url='login')
def viewall(request):
    all_is = Enroll.objects.all()
    return render(request, 'view.html', {'all':all_is})
# @allowed_users(allowed_roles=['alidurrani','fahadsaleem'])
@login_required(login_url='login')
def home(request):
        distinctinary ={'id':request.user.id,'username': request.user.username,'f_name':request.user.first_name,'l_name':request.user.last_name}
        all_is = Enroll.objects.all()[::2]
        if request.method == 'POST':
            UserName = request.POST['ed_username']
            if not re.match('^[A-Za-z0-9_-]*$', UserName):
                    messages.success(request, 'Username is not Valid')
            elif User.objects.filter(username=UserName):
                messages.success(request, 'User Already Exist')
            elif request.POST['passwd'] == request.POST['ed_cpasswd']:
                user1 = User.objects.get(id = request.user.id)
                user1.username = request.POST['ed_username']
                user1.set_password(request.POST['ed_cpasswd'])
                user1.save()
                messages.success(request,'Record Updated')
            else:
                messages.success(request,'Password Must Be Same')
        return render(request, 'home.html', {'all':all_is,'ali':distinctinary})

@login_required(login_url='login')
def enroll_new(request):
    if request.method == 'POST' and len(request.FILES) !=0:
        fi_name = request.POST['f_name']
        la_name = request.POST['l_name']
        arid = request.POST['arid_no']
        img1 = request.FILES['image']
        if arid and fi_name and la_name != '':

            if Enroll.objects.filter(Arid_no=arid):
                messages.success(request, 'Already Exist')
                redirect('enroll')
            else:
                obj = Enroll(first_name=fi_name, last_name=la_name, Arid_no=arid, img = img1)
                obj.save()
                return redirect('home')
        else:
            messages.success(request, 'Check Entries')
            redirect('enroll')
    else:
        messages.success(request, 'Check Entries')
        redirect('enroll')
    return render(request, 'enroll.html')

@login_required(login_url='login')
def delete(request,auth_id):
    data = Enroll.objects.get(id=auth_id)
    if len(data.img)>0:
        os.remove(data.img.path)
        data.delete()

    return redirect('home')



def contact(request):
    return render(request, 'contactus.html')

def about_us(request):
    return render(request, 'about.html')
@login_required(login_url='login')

def newis(request):
        path = '/root/Desktop/FYP_Interface/media/images'
        images = []
        classnames = []
        mylist = os.listdir(path)
        print(mylist)
        folder = mylist
        if len(folder)==0:
            return HttpResponse("NO ENTRY OF AUTHORIZED PEROSN IN DATABASE")
        else:
            for cls in mylist:
                if cls:
                    imgs = cv2.imread(f'{path}/{cls}')
                    images.append(imgs)
                    classnames.append(os.path.splitext(cls)[0])
                else:
                    return HttpResponse("NO ENTRY OF AUTHORIZED PEROSN IN DATABASE")

        encodelistknown = encodings(images)
        realtime = cv2.VideoCapture(0)
        header = ['Type', 'Time']
        with open('Unknown_Entries.csv', 'w', encoding='UTF8') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                while True:
                    ret, frame = realtime.read()
                    frame = cv2.resize(frame,(800,600))
                    check = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                    faces = face_recognition.face_locations(check)
                    encode = face_recognition.face_encodings(check,faces)

                    for encodeface, location in zip(encode,faces):
                            matches = face_recognition.compare_faces(encodelistknown,encodeface)
                            face_ds = face_recognition.face_distance(encodelistknown, encodeface)
                            print(face_ds)
                            matchIndex = np.argmin(face_ds)
                            print(matchIndex)

                            if matches[matchIndex]:
                                name = classnames[matchIndex].upper()
                                print(name)
                                y1,x2,y2,x1 = location
                                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0), 2)
                                cv2.putText(frame,f"{name}",(x1,y1),cv2.FONT_HERSHEY_PLAIN,1,(0,255,0),4)
                            else:
                                y1, x2, y2, x1 = location
                                playsound('/root/Desktop/FYP/sounds/beep.wav')
                                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                                x = datetime.datetime.now()
                                data = ['Unknown', x, ]
                                writer.writerow(data)
                    cv2.imshow("Name",frame)
                    keyCode=cv2.waitKey(250)
                    if (keyCode & 0xFF) == ord("q"):
                        cv2.destroyAllWindows()
                        break
                realtime.release()

        return redirect('home')
