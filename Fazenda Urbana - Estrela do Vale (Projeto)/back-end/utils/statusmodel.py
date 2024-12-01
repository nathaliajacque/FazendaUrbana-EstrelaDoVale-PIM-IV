from django.db import models

# Status ativo e inativo


class StatusModel(models.Model):
    STATUS_CHOICES = [
        ("ATIVO", "Ativo"),
        ("INATIVO", "Inativo"),
    ]

    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default="ATIVO")

    class Meta:
        abstract = True

    @classmethod
    def inativar(cls, id_obj):
        try:
            obj = cls.objects.get(pk=id_obj)
            obj.status = "INATIVO"
            obj.save()
            return obj
        except cls.DoesNotExist:
            return None

    @classmethod
    def ativar(cls, id_obj):
        try:
            obj = cls.objects.get(pk=id_obj)
            obj.status = "ATIVO"
            obj.save()
            return obj
        except cls.DoesNotExist:
            return None
