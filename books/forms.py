from django import forms
from .models import Review


class ReviewCreateForm(forms.ModelForm):
    stars_given = forms.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Review
        fields = ("review_text", "stars_given")
