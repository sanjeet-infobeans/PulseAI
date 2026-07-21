import os

from fastapi import HTTPException

from app.connectors.base import BaseConnector
from app.connectors.jira import JiraConnector
from app.connectors.simulated import SeededConnector
from app.models.connector import Connector, ConnectorMode, ConnectorType

# Real connectors by type. Anything not listed falls back to the seeded connector.
_REAL: dict[ConnectorType, type[BaseConnector]] = {
    ConnectorType.jira: JiraConnector,
}


def _resolve_secret(connector: Connector) -> str | None:
    if not connector.secret_ref:
        return None
    return os.environ.get(connector.secret_ref)


def get_connector(connector: Connector) -> BaseConnector:
    """Factory: real connector when the type is implemented and mode is real,
    otherwise the seeded connector. Mirrors the AIMS provider registry."""
    if connector.mode == ConnectorMode.real and connector.type in _REAL:
        return _REAL[connector.type](connector, _resolve_secret(connector))
    if connector.mode == ConnectorMode.real and connector.type not in _REAL:
        raise HTTPException(
            status_code=400,
            detail=f"Real connector '{connector.type.value}' is not implemented; use simulated mode",
        )
    return SeededConnector(connector)
