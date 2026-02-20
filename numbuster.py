import asyncio
from typing import Any, Dict
from curl_cffi import requests

async def numbuster(phone: str) -> Dict[str, Any]:
    url = f"https://app.truenmbapp.de/api/v202505/search/{phone}"

    params = {
        "locale": "ru-ru",
        "paidSearch": "0",
        "source": "WEB",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 ...",
        "Accept": "application/json",
        "content-type": "application/json",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "cors",
        "referer": f"https://app.truenmbapp.de/number/{phone}",
        "sec-fetch-dest": "empty",
        "authorization": "", # Need token
        "accept-language": "ru",
        "priority": "u=3, i",
        "Cookie": "", # Need cookie
    }

    try:
        async with requests.AsyncSession(impersonate="safari_ios") as s:
            resp = await s.get(url, params=params, headers=headers, timeout=30)

        if resp.status_code >= 400:
            return {
                "ok": False,
                "status": resp.status_code,
                "error": "http_error",
                "body_preview": resp.text[:500],
            }

        try:
            data = resp.json()
        except Exception:
            return {
                "ok": False,
                "status": resp.status_code,
                "error": "not_json",
                "body_preview": resp.text[:500],
            }

        if isinstance(data, dict) and "ok" not in data:
            data = {"ok": True, "status": resp.status_code, "data": data}
        return data

    except (requests.RequestsError, asyncio.TimeoutError) as e:
        return {"ok": False, "error": "request_failed", "detail": str(e)[:300]}
    except Exception as e:
        return {"ok": False, "error": "unexpected", "detail": str(e)[:300]}
