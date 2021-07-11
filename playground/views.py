from datetime import datetime
from typing import Annotated
from django.db.models import aggregates
from django.db.models.expressions import ExpressionWrapper, Value
from django.db.models.fields import DecimalField
from tags.models import Tag
from django.shortcuts import render
from django.db.models import F, Q
from django.db.models.aggregates import Count, Min, Sum, Avg, Max
from store.models import Address, Cart, CartItem, Order, OrderItem, Product, Customer, Collection



def say_hello(request):

    #query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    #lastFive = Order.objects.order_by('placed_at').values('id')[:5]
    #query_set = OrderItem.objects.select_related('order','product').filter(order__in=lastFive)
    
    #Product.objects.filter(id__in=(OrderItem.objects.values('product_id').distinct())).order_by('title')
    # you can iterate over the query set
    #for product in query_set:
    #    print(product)
    #list(query_set)

    # #How many order do we have?
    # orderTotalCount = Order.objects.aggregate(count=Count('id'))['count']
    # #How many units of product 1 have we sold?
    # product1Sold = OrderItem.objects.filter(product=1).aggregate(count=Sum('quantity'))['count']
    # #Giw naby irders gas cystiner 1 placed?
    # customer1OrderCount = Order.objects.filter(customer=1).aggregate(count=Count('id'))['count']
    # # what is the min, max and avg price of the products in collection 3?
    # collection3PriceData = Product.objects.filter(collection=3).aggregate(
    #     min=Min('unit_price'), max=(Max('unit_price')), avg= Avg('unit_price')).items()
    # context = {
    #     'orderCount': orderTotalCount,
    #     'product1Sold': product1Sold,
    #     'customer1OrderCount' : customer1OrderCount,
    #     'collection3PriceData' : collection3PriceData,
    # }

    # #Customers with their last order ID
    # result = Customer.objects.annotate(
    #     last_order = Max('order__id')
    # )
    # #Collection and count of their products
    # result = Collection.objects.annotate(
    #     products_count = Count('product')
    # )
    # #Customer with more than 5 order
    # result = Customer.objects.annotate(
    #     total_orders = Count('order')
    # ).filter(total_orders__gt=5)
    # #Customer and the total amount they've spent
    # list(Customer.objects.annotate(
    #     total_spent = Sum(
    #         F('order__orderitem__unit_price') *
    #         F('order__orderitem__quantity')
    #     )
    # ))

    # #Top best'selling products and their total sales
    # list(Product.objects.annotate(
    #     total_sales = Sum(
    #         F('orderitem__unit_price') *
    #         F('orderitem__quantity')
    #     )
    # ).order_by('-total_sales')[:10])

    # #Creating an object
    # cart = Cart()
    # product = Product(pk=55)
    # cartItem = CartItem()
    # cartItem.product = product
    # cartItem.quantity = 5
    # cartItem.cart = cart
    # cart.save()
    # cartItem.save()

    #Update the quantity of an item in a shopping cart:
    item = CartItem.objects.get(pk=1)
    item.quantity = 2
    item.save()

    # Remove a shipping cart with its items.
    cart = Cart.objects.get(pk=1)
    cart.delete()






    return render(request, 'hello.html' )
