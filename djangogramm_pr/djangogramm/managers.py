import os

from django.db.models import QuerySet


class PostQuerySet(QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            for image in obj.media.all():
                os.remove(image.preview.path)
                os.remove(image.original.path)

        super().delete(*args, **kwargs)