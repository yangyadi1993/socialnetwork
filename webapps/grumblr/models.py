from django.db import models

from django.contrib.auth.models import User
from django.db.models import Max
from django.utils.html import escape

#class User(models.Model):
#	user_name = models.CharField(max_length=20)
#	user_password = models.CharField(max_length=20)

class Post(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	text = models.CharField(max_length=42)
	date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.text
	def __str__(self):
		return self.__unicode__()

	@staticmethod
	def get_changes(time="1970-01-01T00:00+00:00"):
		return Post.objects.filter(date__gt=time).distinct()

	@staticmethod
	def get_posts(time="1970-01-01T00:00+00:00"):
		return Post.objects.filter(date__gt=time).distinct()

	@property
	def html(self):
		return "<div class='col-md-3'><img class='img-thumbnail profile' src='%s'></div><h4><a href='profile/%s'> %s %s </a></h4><p id='post_%d'> %s</p><p id='time' class='lead'> %s </p><input id='comment_post_%d' value=''><button id='add-comment'>Comment</button>" % (self.user.profile.picture.url, self.user.id, escape(self.user.profile.first_name), escape(self.user.profile.last_name), self.id, escape(self.text), self.date, self.id)

	# @property
	# def userhtml(self):
	# 	return "<p id='post_%d'> %s</p>" % (self.id, escape(self.user.username))

	@staticmethod
	def get_max_time():
		return Post.objects.all().aggregate(Max('date'))['date__max'] or "1970-01-01T00:00+00:00"

class Profile(models.Model):
	# owner = models.ForeignKey(User)
	owner = models.OneToOneField(User)
	follow = models.ManyToManyField('self', related_name='profile', blank=True, default="")
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	age = models.IntegerField()
	bio = models.CharField(max_length=420)
	picture = models.ImageField(upload_to="grumblr-photos")

	def __unicode__(self):
		return self.first_name + " " + self.last_name
	def __str__(self):
		return self.first_name + " " + self.last_name

	@staticmethod
	def get_profile(owner):
		return Profile.objects.filter(owner=owner).order_by('last_name', 'first_name')

class Comment(models.Model):
	owner = models.ForeignKey(Post, default="")
	user = models.ForeignKey(Profile, default="")
	text = models.CharField(max_length=420)
	date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.text
	def __str__(self):
		return self.__unicode__()
	@property
	def html(self):
		return "<div class='col-md-2' id='commentTotal'><img class='img-thumbnail profile' src='%s'></div><h5><a> %s </a></h5><h4><p id='comment_%d'> %s</p><h4><p id='time' class='lead'> %s </p>" % (self.user.picture.url, escape(self.user.first_name), self.id, escape(self.text), self.date)


