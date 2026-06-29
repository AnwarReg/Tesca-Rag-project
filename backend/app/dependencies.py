import jwt
from fastapi import Header, HTTPException, status
from jwt import PyJWKClient

from app.config import settings

# Built lazily on first real validation so local dev (with the bypass on) never
# needs Clerk configured at all.
_jwks_client: PyJWKClient | None = None


def _get_jwks_client() -> PyJWKClient:
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient(settings.clerk_jwks_url)
    return _jwks_client


def get_current_user(authorization: str | None = Header(default=None)) -> str:
    """Validate the Clerk JWT and return the user id (the token's `sub` claim).

    With DEV_AUTH_BYPASS on, validation is skipped and every request is treated
    as `dev_user_id` — a local-testing convenience, never for production.
    """
    if settings.dev_auth_bypass:
        return settings.dev_user_id

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")

    token = authorization.removeprefix("Bearer ")
    try:
        signing_key = _get_jwks_client().get_signing_key_from_jwt(token)
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=settings.clerk_issuer,
            options={"verify_aud": False},
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Invalid token") from exc

    return claims["sub"]
