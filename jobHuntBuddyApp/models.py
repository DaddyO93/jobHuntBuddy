from __future__ import unicode_literals
from django.db import models
from django.db.models.deletion import CASCADE
import re


# Create your models here.
class UserManager (models.Manager):
    def loginValidator(self, dataPost):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-z!-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(dataPost['user_first_name'])<2:
            errors['user_first_name'] = "First name must be longer than 2 characters"
        if len(dataPost['user_last_name'])<2:
            errors['user_last_name'] = "Last name must be longer than 2 characters"
        if len(dataPost['user_password'])<8:
            errors['user_password'] = "Password must be at least 8 characters. HINT: Use a phrase or sentence."
        # Ensure valid email address
        if not EMAIL_REGEX.match(dataPost['user_email']):
            errors['user_email'] = "You must use a valid email address"
        # Validate unique email address
        user = User.objects.filter(email=dataPost['user_email'])
        if len(user)>0:
            errors['user_email'] = "That email address is already taken"
        # Confirm password and pw_confirm match
        if dataPost['user_password'] != dataPost['user_password_conf']:
            errors['user_password_conf'] = "Your passwords did not match"
        return errors
    
class PositionManager (models.Manager):
    def positionValidator(self, dataPost):
        errors = {}
        if len(dataPost['position_applied_for'])<4:
            errors['Position Entry'] = "Please enter the name of a position title longer than 4 characters"
        return errors
    
    def companyValidator(self, dataPost):
        errors = {}
        if len(dataPost['name'])<4:
            errors['Company Entry'] = "Please enter the name of a company longer than 4 characters"
        if len(dataPost['website'])<4:
            errors['Company Entry'] = "Please enter a valid company website"
        
    def contactPersonValidator(self, dataPost):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-z!-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # Ensure valid email address
        if not EMAIL_REGEX.match(dataPost['user_email']):
            errors['user_email'] = "You must enter a valid email address"
        if len(dataPost['contact_person'])<3:
            errors['Contact Entry'] = "Please enter a name longer than 3 characters"
        

class User (models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
      
class Company (models.Model):
    name = models.CharField(max_length=100)
    website = models.CharField(max_length=255)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    objects = PositionManager()
    # company foreign field from Position
    # company foreign field from ContactPerson
  
class Position (models.Model):
    user = models.ForeignKey(User, related_name="position", on_delete=CASCADE)
    date_applied = models.DateField(null=True)
    position_applied_for = models.CharField(max_length=50)
    company = models.ForeignKey(Company, related_name="position", on_delete=CASCADE)
    date_declined = models.DateField(null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PositionManager()
    # contact_person foreign field from ContactPerson
    # position foreign field from FollowUpDate

class ContactPerson (models.Model):
    contact_person = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=100, null=True)
    company = models.ForeignKey(Company, related_name="contact_person", on_delete=CASCADE)
    position = models.ForeignKey(Position, related_name="contact_person", on_delete=models.SET_NULL, null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # contact_person foreign field from FollowUpDate

class FollowUpDate (models.Model):
    date_heard_back = models.DateField(null=True)
    last_follow_up = models.DateField(null=True)
    position = models.ForeignKey(Position, related_name="follow_up_date", on_delete=CASCADE)
    contact_person = models.ForeignKey(ContactPerson, related_name="follow_up_date", on_delete=CASCADE)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

