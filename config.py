TORTOISE_ORM = {
    "connections": {
        "default": "sqlite://db.sqlite3"
    },
    "apps": {
        "models": {
            "models": ["models.user", "models.chat", "aerich.models"],
            "default_connection": "default",
        }
    },
}
