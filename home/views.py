from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Category, Post, Comment, Message

def landingPage(request):
    return render(request, 'html/landingPage.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        citizenship = request.FILES['citizenship']

        try:
            user = User.objects.get(username=username)
            messages.error(request, 'Username is already occupied, try another username')
        except User.DoesNotExist:
            pass

        if password1 == password2:
            user = User(
                first_name=first_name,
                last_name=last_name,
                username=username
            )

            user.set_password(password1)

            user.save()

            user.profile.citizenship = citizenship
            user.profile.save()

            if user:
                login(request, user)
                messages.success(request, 'Account created successfully.')
                return redirect('profile')
            else:
                messages.error(request, 'Registration failed.')
        else:
                messages.error(request, 'Password did\'t match. Register again')

    context = {
        'to': 'register'
    }
        
    return render(request, 'html/index.html', context)

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Invalid username or password')

    return render(request, 'html/index.html')

def logoutUser(request):
    logout(request)
    return redirect('landingPage')


def home(request):
    return render(request, 'html/index.html')


def post(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'home/post.html', context)


def item(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse('Post not found')

    if request.method == 'POST':
        content = request.POST.get('content')
    
        user = request.user
        comment = Comment(
            user=user,
            post=post,
            content=content
        )

        comment.save()
    

    comments = Comment.objects.filter(post=post)
    
    context = {
        'post': post,
        'comments': comments
    }

    return render(request, 'html/item.html', context)


@login_required(login_url='login')
def createPost(request):
    if request.method == "POST":
        user = request.user
        category = request.POST.get('category')

        try:
            category = Category.objects.get(id=int(category))
        except Category.DoesNotExist:
            pass

        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        image = request.FILES['image']

        post = Post(
            category=category,
            user=user,
            title=title,
            description=description,
            location=location,
            image=image
        )

        post.save()

    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'home/createPost.html', context)


@login_required
def updatePost(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse("Post does not exists")

    if request.method == "POST":
        user = request.user
        category = request.POST.get('category')

        print(category)
        try:
            category = Category.objects.get(id=category)
        except Category.DoesNotExist:
            pass

        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        images = request.FILES['images']

        post.category=category
        post.user=user
        post.title=title
        post.description=description
        post.location=location
        post.images=images

        post.save()

        return redirect('post')
    
    categories = Category.objects.all()

    context = {
        'post': post,
        'categories': categories
    }
    return render(request, 'home/updatePost.html', context)


@login_required
def deletePost(request, id):
    try:
        post = Post.objects.get(id=id)
        post.delete()
    except Post.DoesNotExist:
        pass
    return redirect('post')


def comments(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return HttpResponse("Post does not exists")

    comments = Comment.objects.filter(post=post)

    context = {
        'comments': comments,
        'post': post
    }
    return render(request, 'home/comment.html', context)



@login_required
def createComment(request, post_id):
    if request.method == "POST":
        content = request.POST.get('content')
    
        try:
            post = Post.objects.get(id=post_id)
            print(post)
        except Post.DoesNotExist:
            return HttpResponse("Post does not exist.")

        user = request.user
        comment = Comment(
            user=user,
            post=post,
            content=content
        )

        comment.save()

        return redirect('item', id=post_id)


    return render(request, 'home/item.html')


@login_required
def updateComment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return HttpResponse("Post does not exist.")

    if request.method == "POST":
        content = request.POST.get('content')
    
        user = request.user
        comment.content = content
        comment.save()

        return redirect('comments', id=comment.post.id)

    context = {
        'comment': comment
    }
    return render(request, 'home/updateComment.html', context)


@login_required
def deleteComment(request, comment_id):
    try:
        comment = Comment.objects.get(id=comment_id)
        post_id = comment.post.id
        comment.delete()
    except Comment.DoesNotExist:
        pass
    return redirect('item', id=post_id)


@login_required
def message(request, receiver_username):
    sender = request.user
    
    try:
        receiver = User.objects.get(username=receiver_username)
    except User.DoesNotExist:
        return HttpResponse("Receiver Does not exists")

    if request.method == "POST":
        content = request.POST.get('content')

        print(content)
        message = Message(
            sender=sender,
            receiver=receiver,
            content=content,
        )

        message.save()
        return redirect('message', receiver_username=receiver_username)

    conversations = Message.objects.filter(sender=sender, receiver=receiver)
    print(conversations)
    context = {
        'conversations': conversations,
        'receiver': receiver
    }

    return render(request, 'html/messaging.html', context)



@login_required
def deleteMessage(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
        receiver = message.receiver
        if message.sender == request.user:
            message.delete()
        else:
            messages.error(request, 'Cannot delete message created by other user.')
    except Message.DoesNotExist:
        return HttpResponse("Message Does not exists")
    return redirect('message', receiver_username=receiver.username)


@login_required
def profile(request):
    user = request.user
    
    user_posts = Post.objects.filter(user=user)
    
    context = {
        'posts': user_posts
    }

    return render(request, 'html/profile.html', context)



@login_required
def updateUserProfile(request):
    user = request.user
    
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        address = request.POST.get('address')

        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.profile.contact = contact
        user.profile.address = address

        user.profile.save()
        user.save()

        messages.success(request, "Profile updated successfully.")

    return redirect('profile')


@login_required
def updateUserPhoto(request):
    user = request.user
    
    if request.method == "POST":
        photo = request.FILES['photo']

        user.profile.photo = photo
        user.profile.save()

    return redirect('profile')
