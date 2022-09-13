from tkinter import Widget
from django import forms
from .models import *

# Model form for a new listing
class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startingBid', 'image', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows':2, 'maxlength': 1000, 'class': 'form-control'}),
            'startingBid': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }
        labels = {
            'image': 'Image URL'
        }


# Model form for commenting on a particular listing
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'maxlength': '5000'})
        }


# Model form for inputting a Bid
class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'})
        }
