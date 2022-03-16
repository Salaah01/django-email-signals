from django.contrib import admin
from . import models, forms


class SignalConstraintInline(admin.TabularInline):
    form = forms.SignalConstraintAdminForm
    model = models.SignalConstraint
    extra = 0


@admin.register(models.Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "content_type",
        "signal_type",
        "constraints_count",
        "active",
    )

    form = forms.SignalAdminForm
    change_form_template = "email_signals/admin/email_signals/signal/change_form.html"  # noqa: E501
    inlines = [SignalConstraintInline]

    class Media:
        css = {"all": ("email_signals/css/signal_change_form.min.css",)}
        js = ("email_signals/js/signal_change_form.min.js",)
