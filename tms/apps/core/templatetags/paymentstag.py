from django import template
# import payments model
from ..models import payments

register = template.Library()


@register.inclusion_tag("core/includes/pay_table.html")
def get_payments(tenancy):
    # Get all payments in the tenancy
    rent_payments = payments.objects.filter(rental=tenancy)
    count = len(rent_payments)

    return {
        'payments': rent_payments,
        'pay_count': count,
    }
