from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from grumblr.models import *
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import views
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from mimetypes import guess_type

from .models import *
from .forms import *

def index(request):
	username=''
	password=''
	if 'username' in request.POST:
		username = request.POST['username']
	if 'password' in request.POST:
		password = request.POST['password']
	
	user = authenticate(username=username, password=password)
	if user is not None:
		login(request, user)
		return redirect('global')
	else:
		return redirect('login')

def password_reset(request):
	context = {}
	context['email'] = ''
	if request.method == 'GET':
		return render(request, 'grumblr/registration/password_reset_form.html', context)

	if 'email' in request.POST:
		try:
			user = User.objects.get(username=request.POST['email'])
			token = default_token_generator.make_token(user)
			
			email_body = """Please click the link below to change your password
			http://%s%s """ % (request.get_host(),
			               reverse('password_reset_email', args=(urlsafe_base64_encode(force_bytes(user.id)), token)))

			send_mail(subject="Change password",
				      message=email_body,
				      from_email="yadiy@andrew.cmu.edu",
				      recipient_list=[user.username],
				      fail_silently=False)

			return render(request, 'grumblr/registration/password_reset_done.html', context)		
		except:
			return render(request, 'grumblr/reset_failure.html', context)
	return render(request, 'grumblr/registration/password_reset_done.html', context)

@login_required
def get_photo_profile(request, userid, id):
	profile = get_object_or_404(Profile, owner_id=id)
	if not profile.picture:
		raise Http404
	con_type = guess_type(profile.picture.name)
	return HttpResponse(profile.picture, content_type=con_type)

@login_required
def get_photo(request, id):
	profile = get_object_or_404(Profile, owner_id=id)
	if not profile.picture:
		raise Http404
	con_type = guess_type(profile.picture.name)
	return HttpResponse(profile.picture, content_type=con_type)



@login_required
def profile(request,userid):
	context ={}
	context['user'] = ''
	profile = Profile.objects.filter(owner_id=userid).first()
	if not profile:
		raise Http404
	context['name'] = profile.first_name + " " + profile.last_name
	context['age'] = profile.age
	context['bio'] = profile.bio
	context['picture'] = profile.picture

	post = Post.objects.filter(user=userid).order_by('date')
	#post = Post.objects.filter(user=User.objects.filter(id=11)).order_by('-date')
	context['post'] = post
	context['id'] = userid

	#return render(request, 'grumblr/profile.html', context)
	return render(request, 'grumblr/profile.html', context)

@login_required
def follow_other(request, userid):	
	profileFollow = Profile.objects.filter(owner_id=userid).first()
	profileMine = Profile.objects.filter(owner = request.user).first()
	profileMine.follow.add(profileFollow)

	return redirect('/grumblr/global')

def unfollow(request, userid):
	profileFollow = Profile.objects.filter(owner_id=userid).first()
	profileMine = Profile.objects.filter(owner = request.user).first()
	profileMine.follow.remove(profileFollow)

	return redirect('/grumblr/global')







@login_required
def myProfile(request):
	context ={}
	context['user'] = ''
	if 'user' in request.POST:
		profile = Profile.objects.filter(owner=request.POST['user']).first()
		context['name'] = profile.first_name + " " + profile.last_name
		context['age'] = profile.age
		context['bio'] = profile.bio
		context['picture'] = profile.picture.url
		context['profile'] = Profile.get_profile(request.POST['user'])
		context['id'] = profile.owner.id
		post = Post.objects.filter(user=request.POST['user']).order_by('date')
	else:
		profile = Profile.objects.filter(owner=request.user).first()
		context['name'] = profile.first_name + " " + profile.last_name
		context['age'] = profile.age
		context['bio'] = profile.bio
		context['picture'] = profile.picture.url
		context['profile'] = Profile.get_profile(request.user)
		context['id'] = profile.owner.id
		post = Post.objects.filter(user=request.user).order_by('date')
	#post = Post.objects.filter(user=User.objects.filter(id=11)).order_by('-date')
	
	context['post'] = post
	return render(request, 'grumblr/profile.html', context)



# def add_post(request):
# 	context={}
# 	errors = []
# 	context['errors'] = errors

# 	if not 'post' in request.POST or not request.POST['post']:
# 		errors.append('You must enter something to post.')
# 	else:
# 		new_post = Post(text=request.POST['post'], date=timezone.now(), user=request.user)
# 		new_post.save()


# 	if errors:
# 		user=[]
# 		post = Post.objects.all().order_by('-date')
# 		for postcontent in post:
# 			user.append(User.objects.all().filter(id=postcontent.user_id).first().username)
# 		result = [(post[i], user[i]) for i in range(len(post))]
# 		context['result'] = result
# 		return render(request, 'grumblr/global.html', context)
# 	#context = {'result': result, 'errors' : errors}
# 	#return render(request, 'grumblr/global.html', context)
# 	return redirect('/grumblr/global')


	# if errors:
	# 	user=[]
	# 	userObject=[]
	# 	post = Post.objects.all().order_by('-date')
	# 	comment = []
	# 	profile=[]
	# 	for postcontent in post:
	# 		user.append(User.objects.all().filter(id=postcontent.user_id).first().username)
	# 		userObject.append(User.objects.all().filter(id=postcontent.user_id).first())
	# 		profile.append(Profile.objects.all().get(owner_id=postcontent.user_id))
	# 		commentContent = Comment.objects.all().filter(owner=postcontent).order_by('-date')
	# 		sub = []
	# 		for each in commentContent:
	# 			sub.append(each)
	# 		comment.append(sub)
	# 	result = [(post[i], userObject[i], profile[i], comment[i]) for i in range(len(post))]
	# 	context['result'] = result
	# 	return render(request, 'grumblr/global.html', context)
	# return redirect('/grumblr/global')

def signin(request):
	context = {}

	if request.method =='GET':
		context['form'] = RegistrationForm()
		return render(request, 'grumblr/signin.html', context)

	form = RegistrationForm(request.POST)
	context['form'] = form

	if not form.is_valid():
		return render(request, 'grumblr/signin.html', context)

	new_user = User.objects.create_user(username=form.cleaned_data['username'],
		                                password=form.cleaned_data['password1'])
	new_user.is_active = False

	new_user.save()
	token = default_token_generator.make_token(new_user)

	email_body = """Welcome to Grumblr. Please clicke the link below to verify your email address and
	complete the registration of your count:
	http://%s%s """ % (request.get_host(),
		               reverse('confirm', args=(new_user.username, token)))

	send_mail(subject="Verify your email address",
		      message=email_body,
		      from_email="yadiy@andrew.cmu.edu",
		      recipient_list=[new_user.username],
			  fail_silently=False)

	context['email'] = form.cleaned_data['username']

	return render(request, 'grumblr/confirm.html', context)

@login_required
def globalPage(request):

	

	context = {}
	context['form'] = PostForm()
	context['username'] = request.user
	user=[]
	userObject=[]
	post = Post.objects.all().order_by('date')
	comment = []
	profile=[]
	for postcontent in post:
		user.append(User.objects.all().filter(id=postcontent.user_id).first().username)
		userObject.append(User.objects.all().filter(id=postcontent.user_id).first())
		profile.append(Profile.objects.all().get(owner_id=postcontent.user_id))
		commentContent = Comment.objects.all().filter(owner=postcontent).order_by('date')
		sub = []
		for each in commentContent:
			sub.append(each)
		comment.append(sub)


	result = [(post[i], userObject[i], profile[i], comment[i]) for i in range(len(post))]
	context['result'] = result
	return render(request, 'grumblr/global.html', context)









	#login(request, new_user)
	
#@transation.commit_on_success
def confirm_registration(request, username, token):
	try:
		user = User.objects.get(username=username)
		if default_token_generator.check_token(user, token):
			user.is_active = True
			user.save()
			user.backend='django.contrib.auth.backends.ModelBackend'
			login(request, user)

		return redirect(reverse('add'))
	except:
		return redirect(reverse('signin'))





@login_required
def follower_stream(request):
	context = {}
	context['username'] = request.user
	profile = Profile.objects.get(owner=request.user)
	userList = []
	follower = profile.follow.all()
	profileFollow = []
	for each in follower:
		userList.append(each.owner)
	post = Post.objects.filter(user__in=userList).order_by('date')
	user=[]
	userObject=[]
	comment = []
	for postcontent in post:
		user.append(User.objects.all().filter(id=postcontent.user_id).first().username)
		userObject.append(User.objects.all().filter(id=postcontent.user_id).first())
		profileFollow.append(Profile.objects.all().get(owner_id=postcontent.user_id))
		commentContent = Comment.objects.all().filter(owner=postcontent).order_by('date')
		sub = []
		for each in commentContent:
			sub.append(each)
		comment.append(sub)

	result = [(post[i], userObject[i], profileFollow[i], comment[i]) for i in range(len(post))]
	context['result'] = result
	return render(request, 'grumblr/follower_stream.html', context)




@login_required
def add_profile(request):
	if request.method == "GET":
		context = {'form': ProfileForm()}
		return render(request, 'grumblr/add.html', context)

	new_profile = Profile(owner=request.user)
	form = ProfileForm(request.POST, request.FILES, instance=new_profile)
	if not form.is_valid():
		context = {'form': form}
		return render(request, 'grumblr/add.html', context)

	form.save()
	return redirect(reverse('global'))

@login_required
def edit_profile(request, id):
	profile_to_edit = get_object_or_404(Profile, owner=request.user, id=id)
	#user_to_edit = get_object_or_404(User, id=request.user.id)

	if request.method == 'GET':
		form1 = ProfileForm(instance=profile_to_edit)
		context = {'form1': form1, 'id': id}
		return render(request, 'grumblr/edit.html', context)

	form1 = ProfileForm(request.POST, request.FILES, instance=profile_to_edit)

	if not form1.is_valid():
		context = {'form1': form1, 'id': id}
		return render(request, 'grumblr/edit.html', context)

	form1.save()
	return redirect(reverse('myProfile'))

@login_required
def add_post(request):

	if request.method == 'POST':
	# if not 'post' in request.POST or not request.POST['post']:
	# 	raise Http404
	# else:
		new_post = Post(text=request.POST['post'], user=request.user)
		new_post.save()
	return HttpResponse("")

@login_required
def edit_password(request, id):
	profile_to_edit = get_object_or_404(Profile, owner=request.user, id=id)
	#user_to_edit = get_object_or_404(User, id=request.user.id)

	if request.method == 'GET':
		form2 = PasswordChangeForm(user=request.user)
		context = {'form2': form2, 'id': id}
		return render(request, 'grumblr/edit.html', context)

	form2 = PasswordChangeForm(user=request.user, data=request.POST)

	if not form2.is_valid():
		context = {'form2': form2, 'id': id}
		return render(request, 'grumblr/edit.html', context)

	form2.save()
	update_session_auth_hash(request, form2.user)
	return redirect(reverse('myProfile'))

def get_posts(request, time="1970-01-01T00:00+00:00"):
	max_time = Post.get_max_time()
	posts = Post.get_posts(time)
	comments = []
	for each in posts:
		comment = Comment.objects.filter(owner=each.id)
		comments.append(comment)
	context = {"max_time":max_time, "posts":posts, "comments": comments}
	return render(request, 'posts.json', context, content_type='application/json')

def get_follower_posts(request, time="1970-01-01T00:00+00:00"):
	context = {}
	max_time = Post.get_max_time()
	# context['username'] = request.user
	profile = Profile.objects.get(owner=request.user)
	userList = []
	follower = profile.follow.all()
	# profileFollow = []
	for each in follower:
		userList.append(each.owner)
	posts = Post.objects.filter(user__in=userList).order_by('date')
	# posts = Post.get_posts(time)
	comments = []
	for each in posts:
		comment = Comment.objects.filter(owner=each.id)
		comments.append(comment)
	context = {"max_time":max_time, "posts":posts, "comments": comments}
	return render(request, 'posts.json', context, content_type='application/json')

def get_myprofile_posts(request, time="1970-01-01T00:00+00:00"):
	context = {}
	max_time = Post.get_max_time()
	# context['username'] = request.user
	profile = Profile.objects.get(owner=request.user)

	# profileFollow = []

	posts = Post.objects.filter(user=request.user).order_by('date')
	# posts = Post.get_posts(time)
	comments = []
	for each in posts:
		comment = Comment.objects.filter(owner=each.id)
		comments.append(comment)
	context = {"max_time":max_time, "posts":posts, "comments": comments}
	return render(request, 'posts.json', context, content_type='application/json')

def get_profile_posts(request, time="1970-01-01T00:00+00:00"):
	if not 'id' in request.POST or not request.POST['id']:
		raise Http404
	else:
		context = {}
		id = request.POST['id']
		max_time = Post.get_max_time()
		# context['username'] = request.user
		profile = Profile.objects.get(owner=id)

		# profileFollow = []

		posts = Post.objects.filter(user=id).order_by('date')
		# posts = Post.get_posts(time)
		comments = []
		for each in posts:
			comment = Comment.objects.filter(owner=each.id)
			comments.append(comment)
		context = {"max_time":max_time, "posts":posts, "comments": comments}
	return render(request, 'posts.json', context, content_type='application/json')

def get_changes(request, time="1970-01-01T00:00+00:00"):
	max_time = Post.get_max_time()
	posts = Post.get_changes(time)
	comments = []
	for each in posts:
		comment = Comment.objects.filter(owner=each.id)
		comments.append(comment)
	context = {"max_time":max_time, "posts":posts, "comments": comments}
	return render(request, 'posts.json', context, content_type='application/json')

def add_comment(request):
	# context = {}
	# # errors = []
	# # context['errors'] = errors
	# context['username'] = request.user
	if not 'comment' in request.POST or not request.POST['comment'] or not 'post' in request.POST or not request.POST['post']:
		raise Http404
		# errors.append('You must enter something to comment.')
	else:
		post = Post.objects.get(id=request.POST['post'])
		profile = Profile.objects.get(owner=request.user.id)
		new_comment = Comment(text=request.POST['comment'], user=profile, owner=post)
		new_comment.save()
	list = []
	list.append(new_comment)
	context = {"comment_list": list}
	return render(request, 'comment_list.json', context, content_type='application/json')


