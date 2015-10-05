from django import template

register = template.Library()

@register.inclusion_tag("partials/data_row.html", takes_context=True)
def data_row(context, tag, label, value):
    return {"tag": tag, "label": label, "value": value}
