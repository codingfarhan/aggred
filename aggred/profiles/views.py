from django.shortcuts import render, redirect
import datetime
from .models import profile
import uuid 
from django.contrib.auth import authenticate, get_user_model, logout
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password



def send_email_after_registration(email, auth_token):

    #### sending email on the given id for verification ####
    
    subject = 'Your Account needs to be verified.'
    message = f'Hey, follow this link to verify your account  http://localhost:8000/verify/{auth_token}'
    email_from = settings.EMAIL_HOST_USER
    print(email_from)
    recipient_list = [email]

    send_mail(subject, message, email_from, recipient_list)





def signin(request):

    if request.method == 'POST':

        email = request.POST.get('email', False)
        password = request.POST.get('password', False)

        normal_login = email and password


        if normal_login:

            user = authenticate(email=email, password=password)

            if user is not None:

                return render(request, 'index.html')

            else:

                return render(request, 'error_message.html', {'heading': 'Authentication Failed!', 'message': 'Please re-check your details and try again.'})


        else:

            return render(request, 'error_message.html', {'heading': 'An Error Occured.', 'message': 'Please try again in a moment.'})


    elif request.method == 'GET':

        return render(request, 'signin.html')





def signup(request):



    if request.method == 'POST':

        email = request.POST.get('email', False)
        password = request.POST.get('password', False)
        first_name = request.POST.get('first_name', False)
        last_name = request.POST.get('last_name', False)


        # google_signup = request['POST'].get(google_signup, False)


        signup_user = email and password and first_name and last_name


        if first_name == last_name:

            return render(request, 'error_message.html', {'heading': 'Error', 'message': 'First name and Last name are similar. Please re-enter the details.'})

        elif signup_user:

            # we will signup using our custom user model

            auth_token = str(uuid.uuid4())

            new_user = profile().__class__.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, auth_token = auth_token, social_user=False)

            new_user.save()


            # sending verification mail to the user:

            send_email_after_registration(email, auth_token)

            return render(request, 'message_screen.html', {'heading': 'Verification mail sent.', 'message': 'Please check your inbox for a verification link we just sent you. This is important to verify your account.'})


        elif not signup_user:

            return render(request, 'error_message.html', {'heading': 'Error', 'message': 'Please go back and re-check your details.'})

        

    elif request.method == 'GET':

        return render(request, 'signup.html')




@login_required(login_url='signin')
def signout(request):

    logout(request)
    return redirect('/')




def verify_email(request, auth_token):

    if auth_token == request.user.auth_token:

        current_user = profile().__class__.objects.filter(auth_toke=auth_token).first()

        current_user.is_verified = True
        current_user.save()

        return render(request, 'message_screen.html', {'heading': 'Email Successfully Verified!', 'message': 'You will be redirected to the home page in a second.'})
    
    else:

        return render(request, 'error_message.html', {'heading': 'An Error Occured.', 'message': 'Please re-check the URL and try again'})




@login_required(login_url='signin')
def settings_(request):

    if request.method == 'GET':

        return render(request, 'settings.html', {'social_user': f'{request.user.social_user}'})



@login_required(login_url='signin')
def delete_confirmation(request):

    if request.method == 'POST':

        # deleting user's account:

        user = profile().__class__.objects.filter(email=request.user.email)

        if user.exists():

            user1 = user.first()
            user1.delete()

            return render(request, 'message_screen.html', {'heading': 'Account Successfully Deleted.', 'message': 'We will miss you!'})

        else:

            return render(request, 'error_message.html', {'heading': 'An Error Occured.', 'message': 'Please contact Aggred to resolve this issue.'})


    elif request.method == 'GET':

        return render(request, 'delete_confirmation.html')




@login_required(login_url='signin')
def change_password(request):

    if request.method == 'POST':

        old_password = request.POST.get('old_password', False)
        new_password = request.POST.get('new_password', False)


        if old_password and new_password:

            if check_password(old_password, new_password):

                if old_password == new_password:

                    return render(request, 'error_message.html', {'heading': 'Error', 'message': 'The new password is the same as the old one. Please choose a different password.'})

                else:

                    # change the password here
                    pass

            else:

                return render(request, 'error_message.html', {'heading': 'Error', 'message': 'The old password that you have entered is incorrect.'})


    elif request.method == 'GET':

        if request.user.social_user == True:

            return render('/')

        else:

            return render(request, 'change_password.html')





@login_required(login_url='signin')
def change_email(request):

    if request.method == 'POST':

        password = request.POST.get('password', False)
        new_email = request.POST.get('new_email', False)


        if new_email == request.user.email:

            return render(request, 'error_message.html', {'heading': 'Error', 'message': 'Your new email is the same as your old one. Please enter a new email.'})


        elif check_password(password, request.user.password) == False:

            return render(request, 'error_message.html', {'heading': 'Error', 'message': 'Your password is incorrect. Please try again.'})


        elif new_email != request.user.email and check_password(password, request.user.password):

            auth_token = str(uuid.uuid4())
            send_email_after_registration(new_email, auth_token)

            user = get_user_model()
            user.auth_token = auth_token
            user.is_verified = False

            user.save()

            return render(request, 'message_screen.html', {'heading': 'Verification mail sent', 'message': 'Please check your inbox to verify your new Email.'})


    elif request.method == 'GET':

        return render(request, 'change_email.html')






@login_required(login_url='signin')
def change_title(request):

    if request.method == 'POST':

        title = request.POST.get('title', False)

        if title:

            user = profile().__class__.objects.filter(email=request.user.email).first()
            user.title = title

            user.save()

            return render(request, 'message_screen.html', {'heading': 'Success', 'message': 'Profile Title was successfully saved!'})


    elif request.method == 'GET':

        return render(request, 'change_title.html')




@login_required(login_url='signin')
def change_name(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name', False)
        last_name = request.POST.get('last_name', False)


        if first_name and last_name:

            user = profile().__class__.objects.filter(email=request.user.email).first()
            
            user.first_name = first_name
            user.last_name = last_name

            user.save()

            return render(request, 'message_screen.html', {'heading': 'Success', 'message': 'First Name and Last name were successfully saved!'})


    elif request.method == 'GET':


        if request.user.social_user == True:

            return render('/')

        else:

            return render(request, 'change_name.html')
