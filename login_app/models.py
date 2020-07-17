from django.db import models
import re 
import bcrypt
#regex import

#Pass in a pattern that email must match from the imported re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #regex email format

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # Figure pout how to validate first and last name to have no numbers
        # nonum = str.isalpha() 
        if len(postData['first_name'])< 2:
            errors['first_name'] = "First Name is Required."
        if len(postData['last_name'])< 2:
            errors['last_name'] = "Last Name is Required."
        # if len(postData['email'])< 1:
        #     errors['email'] = "Email is required."
        if not EMAIL_REGEX.match(postData['email']):    # test whether a field matches the pattern            
            errors['email'] = "Invalid email address!"
        if len(postData['password'])< 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm']: #Check to make sure password and confirm are equal
            errors['confirm'] = "Passwords do not match."
        #prevent Duplicate emails
        users_with_email = self.filter(email=postData['email'])
        if users_with_email:
            errors['email'] = "Email is already in use."
        return errors
    
    #place creation in models instead so views stays minimal
    def register(self, postData):
        hashed_password = bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hashed_password
        )
    
    def authenticate(self, email, password):
        #return true/false
        users_with_email = self.filter(email=email)
        if not users_with_email:
            return False
        user = users_with_email[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())




class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)

    objects = UserManager()

class MessagePost(models.Model):
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name="messages_likes")
    update_on = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, related_name="messages", on_delete = models.CASCADE)


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    update_on = models.DateTimeField(auto_now=True)
    message_id = models.ForeignKey(MessagePost, related_name="comments", on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, related_name="comments", on_delete = models.CASCADE)
