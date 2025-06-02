#!/usr/bin/env python
"""
Prepare a release by updating version-dependent files.
"""

import re
import subprocess
import sys
from pathlib import Path


def get_current_version():
    """Extract the current version from pyproject.toml."""
    pyproject_path = Path("pyproject.toml")
    with open(pyproject_path) as f:
        content = f.read()

    version_match = re.search(r'version\s*=\s*"([^"]+)"', content)
    if not version_match:
        print("Error: Could not find version in pyproject.toml")
        sys.exit(1)

    return version_match.group(1)


def run_command(cmd, description):
    """Run a command and check for success."""
    print(f"Running: {description}")
    try:
        result = subprocess.run(
            cmd, shell=True, check=True, capture_output=True, text=True
        )
        print(f"✅ {description}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(e.stderr)
        sys.exit(1)


def main():
    """Prepare release by updating all version-dependent files."""
    print("🚀 Preparing release...")

    version = get_current_version()
    print(f"📦 Current version: {version}")

    # Update badge
    run_command("python scripts/update_badge.py", "Updating PyPI badge")

    # Run quality checks
    run_command("make check", "Running code quality checks")

    # Run tests
    run_command("make test", "Running tests")

    # Build package
    run_command("make build", "Building package")

    print(f"\n✅ Release v{version} is ready!")
    print("\nNext steps:")
    print("1. Update CHANGELOG.md with today's date")
    print("2. git add . && git commit -m 'release: v{version}'")
    print("3. git tag v{version} && git push origin main v{version}")


if __name__ == "__main__":
    main()
