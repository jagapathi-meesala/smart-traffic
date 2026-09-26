"""Base tool class defining abstract interface and contract enforcement."""

from abc import ABC, abstractmethod
from typing import Dict, Any
import pandas as pd


class BaseTool(ABC):
    """Abstract Base Class for all Smart Traffic Management Domain Tools."""

    def __init__(self, name: str, description: str, capability: str):
        self.name = name
        self.description = description
        self.capability = capability

    @abstractmethod
    def execute(self, df: pd.DataFrame, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute domain tool against a pandas DataFrame and execution context.
        Must return a structured dictionary output.
        """
        pass

    def validate_input(self, df: pd.DataFrame) -> bool:
        """Validate that input dataframe is valid."""
        return isinstance(df, pd.DataFrame) and not df.empty
