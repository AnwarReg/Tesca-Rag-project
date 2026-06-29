import jwt
from fastapi import Header, HTTPException, status
from jwt import PyJWKClient

from app.config import settings

# Fetches and caches Clerk's public signing keys (JWKS). It only hits the
# network the first time a key id is seen, then caches it.
_jwks_client = PyJWKClient(settings.clerk_jwks_url)


def get_current_user(authorization: str = Header(...)) -> str:
    """Validate the Clerk JWT and return the user id (the token's `sub` claim).

    Inject this into any endpoint that needs auth. The returned id is what we
    scope every document/query to, so a user can only ever see their own data.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Missing bearer token")

    token = authorization.removeprefix("Bearer ")
    try:
        signing_key = _jwks_client.get_signing_key_from_jwt(token)
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
