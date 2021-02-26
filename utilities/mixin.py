from django.contrib.auth.mixins import LoginRequiredMixin


class InstituteRequired(LoginRequiredMixin):
    """Verify that the current user is institute admin."""

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, 'institute'):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
