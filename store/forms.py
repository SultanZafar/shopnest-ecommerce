from django import forms
from .models import Review, Order


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.Select(attrs={
                "class": "w-full rounded-lg border border-stone-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-700"
            }),
            "comment": forms.Textarea(attrs={
                "rows": 3,
                "placeholder": "Share your experience with this product...",
                "class": "w-full rounded-lg border border-stone-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-700"
            }),
        }


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "address", "city", "payment_method"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "input-field", "placeholder": "Full name"}),
            "phone": forms.TextInput(attrs={"class": "input-field", "placeholder": "03xx-xxxxxxx"}),
            "address": forms.Textarea(attrs={"class": "input-field", "rows": 3, "placeholder": "House #, street, area"}),
            "city": forms.TextInput(attrs={"class": "input-field", "placeholder": "City"}),
            "payment_method": forms.Select(attrs={"class": "input-field"}),
        }
