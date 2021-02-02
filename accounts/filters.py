import django_filters
from django_filters import DateFilter

from .models import LoginLog


class LogFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr="gte")
    end_date = DateFilter(field_name="date_created", lookup_expr="lte")

    class Meta:
        model = LoginLog
        fields = "__all__"
        exclude = ["owner", "login_log", "date_created"]

