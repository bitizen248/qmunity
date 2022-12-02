from tortoise import models
from tortoise import fields


class CvTag(models.Model):
    id = fields.UUIDField(pk=True)
    tag = fields.CharField(max_length=32)
    parent = fields.ForeignKeyField("models.CvTag", null=True)
    