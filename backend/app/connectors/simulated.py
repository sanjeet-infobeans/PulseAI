"""Seeded connector — every simulated integration plugs in behind the same
interface so downstream code never branches on real-vs-simulated. Seeded payloads
live in `simulated_datasets` and are consumed directly by dashboard/projection
endpoints; delivery tables are not populated from here."""
from app.connectors.base import BaseConnector
from app.connectors.schemas import NormalizedBundle
from app.models.connector import ConnectorMode, ConnectorType


class SeededConnector(BaseConnector):
    mode = ConnectorMode.simulated

    def __init__(self, connector, secret=None):
        super().__init__(connector, secret)
        self.type = connector.type

    async def test_connection(self) -> None:
        # Seeded connectors are always "connected" — data ships with the app.
        return None

    async def fetch_and_normalize(self) -> NormalizedBundle:
        return NormalizedBundle()
