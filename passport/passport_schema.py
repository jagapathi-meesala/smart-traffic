"""Passport schema definition matching spec version 0.1.0."""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class CapabilityManifest:
    """Capability schema item."""
    name: str
    description: str
    input_requirements: Optional[Dict[str, Any]] = field(default_factory=dict)
    output_contract: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class ToolManifest:
    """Tool schema item."""
    name: str
    description: str
    capability: str


@dataclass
class PassportManifest:
    """Root agent passport manifest."""
    spec_version: str
    agent_id: str
    name: str
    class_name: str
    version: str
    description: str
    capabilities: List[CapabilityManifest] = field(default_factory=list)
    tools: List[ToolManifest] = field(default_factory=list)
    author: str = "HiDevs x Lyzr Agent Passport Challenge"
    license: str = "MIT"
    contracts: Dict[str, str] = field(default_factory=dict)
    adapters: Dict[str, str] = field(default_factory=dict)


@dataclass
class PassportValidationResult:
    """Result of passport validation check."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    verified_capabilities: List[str] = field(default_factory=list)
    verified_tools: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "verified_capabilities": self.verified_capabilities,
            "verified_tools": self.verified_tools,
        }
