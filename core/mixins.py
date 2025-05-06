from django.contrib.auth.mixins import UserPassesTestMixin


class GroupRequiredMixin(UserPassesTestMixin):
    group_required = []

    def test_func(self) -> bool:
        user = self.request.user  # type: ignore
        return (
            user.is_authenticated
            and user.groups.filter(name__in=self.group_required).exists()
        )
