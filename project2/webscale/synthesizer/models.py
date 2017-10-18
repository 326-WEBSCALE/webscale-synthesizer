from django.db import models
from django.urls import reverse
import uuid

# Create your models here.
class ApplicationTable(models.Model):
    """
    Model of a tabel for applications
    """
    client_secret = models.CharField(max_length=200, help_text="Enter client secret")

    contact_email = models.EmailField(max_length=200, help_text="Enter your email")

    copyright_date = models.CharField(max_length=200, help_text="Enter copyright date")

    def get_client_secret(self):
        """
        Returns the client_secret
        """
        return self.client_secret

    def get_contact_email(self):
        """
        Returns the contact_email
        """
        return self.contact_email

    def get_copyright_date(self):
        """
        Returns the copyright date
        """
        return self.copyright_date

class User(models.Model):
    """
    Model representing a user.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular user")
    name = models.CharField('Name', max_length=200, help_text="Enter your name")
    email = models.EmailField('email', max_length=200, help_text= "Enter you email")
    hashed_password = models.CharField(max_length=200)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    def get_id(self):
        """
        Returns the user's unique id
        """
        return self.id

    def get_name(self):
        """
        Returns the user's name
        """
        return self.name

    def get_email(self):
        """
        Returns the user's email
        """
        return self.email

    def get_hashed_password(self):
        """
        Returns the hashed password
        """
        return self.hashed_password

class Snippit(models.Model):
    """
    Model for representing a Snippit
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this Snippit")
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    name = models.CharField('Name', max_length=200, help_text="Enter name")
    description = models.TextField(max_length=1000, help_text="Enter the snippit description")
    program_text = models.TextField(max_length=99999, help_text="Enter the program text")
    """
    The synthesizer result needs to be a different kind of model field that will be generated, not entered
    """
    synthesizer_result = models.TextField(max_length=99999, help_text="Enter the synthesizer result")
    is_public = (
        ('t', 'True'),
        ('f', 'False'),
    )

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

    def get_id(self):
        """
        Returns the id
        """
        return self.id
    def get_user_id(self):
        """
        Returns the user's unique id
        """
        return self.user_id

    def get_name(self):
        """
        Returns the Snippit's name
        """
        return self.name

    def get_description(self):
        """
        Returns the Snippit's description
        """
        return self.description

    def get_program_text(self):
        """
        Returns the Snippit's program text
        """
        return self.program_text
    def get_synthesizer_result(self):
        """
        Returns the Snippit's synthesizer result
        """
        return self.synthesizer_result
    def get_is_public(self):
        """
        Returns the Snippit's is_public value
        """
        return self.is_public

class SnippitData(models.Model):
    """
    Model for Snippit Data
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this Snippit Data")
    snippit_id = models.ForeignKey('Snippit', on_delete=models.SET_NULL, null=True)
    synthesizer_time = models.CharField(max_length=200, help_text="Enter time")
    holes_count = models.CharField(max_length=200, help_text="Enter number of holes")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.id
    def get_id(self):
        """
        Returns the snippit data's unique id
        """
        return self.id
    def get_snippit_id(self):
        """
        Returns the Snippit's unique id
        """
        return self.snippit_id
    def get_synthesizer_time(self):
        """
        Returns the synthesizer's time
        """
        return self.synthesizer_time
    def get_holes_count(self):
        """
        Returns the amount of holes
        """
        return self.holes_count

class HolzTable(models.Model):
    """
    Model for HolzTable
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this Holz Table")
    snippit_id = models.ForeignKey('Snippit', on_delete=models.SET_NULL, null=True)
    hole = models.CharField(max_length=200, help_text="Enter hole")
    constant = models.CharField(max_length=200, help_text="Enter constant")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.id
    def get_id(self):
        """
        Returns the Holz Table's unique id
        """
        return self.id
    def get_snippit_id(self):
        """
        Returns the Snippit's unique id
        """
        return self.snippit_id
    def get_hole(self):
        """
        Returns the Holz Table hole
        """
        return self.hole
    def get_constant(self):
        """
        Returns the Holz Table constant
        """
        return self.constant

class GoogleAuth(models.Model):
    """
    Model for Google Authentication
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this Google Authentication")
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    is_authenticated = (
        ('t', 'True'),
        ('f', 'False'),
    )
    access_token = models.CharField(max_length=200, help_text="Enter access_token")
    refresh_token = models.CharField(max_length=200, help_text="Enter refresh_token")

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.id
    def get_id(self):
        """
        Returns the GoogleAuth's unique id
        """
        return self.id
    def get_user_id(self):
        """
        Returns the user's unique id
        """
        return self.user_id
    def get_is_authenticated(self):
        """
        Returns is_authenticated
        """
        return self.is_authenticated
    def get_access_token(self):
        """
        Returns access_token
        """
        return self.access_token
    def get_refresh_token(self):
        """
        Returns refresh_token
        """
        return self.refresh_token

class Comment(models.Model):
    """
    Model for comments
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this comment")
    user_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    snippit_id = models.ForeignKey('Snippit', on_delete=models.SET_NULL, null=True)
    text = models.TextField(max_length=99999, help_text="Enter the comment text")
    date_posted = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.id
    def get_id(self):
        """
        Returns the comment's unique id
        """
        return self.id
    def get_user_id(self):
        """
        Returns the user's unique id
        """
        return self.user_id
    def get_snippit_id(self):
        """
        Returns the Snippit's unique id
        """
        return self.snippit_id
    def get_text(self):
        """
        Returns the comment's text
        """
        return self.text
    def get_date(self):
        """
        Returns date_posted
        """
        return self.date_posted
