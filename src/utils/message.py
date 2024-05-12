from typing import Any

from fastapi import Request


def flash(request: Request, message: Any, category: str = "primary"):
    if not request.session.get("flash"):
        request.session["flash"] = []
        request.session["flash"].append({"message": message, "category": category})
    else:
        request.session["flash"].append({"message": message, "category": category})


def get_flash_message(request: Request):
    if request.session.get("flash"):
        notice = request.session.get("flash")
        request.session.pop("flash")
        return notice
    return []
