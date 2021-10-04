import secrets
import random


def generate_direction() -> str:

    return secrets.token_hex(8)


def generate_chat_id() -> int:

    return random.randint(1, 100_000_000)


def generate_handler_data() -> dict:

    return {"data": secrets.token_hex(8)}
