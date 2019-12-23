# changelog

Every noteable change is logged here.

## v0.4.2

## v0.4.1

### Feature

* use multiprocessing to improve decision speed (fb95208aff29)

## v0.4.0

### Feature

* add first draft for page order validator (5e899912d02e)
* add toc working step (cb03d76d84a9)
* forward validated results to linter (aa701f9eaee5)
* summarize validation result (760cdd7e0b37)
* add validator to validate toc level and toc children count (381234023cdd)
* add linter to validate table of content (0629299a91b8)
* add missing title page checker (31b8e6b81c3c)
* automate test data creation (280c14a7afb8)

## v0.3.2

### Feature

* add PROCESS-name to public API (ca5c44482ee9)

## v0.3.1

## v0.3.0

### Feature

* add public API and cleanup cli (1a6bb683784f)
* add 3 checks to titlepage linter (2e3df12953c9)
* add feature `titlepage` to lint errors in `TitlePage`-extraction (13026bbaceb7)

### Fix

* rename source file (5eff1a51c69e)
* fix outdated import (777f73645a59)

## v0.2.6

## v0.2.5

## v0.2.4

## v0.2.3

## v0.2.2

## v0.2.1

### Fix

* fix bounding box detection after changing `Border`-order (086762000594)

## v0.2.0

### Feature

* add test data provider and rawmaker for dynamic test data (e63ec54d2b0e)

## v0.1.9

## v0.1.8

## v0.1.7

### Fix

* fix input to new rawmaker naming (7651d41e4317)

## v0.1.6

## v0.1.5

### Documentation

* extend readme with basic information (5b02bd341886)

## v0.1.4

## v0.1.3

### Feature

* include process name to result filename (7d8754f9e56e)
* add feature to detect ugly fonts and warn user of using it (3b59e46dd841)

### Fix

* add missing __init__ into fonts package (4c0f237fdf01)
* use correct PROCESS_NAME and remove unused code (f1b8d359d0d6)

## v0.1.2

### Feature

* use new saveme-wrapper form utila (53abf71f6ff6)

### Fix

* fixed crashed version id (3c31763bd41a)
* remove slash error introduces while refactoring (f2ad074ecdc2)

## v0.0.2

### Fix

* support single return value (f76cc45016a6)

## v0.0.1

### Feature

* dump hits to yaml to display the in `feedback` (101f89f2518f)
* filter pages without border - ignore None entries (6f96e6b4a267)
* extend interface - load page border form source (c28d125b4fa4)
* add border judger to verify that object violates page border (7d385322f9cd)
* add mechanism simply add data flow from source to dest (5778a4070bcd)
* add basic `decider_border` package (12bc8ceac960)

### Fix

* determine hits for given page, not for whole feature list (ddd49b972337)
* use test data with correct order of x0,y0,x1,y1 (4a792c2a260d)
* add missing reference to test data (6731b18f1ac1)
* run border when running __main__ manually (62e795349565)

## v0.0.0 Initial release
