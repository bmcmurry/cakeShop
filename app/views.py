from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .filters import OrderFilter
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group


@unauthenticated_user
def RegisterPage(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name="customer")
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

            messages.success(request, "Account was created for " + username)
            return redirect("login")

    context = {"form": form}
    return render(request, "register.html", context)


@unauthenticated_user
def LoginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username OR Password is Incorrect")

    context = {}
    return render(request, "login.html", context)


def LogoutUser(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
@admin_only
def Home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "customers": customers,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
    }

    return render(request, "dashboard.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def UserPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status="Delivered").count()
    pending = orders.filter(status="Pending").count()

    context = {
        "orders": orders,
        "total_orders": total_orders,
        "delivered": delivered,
        "pending": pending,
    }
    return render(request, "user.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["customer"])
def AccountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, "account_settings.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def ProductsPage(request):
    products = Product.objects.all()
    form = ProductForm()
    context = {}
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    context = {"products": products, "form": form}
    return render(request, "products.html", context)


@login_required(login_url="login")
# @customer_login_required
@user_is_customer
# @allowed_users(allowed_roles=["admin"])
def CustomerPage(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all() # type: ignore
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        "customer": customer,
        "orders": orders,
        "order_count": order_count,
        "myFilter": myFilter,
    }
    return render(request, "customer.html", context)


@login_required(login_url="login")
@allowed_users(allowed_roles=["admin"])
def CreateCustomer(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            group = Group.objects.get(name="customer")
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.username,
                email=user.email,
            )

            messages.success(request, "Account was created for " + username)
            return redirect("home")

    context = {"form": form}
    return render(request, "create_customer.html", context)


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def CreateOrder(request, pk):
    OrderFormSet = inlineformset_factory(
        Customer, Order, fields=("product", "status"), extra=6
    )
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == "POST":
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect("/")
        else:
            print(formset.errors)

    context = {"formset": formset}
    return render(request, "order_form.html", context)


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def UpdateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {"form": form}
    return render(request, "order_form.html", context)


@login_required(login_url="login")
# @allowed_users(allowed_roles=["admin"])
def DeleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect("/")

    context = {"item": order}
    return render(request, "delete.html", context)


def StoreFront(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, "store_front.html", context)
