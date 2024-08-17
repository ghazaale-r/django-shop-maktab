from .custom_user import User, UserManager

class OwnerManager(UserManager):

    def create_restaurant_owner(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)

        return super().create_user(email, password, **extra_fields)
    
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True, is_superuser=False)


class Owner(User):
    objects = OwnerManager()

    class Meta:
        proxy = True
        verbose_name="صاحب فروشگاه"
        verbose_name_plural = 'صاحب فروشگاه ها' 

    def get_profile_url(self):
        return "/owner/dashboard/"
    
    def save(self, *args, **kwargs):
        self.is_staff = True
        self.is_superuser = False
        self.is_active = True
        super().save(*args, **kwargs)

