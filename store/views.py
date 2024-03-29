from email import message
from django.shortcuts import get_object_or_404, render, redirect
from category.models import Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q, Manager
from django.contrib import messages
from .models import Product, ProductGallery, AccountFavorite, AccountPrice
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .services import build_variant_structure


def store(request, category_slug=None):
    categories = None
    products = None
    product_by_page = 9

    # Si mostramos los Favoritos
    if (request.get_full_path() == '/store/favorites/'):
        current_user = request.user
        # Buscamos los productos favoritos para este usuario
        favorites_products = AccountFavorite.objects.filter(
            account=current_user)
        id_list = favorites_products.values_list('product', flat=True)

        #  PENDIENTE
        products = Product.objects.filter(
            is_available=True, id__in=id_list, parent=0).order_by(
            '-create_date')

        # Paginamos
        paginator = Paginator(products, product_by_page)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        if category_slug is not None:
            categories = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(
                category=categories, is_available=True, parent=0).order_by(
                '-create_date')
            paginator = Paginator(products, product_by_page)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()
        else:
            products = Product.objects.all().filter(
                is_available=True, parent=0).order_by('-create_date')
            paginator = Paginator(products, product_by_page)
            page = request.GET.get('page')
            paged_products = paginator.get_page(page)
            product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count
    }

    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    current_user = request.user

    single_product = Product.objects.filter(
        category__slug=category_slug,
        slug=product_slug
    )

    if single_product:
        single_product = single_product.first()

    product_gallery = ProductGallery.objects.filter(
        product_id=single_product.id
    )

    if request.user.is_anonymous:
        favorites_product_count = 0
    else:
        favorites_product_count = AccountFavorite.objects.filter(
            account=current_user,
            product=single_product.id
        ).count

    price = single_product.price

    if not current_user.is_anonymous:
        account_price = AccountPrice.objects.filter(
            product=single_product.id,
            account=current_user
        )
        if account_price:
            price = account_price.listprice

    if single_product.is_parent:
        variants_structure = build_variant_structure(single_product)

    context = {
        'single_product': single_product,
        'price': price,
        'product_gallery': product_gallery,
        'favorites_product_count': favorites_product_count,
    }

    return render(request, 'store/product_detail.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-create_date').filter(
                Q(description__icontains=keyword) | Q(
                    product_name__icontains=keyword))
            product_count = products.count()

        context = {
            'products': products,
            'product_count': product_count
        }

        return render(request, 'store/store.html', context)


@login_required
def add_favorites(request, id):
    is_fav_count = AccountFavorite.objects.filter(product=id).count()

    if is_fav_count <= 0:
        product = Product.objects.get(id=id)
        current_user = request.user
        account_favorite = AccountFavorite()
        account_favorite.account = current_user
        account_favorite.product = product
        account_favorite.save()
    else:
        pass

    return redirect('favorites_products')


@login_required
def delete_favorites(request, id):
    current_user = request.user
    favorite = AccountFavorite.objects.filter(product=id, account=current_user)
    if favorite.count() >= 0:
        favorite.delete()
    return redirect('favorites_products')
