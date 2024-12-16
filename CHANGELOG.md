# Changelog

The changes to this project will be documented in this file.

## [3.0.0] - 2024-12-16

- Initial Milestone 4 Release

### Added

- Unit tests for all the functions required to run the analysis. 
  - The tests are in the `tests` folder.
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/tree/main/tests>
  - Pull Requests:
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/57>
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/69> 
  - This change was required by milestone 4.

- Added a Make to the Docker environment.
  - Pull Requests:
  - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/73
 
- Added a Makefile script to run the analysis pipeline
  - Pull Requests:
  - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/58
    
### Changed

- Exported the scripts to run the analysis into functions.
  - Note: Many of the functions were initially written in function format, and did not start out as scripts.
  - Pull Requests:
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/41> 
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/27>
  - This change was required by milestone 4.

- READEME.md reproducibility sequence
  - Added Makefile support
  - Badges for correctly built images
  - Corrected instructions sequence and command line consistency
  - Pull request:
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/77
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/71

- Fixed bugs `run_validation.py` where it's unable to run due to missing folder structures. Removed unnecessary click commands. 
  - Pull requests:
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/72

### Fixed

- Fixed the issues with the README.md file:
  - Added a summary that includes a high-level interpretation of analysis findings and what the findings might mean.
  - Added link to the project dependencies.
  - Improved instructions on how to run the analysis.
  - README.md file:
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/blob/main/README.md>
  - Pull requests:
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/50/> 
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/71> 
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/55>
    - <https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/77>
  - This change was a fix to the issues mentioned in Milestone 1 feedback about the missing summary, dependencies, and straightforward instructions on how to run the analysis.

- Fixed environment.yml file to include the versions of the packages used, as well as using = for reproducibility.
  - environment.yml file:
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/blame/main/environment.yml
  - This change fixes the issues mentioned in Milestone 1 feedback about versions that are missing from environment files, as well as using >= instead of = in the file.

- Fixed the tables in tables to not be raw code results, and added table labeling.
  - Fixed tables:
    - https://ubc-mds.github.io/DSCI_522_Group36_taxi_fare_predictor/yellow_taxi_analysis.html
  - This changes fixes the issues mentioned in Milestone 1 feedback about the tables being raw code results and not having table labeling.

- Fix the references so that 2 references don't look like they're combined into 1 reference
  - Fixed references:
    - https://ubc-mds.github.io/DSCI_522_Group36_taxi_fare_predictor/yellow_taxi_analysis.html#references 
  - This change fixes the issues mentioned in Milestone 1 feedback about 2 references looking like they are combined into 1 big reference.

- Fixed GitHub Pages not showing correct images. 
  - Addressed to Adrian's comment's on the same peer review issue. (Comment 2) https://github.com/UBC-MDS/data-analysis-review-2024/issues/16#issuecomment-2537876330
  - Pull request:
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/66/files

- Fixed to pin Dockerfile base image version (tag) and add a step to the docker-publish.yml workflow so that it automatically updates the docker-compose.yml file with the tag of the new image that is built and published
  - This change fixes the issues mentioned in Milestone 2 feedback about Dockerfile base image version (tag) was not pinned
  - Fixed Docker files:
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/blob/main/docker-compose.yml
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/blob/main/.github/workflows/docker-publish.yml
   
- Moved around files in the repository to make it more organized.
  - Pull request:
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/49
    - https://github.com/UBC-MDS/DSCI_522_Group36_taxi_fare_predictor/pull/71
  - This change was a fix to the issues mentioned in Milestone 1 feedback that "Having too many files in the project root makes the project organization less understandable." and Adrian's comment's on the peer review issue that "The organization of the folders is a bit messy and hard to navigate.". (Comment 1) https://github.com/UBC-MDS/data-analysis-review-2024/issues/16#issuecomment-2537876330

## [2.0.0] - 2024-12-08

### Added

- Initial Milestone 3 Release

## [1.0.0] - 2024-11-30

### Added

- Initial Milestone 2 Release

## [0.0.1] - 2024-11-23

### Added

- Initial Milestone 1 Release
