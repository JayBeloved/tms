from django import template
# import payments model
from ...core.models import landlord, managed_properties

register = template.Library()


@register.inclusion_tag("landlords/includes/_landlords_table.html")
def get_landlords(request):
    # Return all if user is an admin
    landlords = landlord.objects.all()
    l_count = landlords.__len__()
    if request.user.user_type == 2:
        # Get the landlord of the properties assigned to the agent
        landlords = set([p.landlord for p in managed_properties.objects.filter(registered_by=request.user)])
        l_count = landlords.__len__()

    return {
        'landlords': landlords,
        'count': l_count,
    }
