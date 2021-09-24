from django.shortcuts import render, redirect
import email
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import post, answer, reply
import uuid



def get_feedback(name, email, message):

    subject = 'A user wants to contact Aggred.'
    message = message

    email_from = email


    if email_from != False and name != False and message != False:

        send_mail(subject,
        f'This message was sent by {name}, mail id: {email_from}.' + '\n' + '\n' + message,
        email_from,
        [f'{settings.EMAIL_HOST_USER}'],
        fail_silently = False)






def message_screen(request):

    return render(request, 'message_screen.html')





def home(request):

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        get_feedback(name, email, message)

        heading = 'Thank You For Contacting Us.'
        message = 'Please wait while you are being redirected to the home page.'

        return render(request, 'message_screen.html', {'heading': heading, 'message': message})


    elif request.method == 'GET':


        if request.user.is_active:

            logged_in = True

        else:

            logged_in = False

        return render(request, 'home.html', {'logged_in': f'{logged_in}'})



@login_required(login_url='signin')
def forum(request):

    if request.method == 'POST':


        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        form_submit = request.POST.get('submit_btn', False)

        print(title, explanation, form_submit)

        valid_ = title and explanation and form_submit

        full_name = request.user.first_name + ' ' + request.user.last_name



        if not valid_:

            return render(request, 'error_message.html', {'heading': 'An Error Occured', 'message': 'Please try again later.'})

        else:

            # if a question is posted:

            if form_submit == "posting_question":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation, user_title=request.user.title)
                new_post.save()

                return redirect(f'forum/post/{post_id}')



    elif request.method == 'GET':

        if request.user.is_verified:

            logged_in = 'True'

        else:

            logged_in = 'False'

        return render(request, 'forum.html', {'logged_in': logged_in})




@login_required(login_url='signin')
def category_posts(request):

    pass



@login_required(login_url='signin')
def post_id(request, post_id):

    if request.method == 'GET':

        # sending post data:

        post_data = post().__class__.objects.filter(post_id=post_id).first()

        
        full_name = post_data.full_name
        image_url = post_data.user_image_url
        likes = post_data.likes
        title = post_data.post_title
        content = post_data.post_content
        post_date = post_data.post_date
        answers = post_data.answers

        user_title = post_data.user_title

        post_date = post_data.post_date


        # sending answer data (if any):

        answers_data = answer.objects.filter(post_id=post_id).all()

        if answers_data is not None:

            print(answers_data)
            answers_exist = 'True'

        else:

            answers_exist = 'False'
        

        # sending replies data (if any):

        replies_data = reply.objects.filter(post_id=post_id).all()

        if replies_data is not None:

            print(replies_data)
            replies_exist = 'True'

        else:

            replies_exist = 'False'


        return render(request, 'post.html', {'answers_exist': answers_exist, 'replies_exist': replies_exist,'full_name': full_name, 'post_date': post_date, 'image_url': image_url, 'likes': likes, 'title': title, 'content': content, 'post_date': post_date, 'answers': answers, 'user_title': user_title})


    elif request.method == 'POST':


        title = request.POST.get('title', False)
        explanation = request.POST.get('explanation', False)
        form_submit = request.POST.get('submit_btn', False)

        valid_ = title and explanation and form_submit

        full_name = request.user.first_name + ' ' + request.user.last_name



        if not valid_:

            return render(request, 'error_message.html', {'heading': 'An Error Occured', 'message': 'Please try again later in the server.'})

        else:

            # if a question is posted:

            if form_submit == "posting_question":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation)

                return redirect(f'forum/post/{post_id}')




@login_required(login_url='signin')
def saved_posts(request):

    pass




@login_required(login_url='signin')
def my_posts(request):

    pass