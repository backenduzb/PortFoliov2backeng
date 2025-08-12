from tortoise import models, fields
from datetime import datetime

class Global(models.Model):
    id = fields.IntField(pk=True)
    message = fields.TextField()
    user = fields.ForeignKeyField("models.User", related_name="global_messages")
    username = fields.CharField(max_length=256)
    user_full_name = fields.CharField(max_length=512)
    sendet_data = fields.DatetimeField()

    class Meta:
        table = "global_messages"


class Chat(models.Model):
    id = fields.IntField(pk=True)
    user1 = fields.ForeignKeyField(
        'models.User',
        related_name='user1_chats',
        on_delete=fields.CASCADE
    )
    user2 = fields.ForeignKeyField(
        'models.User',
        related_name='user2_chats',
        on_delete=fields.CASCADE
    )
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "chats"
        unique_together = [('user1', 'user2')]

    async def get_other_user(self, current_user_id: int) -> 'User':
        return await self.user2 if self.user1_id == current_user_id else await self.user1

class Message(models.Model):
    id = fields.IntField(pk=True)
    chat = fields.ForeignKeyField(
        'models.Chat',
        related_name='messages',
        on_delete=fields.CASCADE
    )
    sender = fields.ForeignKeyField(
        'models.User',
        related_name='sent_messages',
        on_delete=fields.CASCADE
    )
    content = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    is_read = fields.BooleanField(default=False)

    class Meta:
        table = "messages"
        ordering = ["created_at"]