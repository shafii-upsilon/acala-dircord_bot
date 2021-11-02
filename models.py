from enum import unique
from tortoise.models import Model
from tortoise import fields

class Question(Model):
    id = fields.IntField(pk=True, unique=True)
    question = fields.TextField()
    answer = fields.TextField()
    user = fields.CharField(max_length=50)
    created_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return 'Question {0}'.format(self.id)