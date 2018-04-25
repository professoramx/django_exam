# general imports
from __future__ import unicode_literals
from django.db import models

# for handling password
import bcrypt

# for handling date/time fields
from datetime import date, datetime
from time import strptime

# custom model manager for users
class UserManager(models.Manager):
    # user validation method (when registering user)
    def validate(self, postData):
        # run through validation checks
        errors = []
        if len(postData['name']) == 0:
            errors.append("Could not register user: Empty Name not allowed.")
        if len(postData['username']) < 3:
            errors.append("Could not register user: Username should be at least 3 characters.")
        if len(User.objects.filter(username = postData['username'])) > 0:
            errors.append("Could not register user: Username already exists.")
        if len(postData["password"]) < 8:
            errors.append("Could not register user: Password should be at least 8 characters.")
        if postData["password"] != postData["confirm-password"]:
            errors.append("Could not register user: Passwords don't match.")
        # create and return user if no errors are found, otherwise return error(s)
        if len(errors) == 0:
            newuser = User.objects.create(
                name = postData['name'], 
                username = postData['username'], 
                password = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()),
                date_of_birth = postData['date-of-birth']
                )
            return (True, newuser)
        else:
            return (False, errors)
    # user validation method (when logging in)
    def login(self, postData):
        # run through validation checks (if user exists and password is correct)
        errors = []
        if 'username' in postData and 'password' in postData:
            try:
                user = User.objects.get(username = postData['username'])
            except: 
                errors.append("Could not log in: User not found.")
                return (False, errors)
        pw_match = bcrypt.checkpw(postData['password'].encode(), user.password.encode())
        # return user if user is found and password is correct, otherwise return error(s)
        if pw_match == True:
            return [True, user]
        else:
            errors.append("Could not log in: Password is incorrect.")
            return [False, errors]

# model for storing users
class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_of_birth = models.DateField(default = date.today)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    # override model manager for custom validation
    objects = UserManager()

# custom model manager for quotes
class QuoteManager(models.Manager):
    # quote validation method (when contributing quotes)
    def validate(self, postData, id):
        # run through validation checks
        errors = []
        if len(postData['quoted-by']) == 0:
            errors.append("Could not post quote: Empty entry for Quoted By not allowed.")
        elif len(postData['quoted-by']) < 3:
            errors.append("Could not post quote: Quoted By should be at least 3 characters.")
        if len(postData['message']) == 0:
            errors.append("Could not post quote: Empty entry for Message not allowed.")
        elif len(postData['message']) < 10:
            errors.append("Could not post quote: Message should be at least 10 characters.")
        # create and return quote if no errors are found, otherwise return error(s)
        if len(errors) == 0:
            quote = Quote.objects.create(
                message=postData['message'], 
                quoted_by=postData['quoted-by'], 
                posted_by = User.objects.get(id=id)
                )
            return (True, quote)
        else:
            return (False, errors)

# model for storing quotes
class Quote(models.Model):
    message = models.TextField()
    quoted_by = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, related_name="posted_quotes")
    users = models.ManyToManyField(User, related_name="favorite_quotes")
    date_added = models.DateTimeField(auto_now_add = True)
    # override model manager for custom validation
    objects = QuoteManager()