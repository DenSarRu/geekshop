from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import connection
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.views.generic import DetailView

from adminapp.forms import ShopUserAdminEditForm, ProductCategoryEditForm, ProductCategoryCreationForm, ProductEditForm
from authapp.forms import ShopUserRegisterForm
from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory

from django.views.generic.list import ListView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


class UsersListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    login_url = '/'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UsersListView, self).get_context_data()
        context['title'] = 'админка/пользователи'
        return context

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')


class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    form_class = ShopUserRegisterForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data()
        context['title'] = 'пользователь/создание'
        return context


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    form_class = ShopUserAdminEditForm
    template_name = 'adminapp/user_update.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        context['title'] = 'пользователь/редактирование'
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = ShopUser
    template_name = 'adminapp/user_delete.html'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserDeleteView, self).get_context_data()
        context['title'] = 'пользователь/редактирование'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class UserDetailView(DetailView):
    model = ShopUser
    template_name = 'adminapp/user_read.html'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data()
        context['title'] = 'информация о пользователе'
        return context


class CategoryListView(LoginRequiredMixin, ListView):
    model = ProductCategory
    template_name = 'adminapp/categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data()
        context['title'] = 'админка/категории'
        return context

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('-is_active', 'name')


def category_create(request):
    title = 'категория/создание'

    if request.method == 'POST':
        category_form = ProductCategoryCreationForm(request.POST)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        category_form = ProductCategoryCreationForm()

    context = {
        'title': title,
        'category_form': category_form
    }
    return render(request, 'adminapp/category_update.html', context)


def category_update(request, pk):
    title = 'категория/редактирование'
    edit_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        edit_form = ProductCategoryEditForm(request.POST, instance=edit_category)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        edit_form = ProductCategoryEditForm(instance=edit_category)

    context = {
        'title': title,
        'category_form': edit_form,
    }
    return render(request, 'adminapp/category_update.html', context)


def category_delete(request, pk):
    title = 'категория/удаление'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        category.is_active = False
        category.save()
        return HttpResponseRedirect(reverse('admin_staff:categories'))

    context = {
        'title': title,
        'category_to_delete': category
    }
    return render(request, 'adminapp/category_delete.html', context)


def products(request, pk=None, page=1):
    title = 'админка/товары'

    if pk is None or pk == 0:
        products_list = Product.objects.all().order_by('price').select_related()
        category = {'pk': 0, 'name': 'Все'}
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products_list = Product.objects.filter(category__pk=pk).order_by('name').select_related()

    paginator = Paginator(products_list, 5)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': title,
        'category': category,
        'products': products_paginator,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    title = 'товар/создание'

    if pk == 0:
        category = {'pk': 0, 'name': 'Все'}

        if request.method == 'POST':
            product_form = ProductEditForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
        else:
            product_form = ProductEditForm()
    else:
        category = get_object_or_404(ProductCategory, pk=pk)

        if request.method == 'POST':
            product_form = ProductEditForm(request.POST, request.FILES)
            if product_form.is_valid():
                product_form.save()
                return HttpResponseRedirect(reverse('admin_staff:products', args=[pk]))
        else:
            product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'product_form': product_form,
        'category': category,
    }
    return render(request, 'adminapp/product_update.html', context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        context['title'] = 'товар/подробнее'
        return context


def product_update(request, pk):
    title = 'товар/редактирование'
    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('admin_staff:product_read', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'product_form': edit_form,
    }
    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    title = 'товар/удаление'
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.is_active = False
        product.save()
        return HttpResponseRedirect(reverse('admin_staff:products', args=[product.category.pk]))

    context = {
        'title': title,
        'product_to_delete': product
    }

    return render(request, 'adminapp/product_delete.html', context)


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}: ')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_on_productcategorysave(sender, instance, **kwargs):
    if instance.pk:
        instance.product_set.update(is_active=instance.is_active)

        db_profile_by_type(sender, 'UPDATE', connection.queries)

# class ProductListView(ListView):
#     model = Product
#     template_name = 'adminapp/products.html'
#     paginate_by = 5
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(ProductListView, self).get_context_data()
#         context['title'] = 'админка/категории'
#         print(context['page_obj'])
#         return context
#
#     def get_queryset(self):
#         pk = self.kwargs['pk']
#         if pk is None or pk == 0:
#             products_list = Product.objects.all().order_by('price')
#             self.kwargs['page'] = 1
#             category = {'pk': 0, 'name': 'Все'}
#         else:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             products_list = Product.objects.filter(category__pk=pk).order_by('name')
#             self.kwargs['page'] = 1
#         return products_list


# @user_passes_test(lambda u: u.is_superuser)
# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#
#     context = {
#         'title': title,
#         'objects': users_list
#     }
#
#     return render(request, 'adminapp/users.html', context)


# def user_update(request, pk):
#     title = 'пользователь/редактирование'
#     edit_user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         edit_form = ShopUserAdminEditForm(request.POST, request.FILES, instance=edit_user)
#         if edit_form.is_valid():
#             edit_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         edit_form = ShopUserAdminEditForm(instance=edit_user)
#
#     context = {
#         'title': title,
#         'user_form': edit_form,
#     }
#     return render(request, 'adminapp/user_update.html', context)

# def user_delete(request, pk):
#     title = 'пользователь/удаление'
#     user = get_object_or_404(ShopUser, pk=pk)
#
#     if request.method == 'POST':
#         # user.delete() # вместо удаления лучше сделаем неактивным
#         user.is_active = False
#         user.save()
#         return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     context = {
#         'title': title,
#         'user_to_delete': user
#     }
#     return render(request, 'adminapp/user_delete.html', context)


# def categories(request):
#     title = 'админка/категории'
#     categories_list = ProductCategory.objects.all().order_by('-is_active', 'name')
#
#     context = {
#         'title': title,
#         'objects': categories_list
#     }
#
#     return render(request, 'adminapp/categories.html', context)

# def user_create(request):
#     title = 'пользователь/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'user_form': user_form
#     }
#     return render(request, 'adminapp/user_update.html', context)


# def product_read(request, pk):
#     title = 'товар/подробнее'
#
#     product = get_object_or_404(Product, pk=pk)
#     context = {
#         'title': title,
#         'object': product,
#     }
#
#     return render(request, 'adminapp/product_read.html', context)
