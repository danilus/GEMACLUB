from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def action_button(url, icon, label, btn_class="btn-primary", size=""):
    html = f"""
    <a href="{url}" class="btn {btn_class} {size} ms-1">
        <i class="bi {icon}"></i> {label}
    </a>
    """
    return mark_safe(html)
