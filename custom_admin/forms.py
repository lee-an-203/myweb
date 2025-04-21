from django import forms
from myshop.models import Brand, Category, Detail, Order, OrderDetail, Promotion, Rating, Product
from django.contrib.auth.models import User

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'country', 'icon', 'category']
        widgets = {
            'category': forms.CheckboxSelectMultiple(),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'icon', 'category_parent']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'brand', 'price', 'stock_quantity', 'detail', 'image', 'status', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

class DetailForm(forms.ModelForm):
    class Meta:
        model = Detail
        fields = [
            'name', 'screen', 'operating_system', 'rear_camera', 'front_camera',
            'chip', 'RAM', 'memory', 'sim', 'battery', 'adapter'
        ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'create_date', 'total_amount', 'phone', 'address', 'status']

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetail
        fields = ['order', 'product', 'quantity', 'amount']

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['product', 'discount', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['product', 'user', 'stars']

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        
        # Prepopulate the user field with the logged-in user, making it readonly
        if 'user' not in self.initial:
            self.initial['user'] = User.objects.first()  # Assuming you're pre-assigning the user
        self.fields['user'].widget.attrs['readonly'] = True

        # Optional: You can add a custom queryset for 'product' field, if needed
        self.fields['product'].queryset = Product.objects.all()





