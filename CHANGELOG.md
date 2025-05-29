# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.3] - 2025-05-29

### Added
- Signal support: Added `face_image_processed` signal that is emitted when a face image is successfully processed
- This allows applications to hook into the face processing workflow and perform custom actions

### Fixed
- Import compatibility issues

## [0.0.2] - 2025-05-27

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
