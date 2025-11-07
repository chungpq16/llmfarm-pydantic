# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2024-12-19

### Added
- **NEW**: Simple direct interface (`BoschFarmLLM`) for easy usage without Pydantic AI
- Backward compatibility alias (`llmfarminf`) matching your original code structure
- Convenience methods: `ask()`, `chat()`, and `_completion()`
- Comprehensive URL construction handling for Azure OpenAI deployments

### Fixed
- **CRITICAL**: Fixed URL construction in simple interface to use proper Azure deployment paths
- Simple interface now correctly calls `/deployments/{deployment}/chat/completions`
- Proper deployment name extraction from configured URLs

### Technical Details
- Added `BoschFarmLLM` class in `src/bosch_farm_simple.py`
- Automatic URL parsing and deployment name extraction
- Compatible with various URL formats (full deployment URL, API root, trailing slashes)

## [0.1.1] - 2024-12-19

### Fixed
- **CRITICAL**: Fixed 404 "Resource not found" errors when making API calls
- Provider now correctly constructs Azure OpenAI URLs by automatically appending `/chat/completions` endpoint
- Improved URL handling for both trailing slash and non-trailing slash input URLs
- Added better debugging for URL construction

### Changed
- Enhanced provider initialization with proper URL validation
- Improved logging to show final constructed URLs for debugging

### Technical Details
- Modified `BoschFarmProvider._initialize_client()` to ensure proper endpoint URL construction
- Azure OpenAI deployments now correctly use: `{base_url}/chat/completions`
- Backward compatible - no changes required for existing code

## [0.1.0] - 2024-12-19

### Added
- Initial release of Bosch Farm Provider for Pydantic AI
- Secure configuration management with environment variables and config files
- Support for YAML and JSON configuration formats
- Custom authentication headers for Bosch Farm API
- Comprehensive test suite with mocking and integration tests
- Production-ready error handling and logging
- Complete examples and documentation

### Features
- Drop-in replacement for OpenAI providers
- Flexible configuration with multiple sources
- Corporate-ready security practices
- Well-documented API and usage patterns