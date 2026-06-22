# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.2]
### Changed
- Removed raw-data worker deploy from the satellite package. The API now
  ships only the estimation secret and ``pumpwood-estimation-app``
  manifests. Updated docs, tests, and module docstrings accordingly.
