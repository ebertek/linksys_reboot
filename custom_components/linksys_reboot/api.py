"""APIs used for the Linksys Reboot integration."""

# pylint: disable=C0301, E0401

import logging

import aiohttp # type: ignore

_LOGGER = logging.getLogger(__name__)

CLIENT_TYPE_ID = "BB426FA7-16A9-5C1C-55AF-63A4167B26AD"

class LinksysApiClient:
    """Client to interact with the Linksys Smart Wi-Fi cloud API."""
    def __init__(self, username: str, password: str, session: aiohttp.ClientSession):
        """Initialize the API client."""
        self._username = username
        self._password = password
        self._session = session

    async def async_get_data(self):
        """Placeholder method to fetch and return dummy data for testing connectivity."""
        _LOGGER.debug("LinksysApiClient: async_get_data called")
        return {"status": "ready"}

    async def async_reboot_router(self):
        """Authenticate, fetch network ID, and trigger a router reboot."""
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
            _LOGGER.debug("Login response: %s", login_data)
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
            _LOGGER.debug("Network list response: %s", net_data)
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
            _LOGGER.debug("Reboot response: %s", result)
            return result.get("result") == "OK"

class LinksysApiClientError(Exception):
    """Base exception for Linksys API client errors."""

class LinksysApiClientCommunicationError(LinksysApiClientError):
    """Raised when communication with the API fails."""

class LinksysApiClientAuthenticationError(LinksysApiClientError):
    """Raised when authentication with the API fails."""
