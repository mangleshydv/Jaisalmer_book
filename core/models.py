from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey



class HomeSection(models.Model):
    short_heading = models.CharField(max_length=200, help_text="छोटी heading")
    highlight_text = models.CharField(max_length=100, help_text="heading में span वाला text")
    description = models.TextField(help_text="Paragraph text")
    heading_image = models.ImageField(upload_to='home/', help_text="PNG image for heading")

    def __str__(self):
        return self.short_heading



# top TopPalace

class TopPalace(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    short_description = models.TextField()
    image = models.ImageField(upload_to='palaces/')

    class Meta:
        verbose_name = "Top Palace"
        verbose_name_plural = "Top Palaces"

    def __str__(self):
        return self.name





# about content 
class AboutSection(models.Model):
    description = models.TextField()

    branches_count = models.CharField(max_length=50, default="20+")
    branches_text = models.CharField(max_length=100, default="Global Branches")

    destinations_count = models.CharField(max_length=50, default="15+")
    destinations_text = models.CharField(max_length=100, default="Destinations Covered")

    customers_count = models.CharField(max_length=50, default="50K+")
    customers_text = models.CharField(max_length=100, default="Happy Customers")


    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"About Section - {self.description}"



# why choose us content 

class WhyChooseSection(models.Model):
    heading = models.CharField(max_length=255)
    short_content = models.TextField()

    couple_image = models.ImageField(upload_to='whychoose/', help_text="Upload Couple Image")
    tree_image1 = models.ImageField(upload_to='whychoose/', help_text="Upload First Tree Image")
    tree_image2 = models.ImageField(upload_to='whychoose/', help_text="Upload Second Tree Image")

    class Meta:
        verbose_name = "Why Choose Us Section"
        verbose_name_plural = "Why Choose Us Sections"

    def __str__(self):
        return self.heading




# jaisalmer top destination
class Destination(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='destinations/')
    description = models.TextField()
    distance_from_jaisalmer = models.DecimalField(
        max_digits=6, decimal_places=2,
        help_text="Distance from Jaisalmer in km"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"
        ordering = ['distance_from_jaisalmer']

    def __str__(self):
        return self.name





# reviwe

class Review(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    description = models.TextField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"Review by {self.name}"
    



# contact
class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    agreed_to_terms = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"
        ordering = ['-submission_date']
    
    def __str__(self):
        return f"{self.name} - {self.submission_date.strftime('%Y-%m-%d %H:%M')}"