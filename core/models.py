from django.db import models

# Abstract base model that provides self-updating
# 'created_at' and 'updated_at' fields.
class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']

# Abstract base model that provides soft delete functionality.
class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    # Soft delete the instance
    def soft_delete(self):
        from django.utils import timezone
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    # Restore a soft deleted instance.
    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()
