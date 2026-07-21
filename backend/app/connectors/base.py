from abc import ABC, abstractmethod
from typing import ClassVar

from app.connectors.schemas import NormalizedBundle
from app.models.connector import Connector, ConnectorMode, ConnectorType


class BaseConnector(ABC):
    """One concrete subclass per integration. Repurposes the AIMS provider ABC.

    A connector is constructed from its DB row plus an optional resolved secret
    (e.g. a Jira API token read from an env var named by `connector.secret_ref`).
    """

    type: ClassVar[ConnectorType]
    mode: ClassVar[ConnectorMode]

    def __init__(self, connector: Connector, secret: str | None = None) -> None:
        self.connector = connector
        self.secret = secret
        self.config: dict = connector.config or {}

    @abstractmethod
    async def test_connection(self) -> None:
        """Raise HTTPException if the connector cannot reach its source."""

    @abstractmethod
    async def fetch_and_normalize(self) -> NormalizedBundle:
        """Fetch source data and return it in the normalized shape."""
