
from django.contrib import admin
from django.db.models import lookups
from django.db.models.expressions import F, Value
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from django.db.models.aggregates import Count, Sum
from . import models

#Customizable filter
class InventoryFilter(admin.SimpleListFilter):
    #for visualization
    title = 'inventory'
    #for query string (URL)
    parameter_name = 'inventory'
    
    # list of options as tuples, one for the parameter and the other for human-readable
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
        ]
    
    # define a queryset to filter the items
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

#create new class admin
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display  = ['last_name','first_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    ordering      = ['last_name','first_name']
    search_fields = ['last_name__istartswith', 'first_name__istartswith','id__istartswith']
    
    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist')
                            + '?'
                            + urlencode({
                                'customer__id' : str(customer.id)
                            })
        )
        
        return format_html('<a href={}>{}</a>',url,customer.order_count )
    
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            order_count = Count('order')
        )

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title'],
    }
    actions       = ['clear_inventory']
    list_display  = ['title','unit_price','inventory_status','last_update', 'total_units_sold', 'collection']
    list_editable = ['unit_price']
    list_per_page = 20
    list_filter   = ['collection', InventoryFilter]
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    def total_units_sold(self, product):
        return product.orderItem_sum
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orderItem_sum = Sum('orderitem')
        )
    
    @admin.action(description='Clear Inventory')    
    def clear_inventory(self, request, queryset):
        updated_inventory = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_inventory} product/s updated',
            )
    
@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display  = ['id', 'placed_at', 'customer', 'items_count']
    list_per_page = 15
    ordering      = ['-id']
    
    def items_count(self, order):
        url = (reverse('admin:store_orderitem_changelist')
                + '?'
                + urlencode({
                    'order__id' : str(order.id)
                })
        )
        
        return format_html('<a href={}>{}</a>', url, order.items_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count = Count('orderitem')
        )

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order_id','product','quantity','unit_price','total_amount']
    ordering = ['order','product']
    
    def total_amount(self, orderItem):
        return (orderItem.quantity * orderItem.unit_price)

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    ordering = ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
                        + '?'
                        + urlencode({
                            'collection__id' : str(collection.id),
                        })
                        )
                        
        return format_html('<a href={}>{}</a>',url, collection.products_count)
    

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product'))

