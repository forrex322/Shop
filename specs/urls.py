from django.urls import path

from .views import (
    BaseSpecView,
    NewCategoryView,
    CreateNewFeature,
    CreateNewFeatureValidator,
    FeatureChoiceView,
    CreateFeatureView,
    NewProductFeatureView,
    SearchProductAjaxView,
    AttachNewFeatureToProduct,
    ProductFeatureChoicesAjaxView,
    CreatedNewProductFeatureAjaxView,
    UpdateProductFeaturesView,
    ShowProductFeaturesForUpdate,
    UpdateProductFeaturesAjaxView
)

urlpatterns = [
    path('', BaseSpecView.as_view(), name='base-spec'),
    path('new-category/', NewCategoryView.as_view(), name='new-category'),
    path('new-feature/', CreateNewFeature.as_view(), name='new-feature'),
    path('new-validator/', CreateNewFeatureValidator.as_view(), name='new-validator'),
    path('feature-choice/', FeatureChoiceView.as_view(), name='feature-choice-validators'),
    path('feature-create/', CreateFeatureView.as_view(), name='feature-create'),
    path('new-product-feature/', NewProductFeatureView.as_view(), name='new-product-feature'),
    path('search-product/', SearchProductAjaxView.as_view(), name='search-product'),
    path('attach-feature/', AttachNewFeatureToProduct.as_view(), name='attach-feature'),
    path('product-feature/', ProductFeatureChoicesAjaxView.as_view(), name='product-feature'),
    path('attach-new-product-feature/', CreatedNewProductFeatureAjaxView.as_view(), name='attach-new-product-feature'),
    path('update-product-features/', UpdateProductFeaturesView.as_view(), name='update-product-features'),
    path('show-product-features-for-update/', ShowProductFeaturesForUpdate.as_view(), name='show-product-features-for-update'),
    path('update-product-features-ajax/', UpdateProductFeaturesAjaxView.as_view(), name='update-product-features-ajax')
]

