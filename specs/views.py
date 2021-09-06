from django.contrib import messages
from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect, JsonResponse
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


class FeatureChoiceView(View):

    def get(self, request, *args, **kwargs):
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class ="form-select" name="feature-validators" id="feature-validators-id" aria-label="Default select example">
            <option selected>---</option>
            {result}
            </select>
                    """
        feature_key_qs = CategoryFeature.objects.filter(
            category_id=int(request.GET.get('category_id'))
        )
        res_string =""
        for item in feature_key_qs:
            res_string += option.format(value=item.feature_name, option_name=item.feature_name)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"result": html_select, "value": int(request.GET.get('category_id'))})


class CreateFeatureView(View):

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        feature_name = request.GET.get('feature_name')
        value = request.GET.get('feature_value').strip(" ")
        print(value)
        category = Category.objects.get(id=int(category_id))
        feature = CategoryFeature.objects.get(category=category, feature_name=feature_name)
        existed_object, created = FeatureValidator.objects.get_or_create(
            category=category,
            feature_key=feature,
            valid_feature_value=value
        )
        if not created:
            return JsonResponse({
                "error": f"Значение '{value}' уже существует."
            })
        messages.add_message(
            request, messages.SUCCESS,
            f'Значение "{value}" для характеристики '
            f'"{feature.feature_name}" в категории {category.name} успешно создано'
        )
        return JsonResponse({'result': 'ok'})


class NewProductFeatureView(View):

    def get(self, requst, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(requst, 'new_product_feature.html', context)


class SearchProductAjaxView(View):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        category_id = request.GET.get('category_id')
        category = Category.objects.get(id=int(category_id))
        product = list(Product.objects.filter(
            category=category,
            title__icontains=query
        ).value())
        return JsonResponse({'result': product})


class AttachNewFeatureToProduct(View):

    def get(self, request, *args, **kwargs):
        res_string = ""
        product = Product.objects.get(id=int(request.GET.get('product_id')))
        existing_features = list(set([item.feature.feature_name for item in product.features.all()]))
        print(existing_features)
        category_features = CategoryFeature.objcets.filter(
            category=product.category
        ).exclude(feature_name__in=existing_features)
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class="form-select" name="product-category-features" id="product-category-features-id" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        for item in category_features:
            res_string +=option.format(value=item.category.id, option_name=item.feature_name)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"features": html_select})


class ProductFeatureChoicesAjaxView(View):

    def get(self, request, *args, **kwargs):
        res_string = ""
        category = Category.objects.get(id=int(request.GET.get('category_id')))
        feature_key = CategoryFeature.objects.get(
            category = category,
            feature_name = request.GET.get('product_feature_name')
        )
        validators_qs = FeatureValidator.objects.filter(
            category=category,
            feature_key=feature_key
        )
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
                    <select class="form-select" name="product-category-features-choices" id="product-category-features-choices-id" aria-label="Default select example">
                        <option selected>---</option>
                        {result}
                    </select>
                            """
        for item in validators_qs:
            res_string += option.format(value=item.id, option_name=item.valid_feature_value)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"features": html_select})


class CreatedNewProductFeatureAjaxView(View):

    pass