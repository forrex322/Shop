from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.decorators import method_decorator


from .forms import NewCategoryForm, CategoryFeature, NewCategoryFeatureKeyForm
from .models import *
from mainapp.models import Category, Product

# Декоратор для проверки является ли пользователь залогиненым
# @method_decorator(login_required, name='dispatch')
# Декоратор для проверки является ли пользователь админом
@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'product_features.html', {})


class NewCategoryView(View):

    def get(self, request, *args, **kwargs  ):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/product-features/')
        return render(request, 'new_category.html', context)


class CreateNewFeature(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_feature.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        if form.is_valid():
            new_category_feature_key = form.save(commit=False)
            new_category_feature_key.category = form.cleaned_data['category']
            new_category_feature_key.feature_name = form.cleaned_data['feature_name']
            new_category_feature_key.save()
            return HttpResponseRedirect('/product-features/')
        context = {'form': form}
        return render(request, 'new_feature.html', context)


class CreateNewFeatureValidator(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_validator.html', context)