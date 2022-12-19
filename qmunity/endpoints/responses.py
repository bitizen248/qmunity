from pydantic import BaseModel


class SimpleResponse(BaseModel):
    """
    Simple response in format {"success": true|false, "reason": "str"}
    """
    success: bool = True
    reason: str | None

    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = True
            return BaseModel.dict(self, *args, **kwargs)
