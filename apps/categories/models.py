from django.db import models
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    title = models.CharField(max_length=255, unique=True, verbose_name='Название')
    parent = TreeForeignKey('self', on_delete=models.CASCADE,  verbose_name="Категории", null=True, blank=True, related_name='children')

    class Meta:
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-detail', kwargs = {"pk" : self.pk})
    
    class Meta:
        verbose_name_plural = "Категории"
    