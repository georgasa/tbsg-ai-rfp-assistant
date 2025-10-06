# Changelog

All notable changes to the TBSG AI RFP Assistant project will be documented in this file.

## [2.1.0] - 2025-10-06

### Added
- 3-API call strategy for comprehensive analysis
- Enhanced gap coverage in Details section
- Improved document structure with proper formatting
- API calls counter display in generated documents

### Changed
- Optimized RAG API calls from 2 to 3 per analysis
- Enhanced 3rd API call to cover remaining key points gaps
- Improved Details section to achieve 100% key-point coverage
- Updated project structure (removed test files and temporary documents)

### Fixed
- Double pillar title issue in Word documents
- Bold formatting rendering in generated documents
- Missing analysis for specific key points (UI components, non-cloud deployments, DR strategies)
- Bullet points format in Key-points section

### Technical Improvements
- Enhanced `rag_client.py` with 3-API call strategy
- Improved `word_generator.py` document structure
- Better error handling and debug logging
- Cleaner project structure

## [2.0.0] - 2025-10-03

### Added
- Complete UI redesign with Temenos Explorer look & feel
- RESTful API implementation
- Azure deployment support
- Professional Word document generation
- 2-API call strategy for comprehensive analysis

### Changed
- Migrated from command-line to web interface
- Enhanced document structure with Key-points and Details sections
- Improved API call optimization

## [1.0.0] - 2025-09-XX

### Added
- Initial release
- Basic pillar analysis
- Command-line interface
- JSON output only
