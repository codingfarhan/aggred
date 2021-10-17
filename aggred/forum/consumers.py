from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from profiles.models import *
from .models import *

import json




# All helper functions:

def save_data(userEmail, post_id, action):


    if action == 'like':

        # Updating number of liked on the post:

        post_object = post.objects.filter(post_id=post_id).first()
        post_object.likes += 1
        post_object.save()

        
        #Updating the user's field of liked posts:

        user_object = profile.objects.filter(email=userEmail).first()


        if len(user_object.liked_posts) == 0:

            user_object.liked_posts = post_id

        else:

            user_object.liked_posts += ',' + post_id


    elif action == 'dislike':

        # Updating number of liked on the post:

        post_object = post.objects.filter(post_id=post_id).first()
        post_object.likes -= 1
        post_object.save()


        #Updating the user's field of liked posts:

        user_object = profile.objects.filter(email=userEmail).first()


        if len(user_object.liked_posts) == 1:

            user_object.liked_posts = user_object.liked_posts.remove(post_id, '')

        elif user_object.liked_posts.split(',')[0] == post_id:

            user_object.liked_posts = user_object.liked_posts.remove(f'{post_id},', '')

        else:

            user_object.liked_posts = user_object.liked_posts.remove(f',{post_id}', '')

    
    elif action == 'save':


        #Adding saved post to the saved posts table:

        save_post_object = save_post(email=userEmail, post_id=post_id)
        save_post_object.save()


    elif action == 'unsave':


        #Removing saved post from the saved posts table:

        save_post_object = save_post.objects.filter(email=userEmail, post_id=post_id).first()
        save_post_object.delete()
         





# Websocket Consumer:

class interact_with_post_consumer(AsyncWebsocketConsumer):

    
    #Connecting to Consumer
    async def connect(self):

        self.post_id_ = self.scope['url_route']['kwargs']['post_id_']

        await self.channel_layer.group_add(
            self.post_id_,
            self.channel_name
        )

        await self.accept()



    #Disconnecting from Consumer:
    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.post_id_,
            self.channel_name
        )



    #Receiving data from Websocket:
    async def receive(self, text_data):

        received_data = json.loads(text_data)

        userEmail = received_data['userEmail']
        post_id = received_data['post_id']
        action = received_data['action']


        await sync_to_async(save_data)(userEmail, post_id, action)

        await self.channel_layer.group_send(
            self.post_id_,
            {
                'userEmail': userEmail,
                'post_id': post_id,
                'action': action
            }
        )


    
    #Receiving data from the above function:
    async def send_to_client(self, event):

        userEmail = event['userEmail']
        post_id = event['post_id']
        action = event['action']

        await self.send(text_data=json.dumps({
            'userEmail': userEmail,
            'post_id': post_id,
            'action': action,
        }))
