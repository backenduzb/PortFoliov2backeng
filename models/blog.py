from tortoise import fields, models

class Blog(models.Model):
    img_url = fields.CharField(max_length=1024)
    title = fields.CharField(max_length=256)
    text = fields.TextField()
    