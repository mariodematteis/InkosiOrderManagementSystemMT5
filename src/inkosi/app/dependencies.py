from fastapi import Header, Request
from fastapi.exceptions import HTTPException

from inkosi.utils.settings import get_allowed_ip_addresses, get_api_settings


async def network_policies_check(
    request: Request,
) -> None:
    if (
        isinstance(get_allowed_ip_addresses(), str)
        and get_allowed_ip_addresses() == "*"
    ):
        return
    elif isinstance(get_allowed_ip_addresses(), list):
        ip_addr = request.client.host

        if ip_addr in get_allowed_ip_addresses():
            raise HTTPException(
                status_code=403,
                detail="Your IP Address is not allowed to access the content",
            )


async def authentication(
    x_token: str = Header(
        "",
    ),
) -> None:
    if not get_api_settings().TokenAuthentication:
        return

    if not x_token:
        raise HTTPException(
            status_code=403,
            detail="No data authentication have been provided",
        )
