from tortoise import fields, models
from passlib.hash import bcrypt
from datetime import datetime

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    password_hash = fields.CharField(max_length=256)
    first_name = fields.CharField(max_length=50, null=True)
    last_name = fields.CharField(max_length=50, null=True)
    is_online = fields.BooleanField(default=False)
    last_seen = fields.DatetimeField(null=True, auto_now=True)
    
    class Meta:
        table = "users"  # Явное указание имени таблицы

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    @classmethod
    def create_password_hash(cls, password: str) -> str:
        return bcrypt.hash(password)