from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.timezone import datetime
from store.models import *

# Create your views here.
class Dashboard(View, UserPassesTestMixin, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        # get the current date
        today = datetime.today()
        orders = OrderItem.objects.filter(
            date_added__year=today.year, date_added__month=today.month, date_added__day=today.day)

        # loop through the orders and add the price value
        total_revenue = 0
        for order in orders:
            total_revenue += order.quantity

        # pass the total number of orders and total revenue into templates
        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'total_orders': len(orders),
        }
        return render(request, 'restaurant/dashboard.html', context)

    def test_func(self):
        return self.request.user.groups.filter(name='staff').exists()
