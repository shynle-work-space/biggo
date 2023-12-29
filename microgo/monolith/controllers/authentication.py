from errors import Error
from instantiation import authenticator


def authentication(req) -> str | Error:
    """
    This function acts as a middleware for all private routes.

    Return `user_id` from JWT or Error
    """
    
    if "Authorization" not in req.headers:
        return Error("auth_error", 'Authorization header not found')
    token = req.headers["Authorization"].split(" ")[1]

    verified_sig = authenticator.validate_signature(token)
    if isinstance(verified_sig, Error):
        return Error("auth_error", 'JWT expired')
    
    return verified_sig["id"]