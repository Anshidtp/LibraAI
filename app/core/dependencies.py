import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.database import get_database
from app.core.security import decode_access_token
from app.utils.constants import Role
from motor.motor_asyncio import AsyncIOMotorDatabase
from jose import JWTError

logger = logging.getLogger(__name__)

bearer_scheme = HTTPBearer(auto_error=False)


# ── Database dependency ───────────────────────────────────────────────────────
async def get_db() -> AsyncIOMotorDatabase:
    """Yield the Motor database handle (no teardown needed for Motor)."""
    return get_database()


DBDep = Annotated[AsyncIOMotorDatabase, Depends(get_db)]


# ── Current user dependency ───────────────────────────────────────────────────
async def get_current_user(
    db: DBDep,
    credentials: HTTPAuthorizationCredentials | None = Security(bearer_scheme),
) -> dict:
    """
    Validate Bearer JWT and return the active user document.
    Raises 401 on any failure.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None:
        raise credentials_exception

    try:
        payload = decode_access_token(credentials.credentials)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as exc:
        logger.warning("JWT validation failed: %s", exc)
        raise credentials_exception

    user = await db.users.find_one({"_id": user_id})
    if user is None:
        raise credentials_exception

    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )

    return user


CurrentUser = Annotated[dict, Depends(get_current_user)]


# ── RBAC guard ────────────────────────────────────────────────────────────────
def require_roles(*roles: str):
    """
    Dependency factory: inject into a route to restrict access by role.

    Usage:
        @router.get("/admin", dependencies=[Depends(require_roles("SUPER_ADMIN", "ADMIN"))])
    """

    async def _check(current_user: CurrentUser) -> dict:
        if current_user.get("role") not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {', '.join(roles)}",
            )
        return current_user

    return _check


# ── Convenience role guards ───────────────────────────────────────────────────
SuperAdminOnly = Depends(require_roles(Role.SUPER_ADMIN))
AdminOrAbove = Depends(require_roles(Role.SUPER_ADMIN, Role.ADMIN))
LibrarianOrAbove = Depends(
    require_roles(Role.SUPER_ADMIN, Role.ADMIN, Role.LIBRARIAN)
)
AnyAuthenticatedUser = Depends(get_current_user)