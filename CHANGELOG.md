# Changelog

<!--
Release Checklist:
1. Update version in pyproject.toml
2. Run `make update-badge` (or it will run automatically with `make build`)
3. Update CHANGELOG.md with release date
4. Run `make check && make test && make build`
5. Commit, merge to main, tag, and push
-->

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.7] - 2025-06-03

### Added
- Quick registration form with improved UX
- Autocomplete support for form fields
- Clear user instructions for registration flow
- Registration link on the index page

### Changed
- Updated index page content to be more accurate
- Improved navigation and URL naming
- Fixed WSGI application path

## [0.0.6] - 2025-06-02

### Changed
- **BREAKING**: Modernized build system from setuptools to hatchling
- **BREAKING**: Minimum Python version increased to 3.9 (removed 3.8 support)
- **BREAKING**: Updated psycopg2-binary to psycopg[binary] >= 3.1.0
- Consolidated all configuration into pyproject.toml (single source of truth)
- Simplified CI/CD workflow with reduced matrix testing (focus on LTS versions)
- Updated dependencies to latest compatible versions
- Improved development workflow with uv package manager

### Removed
- setup.py (redundant with pyproject.toml)
- pytest.ini (moved to pyproject.toml)
- .coveragerc (moved to pyproject.toml)
- Bandit security scanning (focused on core linting)

### Added
- uv-based development workflow for faster dependency management
- Modern hatchling build backend
- Simplified Makefile with essential commands only
- pytest-fixturecheck integration for better test validation

### Fixed
- Python 3.13 compatibility issues with TensorFlow (pinned to 3.11 max)
- Import sorting and code formatting consistency
- Migration file linting warnings (properly excluded)

## [0.0.5] - 2025-05-30

### Changed
- CI: run pre-commit hooks only on Python files

## [0.0.4] - 2025-05-30

### Security
- Enhanced username validation in face login to prevent potential security issues
- Improved database authentication security

## [0.0.3] - 2025-05-29

### Added
- Added `face_image_processed` signal that is emitted when a face image is successfully processed
- Signal support for extending functionality when face images are saved

### Changed
- Updated dependencies to latest compatible versions
- Improved test coverage and reliability

## [0.0.0] - 2025-05-26

### Added
- Initial release
- Face recognition authentication using DeepFace
- Support for multiple face images per user
- Webcam and file upload support
- PostgreSQL with pgvector integration
- Modern Bootstrap 5 UI
- Management commands for batch face image processing
- Comprehensive test suite
- CI/CD pipeline with GitHub Actions
