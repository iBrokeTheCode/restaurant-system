from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.timezone import datetime, now, timedelta
from django.views.generic import TemplateView


class GroupRequiredMixin(UserPassesTestMixin):
    group_required = []

    def test_func(self) -> bool:
        user = self.request.user  # type: ignore
        return (
            user.is_authenticated
            and user.groups.filter(name__in=self.group_required).exists()
        )


class DateRangeFilterMixin(TemplateView):
    date_field = None  # You must define this in the view (e.g., 'payment_time__date')

    def get_date_range(self):
        """Returns a tuple: (start_date, end_date) based on request.GET"""
        today = now().date()
        range_type = self.request.GET.get('range', 'today')
        start = end = today

        if range_type == 'week':
            start = today - timedelta(days=today.weekday())
            end = today

        elif range_type == 'month':
            start = today.replace(day=1)
            end = today

        elif range_type == 'custom':
            try:
                start_str = self.request.GET.get('start')
                end_str = self.request.GET.get('end')
                if start_str and end_str:
                    start = datetime.strptime(start_str, '%Y-%m-%d').date()
                    end = datetime.strptime(end_str, '%Y-%m-%d').date()
                    if start > end:
                        raise ValueError('Start date cannot be after end date.')
                else:
                    raise ValueError('Missing start or end date.')
            except ValueError:
                messages.warning(
                    self.request, "Invalid custom date range. Showing today's data."
                )
                start = end = today

        return start, end

    def filter_queryset_by_date(self, queryset):
        """Filters the queryset using the date range and the specified field."""
        if not self.date_field:
            raise ValueError('You must define `date_field` in your view.')
        start, end = self.get_date_range()
        self.start_date = start
        self.end_date = end
        return queryset.filter(**{f'{self.date_field}__range': (start, end)})

    def get_context_data(self, **kwargs):
        """Adds start and end dates to context."""
        context = super().get_context_data(**kwargs)
        context['start'] = getattr(self, 'start_date', now().date())
        context['end'] = getattr(self, 'end_date', now().date())
        return context
