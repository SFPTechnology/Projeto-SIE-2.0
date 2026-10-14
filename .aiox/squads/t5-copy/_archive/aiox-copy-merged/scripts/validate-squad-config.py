#!/usr/bin/env python3
"""
validate-squad-config.py - Squad Config Integrity Validator

Detects mismatches between filesystem and config.yaml:
- Orphan files: exist on disk but not registered in config
- Ghost entries: registered in config but no corresponding file
- FK violations: archived_agents without files in archive/
- Backup files: .backup, .bak, .old, .backup-atomic files
- YAML validation: config.yaml syntax check
- ID uniqueness: duplicate IDs within sections
- Version consistency: version across config.yaml, README.md, ARCHITECTURE.md

Usage:
    python3 validate-squad-config.py <squad-path>
    python3 validate-squad-config.py <squad-path> --verbose
    python3 validate-squad-config.py <squad-path> --json

Exit codes:
    0 = clean (no problems)
    1 = problems found
    2 = fatal error (config missing, invalid YAML)

Story 8 - Copy Squad Config Sync & Documentation Alignment v4.0
"""

import sys
import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Set, Tuple, Optional

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(2)


# ============================================================================
# FILE-TO-CONFIG MAPPING
# ============================================================================

# Each entry: (filesystem_dir, config_section, file_extensions, supports_subdirs)
SECTION_MAPPINGS = {
    "agents": {
        "dir": "agents",
        "config_key": "agents",
        "id_field": "id",
        "extensions": [".md"],
        "subdirs": False,
    },
    "tasks": {
        "dir": "tasks",
        "config_key": "tasks",
        "id_field": "id",
        "extensions": [".md"],
        "subdirs": True,  # plf/, brunson/
    },
    "checklists": {
        "dir": "checklists",
        "config_key": "checklists",
        "id_field": "id",
        "extensions": [".md"],
        "subdirs": True,  # plf/, brunson/
    },
    "templates": {
        "dir": "templates",
        "config_key": "templates",
        "id_field": "id",
        "extensions": [".md", ".yaml", ".yml"],
        "subdirs": True,  # plf/, brunson/, swipe/
        "exclude_files": ["copy-state.json", "progress-copy.txt", "prompt-copy.md",
                          ".DS_Store"],
        "exclude_dirs": ["pipeline"],  # pipeline/ is internal state, not a template
    },
    "data": {
        "dir": "data",
        "config_key": "data",
        "id_field": "id",
        "extensions": [".md", ".yaml", ".yml"],
        "subdirs": True,  # plf/
    },
    "research": {
        "dir": "docs/research",
        "config_key": "research",
        "id_field": "id",
        "extensions": [".md"],
        "subdirs": False,
        "nested_key": "documents",  # config.research.documents[]
    },
    "workflows": {
        "dir": "workflows",
        "config_key": "yolo_mode",
        "id_field": "id",
        "extensions": [".yaml", ".yml"],
        "subdirs": False,
        "nested_path": ["workflows"],  # config.yolo_mode.workflows[]
    },
}


# ============================================================================
# HELPERS
# ============================================================================

def load_config(config_path: Path) -> Tuple[Optional[Dict], Optional[str]]:
    """Load and parse config.yaml. Returns (config_dict, error_message)."""
    if not config_path.exists():
        return None, f"config.yaml not found at {config_path}"
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        if not isinstance(config, dict):
            return None, "config.yaml did not parse to a dictionary"
        return config, None
    except yaml.YAMLError as e:
        return None, f"YAML syntax error: {e}"


def file_to_id(filepath: Path, base_dir: Path) -> str:
    """Convert a filepath to its expected config ID.

    Examples:
        agents/gary-halbert.md -> gary-halbert
        tasks/plf/create-plc-sequence.md -> plf/create-plc-sequence
        templates/brunson/book-funnel-sales-page-tmpl.md -> brunson/book-funnel-sales-page-tmpl
        data/plf/avatar-framework-kb.yaml -> plf/avatar-framework-kb
    """
    rel = filepath.relative_to(base_dir)
    # Remove extension
    stem = rel.with_suffix("")
    # Convert Path to string with forward slashes
    return str(stem).replace("\\", "/")


def get_config_ids(config: Dict, mapping: Dict) -> Set[str]:
    """Extract all IDs from a config section based on mapping."""
    ids = set()
    config_key = mapping["config_key"]
    id_field = mapping["id_field"]

    section = config.get(config_key)
    if section is None:
        return ids

    # Handle nested keys like research.documents
    if "nested_key" in mapping:
        if isinstance(section, dict):
            section = section.get(mapping["nested_key"], [])
        else:
            return ids

    # Handle nested path like yolo_mode.workflows
    if "nested_path" in mapping:
        if isinstance(section, dict):
            for key in mapping["nested_path"]:
                section = section.get(key, [])
                if not isinstance(section, (dict, list)):
                    return ids
        else:
            return ids

    if isinstance(section, list):
        for item in section:
            if isinstance(item, dict) and id_field in item:
                ids.add(item[id_field])

    return ids


def get_filesystem_ids(squad_path: Path, mapping: Dict) -> Set[str]:
    """Scan filesystem and return set of IDs based on mapping."""
    ids = set()
    base_dir = squad_path / mapping["dir"]

    if not base_dir.exists():
        return ids

    extensions = set(mapping["extensions"])
    exclude_files = set(mapping.get("exclude_files", []))
    exclude_dirs = set(mapping.get("exclude_dirs", []))
    supports_subdirs = mapping.get("subdirs", False)

    if supports_subdirs:
        # Recurse into subdirectories
        for filepath in base_dir.rglob("*"):
            if not filepath.is_file():
                continue
            if filepath.suffix not in extensions:
                continue
            if filepath.name in exclude_files:
                continue
            # Check if any parent dir (relative to base) is excluded
            rel = filepath.relative_to(base_dir)
            parts = rel.parts
            if len(parts) > 1 and parts[0] in exclude_dirs:
                continue
            ids.add(file_to_id(filepath, base_dir))
    else:
        # Only direct children
        for filepath in base_dir.iterdir():
            if not filepath.is_file():
                continue
            if filepath.suffix not in extensions:
                continue
            if filepath.name in exclude_files:
                continue
            ids.add(file_to_id(filepath, base_dir))

    return ids


def find_backup_files(squad_path: Path) -> List[str]:
    """Find any backup files in the squad directory."""
    backup_patterns = [".backup", ".bak", ".old", ".backup-atomic"]
    found = []
    for filepath in squad_path.rglob("*"):
        if not filepath.is_file():
            continue
        name = filepath.name
        for pattern in backup_patterns:
            if name.endswith(pattern):
                found.append(str(filepath.relative_to(squad_path)))
                break
    return found


def check_id_uniqueness(config: Dict) -> List[Dict[str, Any]]:
    """Check for duplicate IDs within each config section."""
    duplicates = []

    sections_to_check = [
        ("agents", "agents", None),
        ("tasks", "tasks", None),
        ("templates", "templates", None),
        ("checklists", "checklists", None),
        ("data", "data", None),
        ("research.documents", "research", "documents"),
        ("yolo_mode.workflows", "yolo_mode", "workflows"),
    ]

    for label, key, nested in sections_to_check:
        section = config.get(key)
        if section is None:
            continue

        if nested:
            if isinstance(section, dict):
                section = section.get(nested, [])
            else:
                continue

        if not isinstance(section, list):
            continue

        seen = {}
        for item in section:
            if isinstance(item, dict) and "id" in item:
                item_id = item["id"]
                if item_id in seen:
                    seen[item_id] += 1
                else:
                    seen[item_id] = 1

        for item_id, count in seen.items():
            if count > 1:
                duplicates.append({
                    "section": label,
                    "id": item_id,
                    "count": count,
                })

    return duplicates


def check_version_consistency(squad_path: Path, config: Dict) -> List[Dict[str, str]]:
    """Check version consistency across config.yaml, README.md, ARCHITECTURE.md."""
    issues = []

    # Get config version
    config_version = None
    pack = config.get("pack", {})
    if isinstance(pack, dict):
        config_version = pack.get("version")

    if not config_version:
        issues.append({
            "file": "config.yaml",
            "message": "No version found in pack.version",
        })
        return issues

    # Check README.md
    readme_path = squad_path / "README.md"
    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8", errors="ignore")
        # Look for version patterns like "v4.0.0", "Version: 4.0.0", "version: 4.0.0"
        version_matches = re.findall(
            r'(?:version|versão|v)[\s:]*["\']?(\d+\.\d+\.\d+)', content, re.IGNORECASE
        )
        if version_matches:
            readme_version = version_matches[0]
            if readme_version != config_version:
                issues.append({
                    "file": "README.md",
                    "message": f"Version mismatch: README={readme_version}, config={config_version}",
                })
        else:
            issues.append({
                "file": "README.md",
                "message": "No version pattern found in README.md",
            })

    # Check ARCHITECTURE.md
    arch_path = squad_path / "ARCHITECTURE.md"
    if arch_path.exists():
        content = arch_path.read_text(encoding="utf-8", errors="ignore")
        version_matches = re.findall(
            r'(?:version|versão|v)[\s:]*["\']?(\d+\.\d+\.\d+)', content, re.IGNORECASE
        )
        if version_matches:
            arch_version = version_matches[0]
            if arch_version != config_version:
                issues.append({
                    "file": "ARCHITECTURE.md",
                    "message": f"Version mismatch: ARCHITECTURE={arch_version}, config={config_version}",
                })

    return issues


def check_archived_agents_fk(squad_path: Path, config: Dict) -> List[Dict[str, str]]:
    """Check that archived agents have files in archive/agents/."""
    issues = []

    archived = config.get("archived_agents", {})
    if not isinstance(archived, dict):
        return issues

    agents_list = archived.get("agents", [])
    if not isinstance(agents_list, list):
        return issues

    archive_dir = squad_path / "archive" / "agents"

    for entry in agents_list:
        if isinstance(entry, dict) and "id" in entry:
            agent_id = entry["id"]
            expected_file = archive_dir / f"{agent_id}.md"
            if not expected_file.exists():
                issues.append({
                    "id": agent_id,
                    "expected": str(expected_file.relative_to(squad_path)),
                    "message": f"Archived agent '{agent_id}' has no file in archive/agents/",
                })

    return issues


def check_workspace_integration(squad_path: Path, config: Dict) -> List[Dict[str, str]]:
    """Check workspace integration contract and workspace_first requirements."""
    issues = []
    ws = config.get("workspace_integration")

    if not isinstance(ws, dict):
        issues.append({
            "field": "workspace_integration",
            "message": "Missing workspace_integration block in config.yaml",
        })
        return issues

    level = ws.get("level")
    allowed_levels = {"none", "read_only", "read_write", "workspace_first"}
    if level not in allowed_levels:
        issues.append({
            "field": "workspace_integration.level",
            "message": f"Invalid level '{level}'. Allowed: {sorted(allowed_levels)}",
        })

    read_paths = ws.get("read_paths", [])
    write_paths = ws.get("write_paths", [])

    if not isinstance(read_paths, list) or len(read_paths) == 0:
        issues.append({
            "field": "workspace_integration.read_paths",
            "message": "read_paths must be a non-empty list",
        })
    if not isinstance(write_paths, list):
        issues.append({
            "field": "workspace_integration.write_paths",
            "message": "write_paths must be a list",
        })

    if isinstance(read_paths, list):
        for rel_path in read_paths:
            abs_path = squad_path.parent.parent / str(rel_path)
            if not abs_path.exists():
                issues.append({
                    "field": "workspace_integration.read_paths",
                    "message": f"Declared read path does not exist: {rel_path}",
                })

    if isinstance(write_paths, list):
        for rel_path in write_paths:
            abs_path = squad_path.parent.parent / str(rel_path)
            if not abs_path.exists():
                issues.append({
                    "field": "workspace_integration.write_paths",
                    "message": f"Declared write path does not exist: {rel_path}",
                })

    if level == "workspace_first":
        required_scripts = [
            squad_path / "scripts" / "bootstrap-copy-workspace.sh",
            squad_path / "scripts" / "validate-copy-essentials.sh",
        ]
        for script_path in required_scripts:
            if not script_path.exists():
                issues.append({
                    "field": "workspace_integration.level",
                    "message": f"workspace_first requires script: {script_path.relative_to(squad_path)}",
                })

    return issues


# ============================================================================
# MAIN VALIDATION
# ============================================================================

def validate(squad_path: Path, verbose: bool = False) -> Dict[str, Any]:
    """Run all validation checks and return results."""
    results = {
        "squad_path": str(squad_path),
        "squad_name": squad_path.name,
        "checks": {},
        "summary": {
            "total_orphans": 0,
            "total_ghosts": 0,
            "total_issues": 0,
            "status": "clean",
        },
    }

    # --- Check 1: YAML Validation ---
    config_path = squad_path / "config.yaml"
    config, yaml_error = load_config(config_path)

    results["checks"]["yaml_validation"] = {
        "passed": yaml_error is None,
        "error": yaml_error,
    }

    if config is None:
        results["summary"]["status"] = "fatal"
        results["summary"]["total_issues"] = 1
        return results

    # --- Check 2: Orphan & Ghost Detection per section ---
    orphan_ghost_results = {}
    total_orphans = 0
    total_ghosts = 0

    for section_name, mapping in SECTION_MAPPINGS.items():
        fs_ids = get_filesystem_ids(squad_path, mapping)
        config_ids = get_config_ids(config, mapping)

        orphans = sorted(fs_ids - config_ids)
        ghosts = sorted(config_ids - fs_ids)

        total_orphans += len(orphans)
        total_ghosts += len(ghosts)

        section_result = {
            "filesystem_count": len(fs_ids),
            "config_count": len(config_ids),
            "orphans": orphans,
            "orphan_count": len(orphans),
            "ghosts": ghosts,
            "ghost_count": len(ghosts),
            "passed": len(orphans) == 0 and len(ghosts) == 0,
        }

        if verbose:
            section_result["filesystem_ids"] = sorted(fs_ids)
            section_result["config_ids"] = sorted(config_ids)

        orphan_ghost_results[section_name] = section_result

    results["checks"]["orphan_ghost"] = orphan_ghost_results

    # --- Check 3: FK Validation (archived agents) ---
    fk_issues = check_archived_agents_fk(squad_path, config)
    results["checks"]["fk_validation"] = {
        "passed": len(fk_issues) == 0,
        "issues": fk_issues,
        "issue_count": len(fk_issues),
    }

    # --- Check 4: Backup File Detection ---
    backup_files = find_backup_files(squad_path)
    results["checks"]["backup_detection"] = {
        "passed": len(backup_files) == 0,
        "files": backup_files,
        "count": len(backup_files),
    }

    # --- Check 5: ID Uniqueness ---
    duplicates = check_id_uniqueness(config)
    results["checks"]["id_uniqueness"] = {
        "passed": len(duplicates) == 0,
        "duplicates": duplicates,
        "count": len(duplicates),
    }

    # --- Check 6: Version Consistency ---
    version_issues = check_version_consistency(squad_path, config)
    results["checks"]["version_consistency"] = {
        "passed": len(version_issues) == 0,
        "issues": version_issues,
        "count": len(version_issues),
    }

    # --- Check 7: Workspace Integration Governance ---
    workspace_issues = check_workspace_integration(squad_path, config)
    results["checks"]["workspace_integration"] = {
        "passed": len(workspace_issues) == 0,
        "issues": workspace_issues,
        "count": len(workspace_issues),
    }

    # --- Summary ---
    all_checks_passed = all(
        check.get("passed", True) for check in results["checks"].values()
        if isinstance(check, dict) and "passed" in check
    )
    # Also check nested orphan_ghost sections
    og_passed = all(
        s.get("passed", True) for s in orphan_ghost_results.values()
    )

    issue_count = (
        total_orphans
        + total_ghosts
        + len(fk_issues)
        + len(backup_files)
        + len(duplicates)
        + len(version_issues)
        + len(workspace_issues)
    )

    results["summary"] = {
        "total_orphans": total_orphans,
        "total_ghosts": total_ghosts,
        "fk_violations": len(fk_issues),
        "backup_files": len(backup_files),
        "duplicate_ids": len(duplicates),
        "version_mismatches": len(version_issues),
        "workspace_issues": len(workspace_issues),
        "total_issues": issue_count,
        "status": "clean" if (all_checks_passed and og_passed) else "problems_found",
    }

    return results


# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def print_report(results: Dict[str, Any], verbose: bool = False) -> None:
    """Print human-readable report."""
    summary = results["summary"]

    print()
    print("=" * 70)
    print(f"  VALIDATE-SQUAD-CONFIG: {results['squad_name']}")
    print("=" * 70)
    print(f"  Path: {results['squad_path']}")
    print()

    # YAML Validation
    yaml_check = results["checks"]["yaml_validation"]
    if yaml_check["passed"]:
        print("  [PASS] YAML Validation: config.yaml is valid")
    else:
        print(f"  [FAIL] YAML Validation: {yaml_check['error']}")
        print()
        return

    print()

    # Orphan & Ghost Detection
    print("-" * 70)
    print("  ORPHAN & GHOST DETECTION")
    print("-" * 70)

    og_checks = results["checks"]["orphan_ghost"]
    for section_name, section in og_checks.items():
        status = "PASS" if section["passed"] else "FAIL"
        orphan_count = section["orphan_count"]
        ghost_count = section["ghost_count"]

        line = f"  [{status}] {section_name:<15} | "
        line += f"fs={section['filesystem_count']:>3} config={section['config_count']:>3} | "
        line += f"orphans={orphan_count} ghosts={ghost_count}"
        print(line)

        if orphan_count > 0 and (verbose or orphan_count <= 10):
            for orphan_id in section["orphans"]:
                print(f"         ORPHAN: {orphan_id}")
        elif orphan_count > 10:
            for orphan_id in section["orphans"][:5]:
                print(f"         ORPHAN: {orphan_id}")
            print(f"         ... and {orphan_count - 5} more (use --verbose)")

        if ghost_count > 0 and (verbose or ghost_count <= 10):
            for ghost_id in section["ghosts"]:
                print(f"         GHOST:  {ghost_id}")
        elif ghost_count > 10:
            for ghost_id in section["ghosts"][:5]:
                print(f"         GHOST:  {ghost_id}")
            print(f"         ... and {ghost_count - 5} more (use --verbose)")

    print()

    # FK Validation
    fk_check = results["checks"]["fk_validation"]
    status = "PASS" if fk_check["passed"] else "FAIL"
    print(f"  [{status}] FK Validation (archived agents): {fk_check['issue_count']} violations")
    if fk_check["issue_count"] > 0:
        for issue in fk_check["issues"]:
            print(f"         {issue['message']}")
    print()

    # Backup Detection
    backup_check = results["checks"]["backup_detection"]
    status = "PASS" if backup_check["passed"] else "FAIL"
    print(f"  [{status}] Backup Detection: {backup_check['count']} backup files")
    if backup_check["count"] > 0:
        for bf in backup_check["files"]:
            print(f"         {bf}")
    print()

    # ID Uniqueness
    id_check = results["checks"]["id_uniqueness"]
    status = "PASS" if id_check["passed"] else "FAIL"
    print(f"  [{status}] ID Uniqueness: {id_check['count']} duplicates")
    if id_check["count"] > 0:
        for dup in id_check["duplicates"]:
            print(f"         {dup['section']}: '{dup['id']}' appears {dup['count']}x")
    print()

    # Version Consistency
    ver_check = results["checks"]["version_consistency"]
    status = "PASS" if ver_check["passed"] else "FAIL"
    print(f"  [{status}] Version Consistency: {ver_check['count']} mismatches")
    if ver_check["count"] > 0:
        for issue in ver_check["issues"]:
            print(f"         {issue['file']}: {issue['message']}")

    print()

    # Workspace Integration
    ws_check = results["checks"]["workspace_integration"]
    status = "PASS" if ws_check["passed"] else "FAIL"
    print(f"  [{status}] Workspace Integration: {ws_check['count']} issues")
    if ws_check["count"] > 0:
        for issue in ws_check["issues"]:
            print(f"         {issue['field']}: {issue['message']}")

    # Summary
    print()
    print("=" * 70)
    overall_status = "CLEAN" if summary["status"] == "clean" else "PROBLEMS FOUND"
    print(f"  SUMMARY: {overall_status}")
    print(f"  Orphans: {summary['total_orphans']} | Ghosts: {summary['total_ghosts']} | "
          f"FK: {summary['fk_violations']} | Backups: {summary['backup_files']} | "
          f"Duplicates: {summary['duplicate_ids']} | Version: {summary['version_mismatches']} | "
          f"Workspace: {summary['workspace_issues']}")
    print(f"  Total issues: {summary['total_issues']}")
    print("=" * 70)
    print()


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Validate squad config.yaml integrity against filesystem",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 validate-squad-config.py squads/aiox-copy/
    python3 validate-squad-config.py squads/aiox-copy/ --verbose
    python3 validate-squad-config.py squads/aiox-copy/ --json

Checks performed:
    - Orphan detection (files not in config)
    - Ghost detection (config entries without files)
    - FK validation (archived agents)
    - Backup file detection
    - YAML syntax validation
    - ID uniqueness per section
    - Version consistency across docs

TODO (future):
    - --fix flag for auto-registration of orphans
    - Pre-commit hook integration
        """,
    )
    parser.add_argument(
        "squad_path",
        help="Path to squad directory (e.g., squads/aiox-copy/)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output including all filesystem/config IDs",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )

    args = parser.parse_args()

    squad_path = Path(args.squad_path).resolve()

    if not squad_path.exists():
        print(f"ERROR: Squad path does not exist: {squad_path}")
        sys.exit(2)

    if not (squad_path / "config.yaml").exists():
        print(f"ERROR: No config.yaml found in {squad_path}")
        sys.exit(2)

    results = validate(squad_path, verbose=args.verbose)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results, verbose=args.verbose)

    # Exit code
    if results["summary"]["status"] == "fatal":
        sys.exit(2)
    elif results["summary"]["status"] == "problems_found":
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
