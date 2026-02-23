from pathlib import Path
from typing import Dict, List, Any
import yaml

DML_SCHEMA_VERSION = "1.0"

def create_dml(
    simulation_presets: Dict[str, Dict[str, Any]],
    samples: List[Dict[str, Any]],
    schema_version: str = DML_SCHEMA_VERSION,
) -> Dict[str, Any]:
    """
    Create an in-memory DML structure.
    """
    return {
        "schema_version": schema_version,
        "simulation_presets": simulation_presets,
        "samples": samples,
    }


def save_dml(dml: Dict[str, Any], path: str | Path) -> None:
    """
    Write DML to a YAML file.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(
            dml,
            f,
            sort_keys=False,
            default_flow_style=False,
        )


def load_dml(path: str | Path) -> Dict[str, Any]:
    """
    Load DML from a YAML file.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"DML file not found: {path}")

    with path.open("r", encoding="utf-8") as f:
        dml = yaml.safe_load(f)

    _basic_validate_dml(dml)
    return dml


def _basic_validate_dml(dml: Dict[str, Any]) -> None:
    """
    Minimal sanity checks.
    Intentionally lightweight – no full schema validation.
    """
    assert isinstance(dml, dict), "DML must be a dict"

    assert "schema_version" in dml, "Missing 'schema_version'"
    assert dml["schema_version"] == DML_SCHEMA_VERSION, (
        f"Unsupported schema_version: {dml['schema_version']}"
    )

    assert "simulation_presets" in dml, "Missing 'simulation_presets'"
    assert isinstance(dml["simulation_presets"], dict)

    assert "samples" in dml, "Missing 'samples'"
    assert isinstance(dml["samples"], list)

    for i, s in enumerate(dml["samples"]):
        assert "path" in s, f"Sample {i} missing 'path'"
        assert "sim" in s, f"Sample {i} missing 'sim'"
        assert "split" in s, f"Sample {i} missing 'split'"

        sim = s["sim"]
        assert (
            sim in dml["simulation_presets"]
        ), f"Sample {i} references unknown preset '{sim}'"
