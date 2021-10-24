from django.shortcuts import render, redirect
import email
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import post, answer, reply
import uuid
import json
import datetime
from django.http import Http404, HttpResponseRedirect
from profiles.models import profile, save_post
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# for advanced Search:
from django.contrib.postgres.search import SearchQuery, SearchVector






# helper function:
def important_details_form(request):

    if request.user.country == '' or request.user.category == '':

        return HttpResponseRedirect('/signup/important_form')

    else:

        pass





def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


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





# Saving Data from AJAX request:

def save_data(userEmail, post_id, action, request):


    if action == 'like':

        # Updating number of liked on the post:

        post_object = post.objects.filter(post_id=post_id).first()
        post_object.likes += 1
        post_object.save()

        
        #Updating the user's field of liked posts:

        user_object = profile.objects.filter(email=userEmail).first()


        if len(user_object.liked_posts) == 0:

            user_object.liked_posts = post_id
            user_object.save()

        else:

            user_object.liked_posts += ',' + post_id
            user_object.save()


    elif action == 'dislike':

        # Updating number of liked on the post:

        post_object = post.objects.filter(post_id=post_id).first()
        post_object.likes -= 1
        post_object.save()


        #Updating the user's field of liked posts:

        user_object = profile.objects.filter(email=userEmail).first()


        if ',' not in user_object.liked_posts and user_object.liked_posts != '':

            user_object.liked_posts = user_object.liked_posts.replace(post_id, '')
            print('post disliked updated the users profile table.')

        elif ',' in user_object.liked_posts and user_object.liked_posts.split(',')[0] == post_id:

            user_object.liked_posts = user_object.liked_posts.replace(f'{post_id},', '')
            print('post disliked updated the users profile table.')

        else:

            user_object.liked_posts = user_object.liked_posts.replace(f',{post_id}', '')
            print('post disliked updated the users profile table.')

        
        user_object.save()

    
    elif action == 'save':


        #Adding saved post to the saved posts table:

        save_post_object = save_post(email=userEmail, post_id=post_id)
        save_post_object.save()


    elif action == 'unsave':


        #Removing saved post from the saved posts table:

        save_post_object = save_post.objects.filter(email=userEmail, post_id=post_id).first()
        save_post_object.delete()


    elif action == 'vote':

        # adding a vote to the post:

        answer_ = answer.objects.filter(answer_id=post_id).first()

        answer_.votes += 1
        answer_.save()


        # adding answer_id to the profile's voted_answers field:

        user_object = profile.objects.filter(email=request.user.email).first()

        if len(user_object.voted_answers) == 0:

            user_object.voted_answers = post_id
            user_object.save()

        else:

            user_object.voted_answers += f',{post_id}'
            user_object.save()

        
        user_object.save()

    
    elif action == 'undovote':

        # removing vote from the answer:

        answer_ = answer.objects.filter(answer_id=post_id).first()

        answer_.votes -= 1
        answer_.save()


        #Updating the user's field of liked posts:

        user_object = profile.objects.filter(email=userEmail).first()


        if ',' not in user_object.voted_answers and user_object.voted_answers != '':

            user_object.voted_answers = user_object.voted_answers.replace(post_id, '')
            print('answer undovote updated the users profile table. 1')

        elif ',' in user_object.voted_answers and user_object.voted_answers.split(',')[0] == post_id:

            user_object.voted_answers = user_object.voted_answers.replace(f'{post_id},', '')
            print('answer undovote updated the users profile table. 2')

        else:

            user_object.voted_answers = user_object.voted_answers.replace(f',{post_id}', '')
            print('answer undovote updated the users profile table. 3')

        
        user_object.save()








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

        return render(request, 'home.html', {'logged_in':logged_in})





@login_required(login_url='signin')
def forum(request):

    if request.method == 'POST':


        # CHECKING IF POST FORM HAS BEEN FILLED:

        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        post_form_submit = request.POST.get('post_question', False)

        post_class = request.POST.get('post_class', False)
        post_subject_or_course = request.POST.get('post_subject_or_course', False)


        print(title, explanation, post_class, post_subject_or_course, post_form_submit)

        filled_post_form = title != False and explanation  != False and post_form_submit != False

        print(filled_post_form)

        full_name = request.user.first_name + ' ' + request.user.last_name



        if not filled_post_form:

            return render(request, 'error_message.html', {'heading': 'An Unexpected Error Occured', 'message': 'Please try again later.'})

        elif filled_post_form:

            # if a question is posted:

            if post_form_submit == "POST":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, grade=post_class, subject=post_subject_or_course, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation, user_title=request.user.title)
                new_post.save()

                return redirect(f'forum/post/{post_id}')

        else:

            return render(request, 'error_message.html', {'heading': 'Unexpected Error', 'message': 'Please try again in a while'})



    elif request.method == 'GET':

        important_details_form(request)

        if request.user.is_authenticated or request.user.social_user:

            logged_in = True

        else:

            logged_in = False

        return render(request, 'forum.html', {'logged_in': logged_in, 'image_url': request.user.user_image_url})






@login_required(login_url='signin')
def category_posts(request, class_, subject, search_query):

    
    if request.method == 'GET':

        important_details_form(request)

        search_query = search_query.replace("+", " ")

        print(class_, subject, search_query)

        no_results = 'False'



        if search_query == "all":

            print('search = all')
            print('search query is ', search_query)



            if class_ != "None" and subject != "None":

                result_set = list(post.objects.filter(grade=class_, subject=subject).values())

            elif class_ == "None" and subject != "None":

                result_set = list(post.objects.filter(subject=subject).values())

            elif class_ != "None" and subject == "None":

                result_set = list(post.objects.filter(grade=class_).values())

            else:

                result_set = list(post.objects.all().values())


        
        elif search_query != "all":

            print('search != all')

            print('search query is ', search_query)


            vector = SearchVector('post_title', 'post_content')
            query = SearchQuery(search_query)


            if class_ != "None" and subject != "None":

                result_set = list(post.objects.annotate(search=vector).filter(grade=class_, subject=subject, search=query).values())

            elif class_ == "None" and subject != "None":

                result_set = list(post.objects.annotate(search=vector).filter(subject=subject, search=query).values())

            elif class_ != "None" and subject == "None":

                result_set = list(post.objects.annotate(search=vector).filter(grade=class_, search=query).values())

            else:

                result_set = list(post.objects.annotate(search=vector).filter(search=query).values())




        context = []

        # qs = json.loads(result_set)
        # print(qs)


        if result_set != [] and len(result_set) != 0 and result_set[0] != None:

            for item in result_set:
                context.append({'post_id': item['post_id'], 'email': item['email'], 'user_image_url': item['user_image_url'], 'full_name': item['full_name'], 'user_title': item['user_title'], 'post_title': item['post_title'], 'post_content': item['post_content'], 'likes': item['likes'], 'post_date': item['post_date'], 'answers': item['answers'], 'redirect_url': f"forum/post/{item['post_id']}"})



        if result_set == [] and len(context) == 0:
            no_results = 'True'

        
        logged_in = request.user.is_authenticated or request.user.social_user
        print(logged_in)

        return render(request, 'category_posts.html', {'context': context, 'search': search_query, 'no_results': no_results, 'number_of_results': len(context), 'logged_in': logged_in, 'image_url': request.user.user_image_url})


    elif request.method == 'POST':


        # CHECKING IF POST FORM HAS BEEN FILLED:

        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        post_form_submit = request.POST.get('post_question', False)

        post_class = request.POST.get('post_class', False)
        post_subject_or_course = request.POST.get('post_subject_or_course', False)


        print(title, explanation, post_class, post_subject_or_course, post_form_submit)

        filled_post_form = title != False and explanation  != False and post_form_submit != False

        print(filled_post_form)

        full_name = request.user.first_name + ' ' + request.user.last_name



        if not filled_post_form:

            return render(request, 'error_message.html', {'heading': 'An Unexpected Error Occured', 'message': 'Please try again later.'})

        elif filled_post_form:

            # if a question is posted:

            if post_form_submit == "POST":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, grade=post_class, subject=post_subject_or_course, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation, user_title=request.user.title)
                new_post.save()

                return HttpResponseRedirect(f'/forum/post/{post_id}')

        else:

            return render(request, 'error_message.html', {'heading': 'Unexpected Error', 'message': 'Please try again in a while'})










def post_id(request, post_id):

    if request.method == 'GET':


        # sending post data:

        post_data = post().__class__.objects.filter(post_id=post_id).first()

        print(f'here is the question: {post_data}')

        if post_data is None:

            raise Http404("Post does not exist. Are you sure the URL is correct?")

        else:

            already_answered = str(answer.objects.filter(post_id=post_id, email=request.user.email).exists())

        
            full_name = post_data.full_name
            image_url = post_data.user_image_url
            likes = post_data.likes
            title = post_data.post_title
            content = post_data.post_content
            post_date = post_data.post_date
            answers = post_data.answers

            post_id = post_data.post_id

            user_title = post_data.user_title

            post_date = post_data.post_date

            email = post_data.email

            liked = post_id in request.user.liked_posts
            saved = save_post.objects.filter(email=request.user.email, post_id=post_id).exists()


            answers_list = []
            replies_list = []


            # sending answer data (if any):

            answers_data = list(answer.objects.filter(post_id=post_id).values())

            print(f' here are the answers: {answer.objects.filter(post_id=post_id).values()}')

            if answers_data != []:

                # qs = json.loads(answers_data)

                # print(qs)
                answers_exist = 'True'

                for item in answers_data:

                    if item['answer_id'] in request.user.voted_answers:
                        voted = True
                    else:
                        voted = False

                    print(f'voted: {voted}')

                    answers_list.append({'voted': voted,'full_name': item['full_name'], 'email': item['email'], 'answer_id': item['answer_id'], 'image': item['user_image_url'], 'user_title': item['user_title'], 'answer_title': item['answer_title'], 'answer_content': item['answer_content'], 'time_stamp': item['timestamp'], 'votes': item['votes']})


            else:

                answers_exist = 'False'
            


            # sending replies data (if any):


            replies_data = list(reply.objects.filter(post_id=post_id).values())


            if replies_data != []:

                # qs = json.loads(replies_data)

                # print(qs)
                replies_exist = 'True'

                for item in replies_data:

                    replies_list.append({'full_name': item['full_name'], 'reply_id': item['reply_id'], 'email': item['email'], 'replying_to': item['replying_to'], 'answer_id': item['answer_id'], 'image': item['user_image_url'], 'reply_content': item['reply_content'], 'time_stamp': item['reply_date']})


            else:

                replies_exist = 'False'

            logged_in = request.user.is_authenticated or request.user.social_user

            
            print(f'liked: {liked}, saved: {saved}')


            return render(request, 'post.html', {'liked': liked, 'saved': saved, 'userEmail': request.user.email, 'email': email, 'already_answered': already_answered, 'answers_exist': answers_exist, 'answers_list': answers_list, 'replies_exist': replies_exist, 'replies_list': replies_list, 'full_name': full_name, 'image_url': image_url, 'likes': likes, 'title': title, 'content': content, 'post_date': post_date, 'answers': answers, 'post_id': post_id, 'user_title': user_title, 'logged_in': logged_in, 'image_url': request.user.user_image_url})


    elif request.method == 'POST':


        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        post_form_submit = request.POST.get('post_question', False)

        class_ = request.POST.get('post_class', False)
        subject = request.POST.get('post_subject_or_course', False)


        filled_post_or_answer_form = title != False and explanation != False and post_form_submit != False
        filled_reply_form = explanation != False and post_form_submit != False


        full_name = request.user.first_name + ' ' + request.user.last_name



        # for debugging:

        print('for debugging: ', title)


        if not filled_post_or_answer_form and not filled_reply_form:

            return render(request, 'error_message.html', {'heading': 'An Error Occured', 'message': 'Please try again later.'})

        else:

            # if a question is posted:

            if post_form_submit == "POST":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, user_title=request.user.title, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation, grade=class_, subject=subject)
                new_post.save()

                return HttpResponseRedirect(request.path_info)


            elif post_form_submit == "Answer":

                # saving answer:


                ans_id = str(uuid.uuid4())

                new_ans = answer(post_id=post_id, answer_id=ans_id, full_name=full_name, email=request.user.email, user_title=request.user.title, user_image_url=request.user.user_image_url, answer_title=title, answer_content=explanation)
                new_ans.save()



                # updating number of answers of the  question:

                question_ = post.objects.filter(post_id=post_id).first()
                question_.answers += 1
                question_.save()

                return HttpResponseRedirect(request.path_info)

            
            elif post_form_submit.split(',')[0] == "Reply To Answer" or post_form_submit.split(',')[0] == "Reply":

                # saving reply:

                reply_id = str(uuid.uuid4())

                print(f'explanation : {explanation}')

                new_reply = reply(reply_id=reply_id, replying_to=post_form_submit.split(',')[-1], post_id=post_id, answer_id=post_form_submit.split(',')[1], email=request.user.email, user_image_url=request.user.user_image_url, full_name=request.user.first_name + ' ' + request.user.last_name, reply_content=explanation)
                new_reply.save()

                return HttpResponseRedirect(request.path_info)





@login_required(login_url='signin')
def edit_post(request, post_id):

    if request.method == 'GET':

        important_details_form(request)

        post_data = post.objects.filter(post_id=post_id).first()

        post_content = post_data.post_content
        post_title = post_data.post_title

        logged_in = request.user.is_authenticated or request.user.social_user

        return render(request, 'edit_post.html', {'post_content': post_content, 'post_title': post_title, 'logged_in': logged_in, 'image_url': request.user.user_image_url})


    elif request.method == 'POST':

        content = request.POST.get('details', False)
        # title = request.POST.get('title', False)

        post_ = post.objects.filter(post_id=post_id).first()


        # editing values for the post:
        post_.post_content = content
        # post_.post_title = title

        post_.save()

        return HttpResponseRedirect(f'/forum/post/{post_id}')





@login_required(login_url='signin')
def edit_answer(request, answer_id):

    answer_ = answer.objects.filter(answer_id=answer_id).first()

    if request.method == 'GET':

        important_details_form(request)


        answer_content = answer_.answer_content
        answer_title = answer_.answer_title

        logged_in = request.user.is_authenticated or request.user.social_user


        return render(request, 'edit_answer.html', {'answer_content': answer_content, 'answer_title': answer_title, 'logged_in': logged_in, 'image_url': request.user.user_image_url})

    
    elif request.method == 'POST':

        title = request.POST.get('title', False)
        content = request.POST.get('details', False)

        answer_.answer_title = title
        answer_.answer_content = content


        post_id = answer_.post_id
        answer_.save()

        return HttpResponseRedirect(f'/forum/post/{post_id}')




@login_required(login_url='signin')
def edit_reply(request, reply_id):

    reply_ = reply.objects.filter(reply_id=reply_id).first()


    if request.method == 'GET':

        important_details_form(request)

        content = reply_.reply_content

        logged_in = request.user.is_authenticated or request.user.social_user

        return render(request, 'edit_reply.html', {'reply_content': content, 'logged_in': logged_in, 'image_url': request.user.user_image_url})



    elif request.method == 'POST':

        new_content = request.POST.get('details', False)

        reply_.reply_content = new_content
        reply_.save()

        post_id = reply_.post_id

        return HttpResponseRedirect(f'/forum/post/{post_id}')







@login_required(login_url='signin')
def delete_post(request, post_id):


    if request.method == 'GET':

        important_details_form(request)

        qs = answer.objects.filter(post_id=post_id)
        delete_ = True

        votes_count = 0

        # can only delete post if there are 0 answers that have been given a lot of votes (we assume that number to be 20 here).

        if qs.exists():

            for item in qs.values():

                votes_count += item['votes']

                if votes_count >= 25:

                    delete_ = False

                    return render(request, 'error_message.html', {'heading': 'Delete Unsuccessful', 'message': 'You cannot delete this question from the forum as a significant number of people have already interacted with it. Do you want to edit it instead?'})


        if delete_ == True:         
        
            return render(request, 'delete_confirmation.html', {'heading': 'Are you sure you want to delete this post?', 'message': 'This is an irreversable action.', 'redirect_path': 'forum', 'image_url': request.user.user_image_url})


    elif request.method == 'POST':


        # delete the post

        del_post = post.objects.filter(post_id=post_id).first()
        del_post.delete()

        # delete all associated answers

        del_answers = answer.objects.filter(post_id=post_id).all()

        for row in del_answers:
            row.delete()

        # delete all associated replies

        del_replies = reply.objects.filter(post_id=post_id).all()

        for row in del_replies:
            row.delete()

        return render(request, 'message_screen.html', {'heading': 'Delete Successful', 'message': 'Your post was successfuly deleted.'})






@login_required(login_url='signin')
def delete_answer(request, answer_id):

    answer_ = answer.objects.filter(answer_id=answer_id).first()
    post_object = post.objects.filter(post_id=answer_.post_id).first()

    
    if request.method == 'GET':

        important_details_form(request)

        return render(request, 'delete_confirmation.html', {'heading': 'Delete Confirmation', 'message': 'Are you sure you want to delete this answer? This action cannot be reversed.', 'redirect_url': f'forum/post/{answer_.post_id}', 'image_url': request.user.user_image_url})


    elif request.method == 'POST':

        answer_.delete()

        post_object.answers -= 1
        post_object.save()

        return render(request, 'message_screen.html', {'heading': 'Delete Successful', 'message': 'Your answer was successfully deleted.'})





@login_required(login_url='signin')
def delete_reply(request, reply_id):

    reply_ = reply.objects.filter(reply_id=reply_id).first()


    if request.method == 'GET':

        important_details_form(request)

        return render(request, 'delete_confirmation.html', {'heading': 'Delete Confirmation', 'message': 'Are you sure you want to delete this reply?', 'redirect_url': f'forum/post/{reply_.post_id}', 'image_url': request.user.user_image_url})


    elif request.method == 'POST':

        reply_.delete()

        return render(request, 'message_screen.html', {'heading': 'Delete Successful', 'message': 'Your reply was successfully deleted.'})






@login_required(login_url='signin')
def saved_posts(request):

    if request.method == 'GET':

        important_details_form(request)

        pass




@login_required(login_url='signin')
def my_posts(request):

    if request.method == 'GET':

        important_details_form(request)

        user_email = request.user.email

        posts = list(post.objects.filter(email=user_email).values())


        context = []


        if posts != []:
            # qs = json.loads(posts)

            for item in posts:
                context.append({'post_id': item['post_id'], 'email': item['email'], 'user_image_url': item['user_image_url'], 'full_name': item['full_name'], 'user_title': item['user_title'], 'post_title': item['post_title'], 'post_content': item['post_content'], 'likes': item['likes'], 'post_date': item['post_date'], 'answers': item['answers'], 'redirect_url': f"forum/post/{item['post_id']}"})


        no_of_posts = len(context)
        logged_in = request.user.is_authenticated or request.user.social_user

        return render(request, 'my_posts.html', {'context': context, 'no_of_posts': no_of_posts, 'logged_in': logged_in, 'image_url': request.user.user_image_url})


    elif request.method == 'POST':


        # CHECKING IF POST FORM HAS BEEN FILLED:

        title = request.POST.get('title', False)
        explanation = request.POST.get('details', False)
        post_form_submit = request.POST.get('post_question', False)

        post_class = request.POST.get('post_class', False)
        post_subject_or_course = request.POST.get('post_subject_or_course', False)


        print(title, explanation, post_class, post_subject_or_course, post_form_submit)

        filled_post_form = title != False and explanation  != False and post_form_submit != False

        print(filled_post_form)

        full_name = request.user.first_name + ' ' + request.user.last_name



        if not filled_post_form:

            return render(request, 'error_message.html', {'heading': 'An Unexpected Error Occured', 'message': 'Please try again later.'})

        elif filled_post_form:

            # if a question is posted:

            if post_form_submit == "POST":

                # saving post:

                post_id = str(uuid.uuid4())

                new_post = post(post_id=post_id, email=request.user.email, grade=post_class, subject=post_subject_or_course, user_image_url=request.user.user_image_url, full_name=full_name, post_title=title, post_content=explanation, user_title=request.user.title)
                new_post.save()

                return HttpResponseRedirect(f'/forum/post/{post_id}')

        else:

            return render(request, 'error_message.html', {'heading': 'Unexpected Error', 'message': 'Please try again in a while'})



@csrf_exempt
def like_save_vote(request):

    if request.method == 'POST':

        received_data = json.load(request)

        userEmail = received_data['userEmail']
        post_id = received_data['post_id']
        action = received_data['action']

        save_data(userEmail, post_id, action, request)


        print(userEmail, post_id, action)
        print('AJAX Data saved in the Database.')

        return JsonResponse({'message': f'successfully performed {action}'})