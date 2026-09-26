"""Passport manager for dynamic manifest loading, parsing, and integrity verification."""

import os
import yaml
from typing import Dict, Any, Optional
from .passport_schema import (
    PassportManifest,
    CapabilityManifest,
    ToolManifest,
    PassportValidationResult,
)


class PassportManager:
    """Manages agent passport lifecycle and validation."""

    def __init__(self, manifest_path: Optional[str] = None):
        if manifest_path is None:
            # Default to root agent.yaml relative to current file directory or workspace root
            root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            manifest_path = os.path.join(root_dir, "agent.yaml")

        self.manifest_path = manifest_path
        self.manifest: Optional[PassportManifest] = None
        self._raw_yaml: Dict[str, Any] = {}

    def load_passport(self) -> PassportManifest:
        """Load and parse agent.yaml file."""
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"Passport manifest not found at: {self.manifest_path}")

        with open(self.manifest_path, "r", encoding="utf-8") as f:
            self._raw_yaml = yaml.safe_load(f) or {}

        spec_version = self._raw_yaml.get("spec_version", "")
        metadata = self._raw_yaml.get("metadata", {})
        
        capabilities_raw = self._raw_yaml.get("capabilities", [])
        capabilities = [
            CapabilityManifest(
                name=c.get("name", ""),
                description=c.get("description", ""),
                input_requirements=c.get("input_requirements", {}),
                output_contract=c.get("output_contract", {}),
            )
            for c in capabilities_raw
        ]

        tools_raw = self._raw_yaml.get("tools", [])
        tools = [
            ToolManifest(
                name=t.get("name", ""),
                description=t.get("description", ""),
                capability=t.get("capability", ""),
            )
            for t in tools_raw
        ]

        self.manifest = PassportManifest(
            spec_version=spec_version,
            agent_id=metadata.get("agent_id", ""),
            name=metadata.get("name", ""),
            class_name=metadata.get("class_name", ""),
            version=metadata.get("version", ""),
            description=metadata.get("description", ""),
            author=metadata.get("author", "HiDevs x Lyzr Agent Passport Challenge"),
            license=metadata.get("license", "MIT"),
            capabilities=capabilities,
            tools=tools,
            contracts=self._raw_yaml.get("contracts", {}),
            adapters=self._raw_yaml.get("adapters", {}),
        )

        return self.manifest

    def validate_passport(self) -> PassportValidationResult:
        """Validate loaded passport manifest for compliance."""
        if self.manifest is None:
            self.load_passport()

        errors = []
        warnings = []
        verified_caps = []
        verified_tools = []

        m = self.manifest
        assert m is not None

        # 1. Spec version requirement
        if m.spec_version != "0.1.0":
            errors.append(f"Invalid spec_version: '{m.spec_version}'. Must be exactly '0.1.0'")

        # 2. Agent Name format (lowercase, hyphenated, starts with letter)
        if not m.name or not m.name[0].isalpha() or m.name.lower() != m.name or " " in m.name:
            errors.append(f"Invalid agent name format: '{m.name}'. Must be lowercase hyphenated starting with a letter.")

        # 3. Class Name requirement
        if not m.class_name or not m.class_name[0].isupper():
            errors.append(f"Invalid class_name: '{m.class_name}'. Must be PascalCase.")

        # 4. Capabilities check
        cap_names = {c.name for c in m.capabilities}
        for cap in m.capabilities:
            if not cap.name or not cap.description:
                errors.append(f"Capability missing name or description: {cap}")
            else:
                verified_caps.append(cap.name)

        # 5. Tools check & binding to capabilities
        for t in m.tools:
            if not t.name or not t.description:
                errors.append(f"Tool missing name or description: {t}")
            elif t.capability and t.capability not in cap_names:
                errors.append(f"Tool '{t.name}' references non-existent capability '{t.capability}'")
            else:
                verified_tools.append(t.name)

        is_valid = len(errors) == 0

        return PassportValidationResult(
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            verified_capabilities=verified_caps,
            verified_tools=verified_tools,
        )

    def get_summary(self) -> Dict[str, Any]:
        """Return summary of passport metadata."""
        if self.manifest is None:
            self.load_passport()

        m = self.manifest
        assert m is not None
        return {
            "spec_version": m.spec_version,
            "agent_id": m.agent_id,
            "name": m.name,
            "class_name": m.class_name,
            "version": m.version,
            "capabilities_count": len(m.capabilities),
            "tools_count": len(m.tools),
        }
