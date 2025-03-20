from django import forms
from .models import Listing

# Form for creating a new listing
class ListingForm(forms.ModelForm):
    class Meta: 
        # Specify the model to use for the form
        model = Listing
        # Fields to include in the form
        fields = ['title', 'description', 'starting_bid', 'image', 'category','duration']
