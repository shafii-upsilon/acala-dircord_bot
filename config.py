TORTOISE_ORM = {
    "connections": {"default": "sqlite://acala.sqlite3"},
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        },
    },
}