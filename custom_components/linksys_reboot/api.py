import aiohttp
import logging

_LOGGER = logging.getLogger(__name__)

CLIENT_TYPE_ID = "BB426FA7-16A9-5C1C-55AF-63A4167B26AD"

class LinksysApiClient:
    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        self._username = username
        self._password = password
        self._session = session

    async def async_get_data(self):
        _LOGGER.debug("LinksysApiClient: async_get_data called")
        return {"status": "ready"}

    async def async_reboot_router(self):
        _LOGGER.debug("LinksysApiClient: async_reboot_router called")

        login_payload = {
            "session": {
                "account": {
                    "username": self._username,
                    "password": self._password
                }
            }
        }
        login_headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
            "X-Linksys-Client-Type-Id": CLIENT_TYPE_ID,
            "X-Linksys-Network-Id": "null",
            "X-Linksys-Router-FW-Version": "null",
            "X-Linksys-Router-Model-Number": "null",
            "X-Requested-With": "XMLHttpRequest"
        }

        async with self._session.post("https://linksyssmartwifi.com/cloud/user-service/rest/v2/sessions",
                                      headers=login_headers, json=login_payload) as resp:
            login_data = await resp.json()
            _LOGGER.debug(f"Login response: {login_data}")
            token = login_data.get("session", {}).get("token")
            if not token:
                _LOGGER.error("Authentication failed")
                return False

        network_headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
            "Authorization": f'CiscoHNUserAuth session_token="{token}"',
            "X-Linksys-Client-Type-Id": CLIENT_TYPE_ID,
            "X-Linksys-Network-Id": "null",
            "X-Linksys-Router-FW-Version": "null",
            "X-Linksys-Router-Model-Number": "null",
            "X-Requested-With": "XMLHttpRequest"
        }

        async with self._session.get("https://linksyssmartwifi.com/cloud/device-service/rest/accounts/self/networks",
                                     headers=network_headers) as resp:
            net_data = await resp.json()
            _LOGGER.debug(f"Network list response: {net_data}")
            networks = net_data.get("networkAccountAssociations", [])
            if not networks:
                _LOGGER.error("No networks found")
                return False
            network_id = networks[0].get("networkAccountAssociation", {}).get("network", {}).get("networkId")
            if not network_id:
                _LOGGER.error("Failed to extract network ID")
                return False

        reboot_headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "*/*",
            "Authorization": f'CiscoHNUserAuth session_token="{token}"',
            "X-JNAP-Action": "http://linksys.com/jnap/core/Reboot",
            "X-Linksys-Client-Type-Id": CLIENT_TYPE_ID,
            "X-Linksys-Network-Id": network_id,
            "X-Requested-With": "XMLHttpRequest"
        }

        async with self._session.post("https://linksyssmartwifi.com/cloud/JNAP/", headers=reboot_headers, json={}) as resp:
            result = await resp.json()
            _LOGGER.debug(f"Reboot response: {result}")
            return result.get("result") == "OK"

class LinksysApiClientError(Exception):
    pass

class LinksysApiClientCommunicationError(LinksysApiClientError):
    pass

class LinksysApiClientAuthenticationError(LinksysApiClientError):
    pass