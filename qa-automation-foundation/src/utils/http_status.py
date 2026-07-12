"""Tiny classification helpers so tests can assert "this was a client error"
without hardcoding numeric ranges inline in every spec."""


def is_success(status: int) -> bool:
    return 200 <= status < 300


def is_client_error(status: int) -> bool:
    return 400 <= status < 500


def is_server_error(status: int) -> bool:
    return 500 <= status < 600
