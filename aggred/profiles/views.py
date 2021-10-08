from django.shortcuts import render, redirect
import datetime
from .models import profile
import uuid 
from django.contrib.auth import authenticate, get_user_model, logout, login
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.http import Http404, HttpResponseRedirect

from django.core.files.storage import FileSystemStorage

import boto3
from botocore.exceptions import NoCredentialsError
from boto3.s3.transfer import S3Transfer
import os
import random, string

import time






# helper function:
def important_details_form(request):

    if request.user.country == '' or request.user.category == '':

        return HttpResponseRedirect('/signup/important_form')

    else:

        pass






# #function that stores file to S3 instance

def upload_to_aws(local_file, bucket, s3_file):

    print('uploading to AWS....')

    region = "ap-south-1" # keep it hard coded for now

    # s3 = boto3.client('s3', 
    # aws_access_key_id= settings.AWS_ACCESS_KEY_ID,
    # aws_secret_access_key= settings.AWS_SECRET_ACCESS_KEY,
    # region_name=region)

    s3 = boto3.client('s3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    # transfer = S3Transfer(s3)

    image_type = os.path.splitext(local_file)[1]

    mimetype = "image/"+image_type.replace('.','')  # find this on basis of file uploaded
    s3.upload_file(local_file, bucket, s3_file)
    # , extra_args={'ACL': 'public-read', "ContentType": mimetype}
    url = 'https://{}.s3.{}.amazonaws.com/{}'.format(bucket, region, s3_file)
    return url



def delete_from_aws(old_image_url):

    print('deleting from AWS....')


    keyId = settings.AWS_ACCESS_KEY_ID
    sKeyId = settings.AWS_SECRET_ACCESS_KEY

    #Name of the file to be deleted
    srcFileName = old_image_url.split('/')[-2] + '/' + old_image_url.split('/')[-1] 

    #Name of the bucket, where the file resides
    bucketName= settings.AWS_STORAGE_BUCKET_NAME 

    # conn = boto.connect_s3(keyId,sKeyId) #Connect to S3
    # bucket = conn.get_bucket(bucketName) #Get the bucket object

    # k = Key(bucket,srcFileName) #Get the key of the given object

    # k.delete() #Delete the object

    client = boto3.client('s3',
    aws_access_key_id=keyId,
    aws_secret_access_key=sKeyId)

    client.delete_object(Bucket=bucketName, Key=srcFileName)





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

        email = request.POST.get('login', False)
        password = request.POST.get('password', False)

        normal_login = email and password


        if normal_login:

            user = authenticate(email=email, password=password)

            if user is not None:

                login(request, user)

                return render(request, 'home.html')

            else:

                return render(request, 'error_message.html', {'heading': 'Authentication Failed!', 'message': 'Please re-check your details and try again.'})


        else:

            return render(request, 'error_message.html', {'heading': 'An Error Occured.', 'message': 'Please try again in a moment.'})


    elif request.method == 'GET':

        return render(request, 'signin.html')





def signup(request):



    if request.method == 'POST':

        email = request.POST.get('login', False)
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






def important_details(request):


    if request.method == 'GET':

        if request.user.country != '' or request.user.category != '':

            raise Http404('Sorry, no such page exists')

        else:

            return render(request, 'important_details.html')


    
    elif request.method == 'POST':

        country = request.POST.get('country', False)
        category = request.POST.get('category', False)


        user_model = profile.objects.filter(email=request.user.email).first()
        
        user_model.country = country
        user_model.category = category
        user_model.save()

        return HttpResponseRedirect('/forum')





def verify_email(request, auth_token):

    user = profile().__class__.objects.filter(auth_token=auth_token)

    if user.exists() and not user.first().is_verified:

        current_user = profile().__class__.objects.filter(auth_token=auth_token).first()

        current_user.is_verified = True
        current_user.save()

        return render(request, 'message_screen.html', {'heading': 'Email Successfully Verified!', 'message': 'You will be redirected to the home page in a second.'})
    
    else:

        return render(request, 'error_message.html', {'heading': 'An Error Occured.', 'message': 'Please re-check the URL and try again'})




@login_required(login_url='signin')
def settings_(request):

    if request.method == 'GET':

        important_details_form(request)

        logged_in = request.user.social_user or request.user.is_authenticated

        return render(request, 'settings.html', {'social_user': f'{request.user.social_user}', 'user_image_url': request.user.user_image_url, 'logged_in': logged_in})



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

        important_details_form(request)

        return render(request, 'delete_confirmation.html', {'heading': 'Are you sure you want to delete this account?', 'message': 'This action cannot be reversed.', 'redirect_path': 'settings'})




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

        important_details_form(request)

        if request.user.social_user == True:

            return render('/')

        else:

            logged_in = request.user.is_authenticated or request.user.social_user

            return render(request, 'change_password.html', {'logged_in': logged_in})





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

        important_details_form(request)

        logged_in = request.user.is_authenticated or reqeust.user.social_user

        return render(request, 'change_email.html', {'logged_in': logged_in})






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

        important_details_form(request)

        logged_in = request.user.is_authenticated or request.user.social_user

        return render(request, 'change_title.html', {'logged_in': logged_in})




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

        important_details_form(request)


        if request.user.social_user == True:

            return render('/')

        else:

            logged_in = request.user.is_authenticated or request.user.social_user

            return render(request, 'change_name.html', {'logged_in':logged_in})




@login_required(login_url='signin')
def edit_profile_image(request):

    if request.method == 'GET':

        important_details_form(request)

        return render(request, 'edit_profile_image.html')


    elif request.method == 'POST':

        pic_upload = request.FILES.get('image_upload', False)


        print(pic_upload)

        if pic_upload != False:

            print('processing and saving image...')


            #######  Saving uploaded image to local temp folder  ##########


            # fs = FileSystemStorage(location='\\static\\temp')

            fs = FileSystemStorage(location='static/temp/')

            filename = fs.save(pic_upload.name, pic_upload)

            uploaded_file_url = fs.url(filename)

            print('profile image uploaded at :',  uploaded_file_url)

            # print('filename: ', filename)



            ############  Saving the image file to S3 instance on AWS.   ##############

            file_extension = os.path.splitext(uploaded_file_url)[1].replace('.','')

            print('file extension of image : ', file_extension)

            randomString = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32)).replace('.','')

            s3_image_url = upload_to_aws('static/temp/{file_name}'.format(file_name=filename), 'aggred-pictures', 'profile-pictures/{random_string}.{type}'.format(random_string=randomString, type=file_extension))
            # \\Users\\alpha\\

            if s3_image_url is not None and s3_image_url != '':

                print(request.user.user_image_url)
                
                if str(request.user.user_image_url) != 'https://aggred-pictures.s3.ap-south-1.amazonaws.com/profile-pictures/default_profile_image.png':
                    delete_from_aws(str(request.user.user_image_url))
                
                current_user = profile.objects.filter(email=request.user.email).first()

                current_user.user_image_url = s3_image_url

                current_user.save()

                os.remove(f'static/temp/{filename}')           

                return redirect('/')


            #### deleting image from temp #########

            os.remove(f'static/temp/{filename}')           


            # \\Users\\alpha\\

        # Now we change the data
        
        return HttpResponseRedirect(f'/settings_')