# changelog

Every noteable change is logged here.

## v0.13.1

## v0.13.0

## v0.12.9

### Feature

* add logging to make generator more responsive (ee2a4d52c137)
* add tolerance to reduce massive linter warnings (c9728a6bad35)
* add tolerance to increase acceptable border overwriting (a4b040459be8)

### Fix

* fix double quotation linter (582e6ee85901)

## v0.12.8

## v0.12.7

### Feature

* add quotation linter (122301db5bcb)

## v0.12.6

## v0.12.5

## v0.12.4

## v0.12.3

### Feature

* shrink bounding box to the last char instead of line (684ed36e4831)

### Fix

* fix spelling error (0edff0aa74f6)

## v0.12.2

### Feature

* extend example generator (c4a7a4b23664)

## v0.12.1

### Fix

* do not sort files (f10c3feb666b)

## v0.12.0

### Feature

* add linter to validate divisions on line endings (38017a9c2f17)
* add textflow_decider to judge extracted result (4beadde399b4)

## v0.11.4

## v0.11.3

## v0.11.2

## v0.11.1

## v0.11.0

### Feature

* add bibliography validator (ca417491f3b7)

## v0.10.0

### Feature

* add links to further linter message documentation (a54a0215616d)
* add links to checkitweg docs (9cddd603181d)

### Fix

* remove unused code (1405a862a444)

### Documentation

* fix spelling errors (c62110895323)

## v0.9.0

### Feature

* add module to determine path of linter result (18aeb1176489)
* add expected and current distance in linter message (6ac72bafbc82)
* extend linter to display unused abbreviations (fe81928f3903)
* add abbreviation-text step to cli (6bfec2c0e2b1)
* add abbreviation to judge abbreviations out of text flow (a595f7b034c9)
* linter: do not describe German default abbreviations (adca5413e2e0)
* add abbreviation table judger to command line interface (a1895b668274)
* add linter to check that abbreviations are sorted alphabetically (fa0be3d22ffa)

### Documentation

* add description and todo for abbreviation-text step (a8462619b6e4)
* remove useless todo - use backlog instead (4271b9cc8da3)

## v0.8.0

### Feature

* add distance option to verify distance between object and text (0acc800ccd20)

## v0.7.3

## v0.7.2

### Feature

* add border decider to test data generator (62f2c99fc29e)

### Fix

* support small examples (f6666131164b)

## v0.7.1

### Fix

* fix loader (98c4de82db77)

## v0.7.0

### Feature

* extend linter message to include hit location (4805db04befc)
* add BoundingLocation to describe rectangles to highlight (4aadbe1e4f01)

## v0.6.1

### Fix

* move generated data to correct folder (4a5c6a4093f7)

## v0.6.0

### Feature

* add linter to verify and print hits on printing border (1a80cb813550)
* make simple error page count dependent (a34fa70af878)
* fix bounding detector (50b6b4b83976)
* use new border detection algorithm to determine border (cb1fbf7a494c)
* handle empty pages and ensure ascending page order (f6c702387385)
* add strategy to detect left right on raising edges (c108a1383d0c)
* add debugging information to verify algorithm result (87e1c6420c01)
* add method to detect left-right document border (e72400f38f75)
* return value of featurepack to caller (12d9daf7513c)
* extend tool --help documentation (1bbb0c3b2f89)
* write result of linting as border detection step output (236b016fee5c)
* add mechanism to judge equal border detection (f1b399ac5b3f)
* round border and use mode to determine border (296df6c05458)
* add --pages flag to shrink selected pages (dacf94e874b5)
* improve interface definition (d767c1f64421)
* rename border bounding detection to feature name (0b366511671b)

### Fix

* ensure that pages are sorted ascendantly (0b55c39268c9)
* determine required border depending on page number (3f58edf70a3d)
* handle None as special value (3f3653870d67)

### Documentation

* fix intention of rawmaker package (6b95f5796c15)
* extend interface documentation (b066550d719d)

## v0.5.0

### Feature

* add page validator to validate page number of document (3ab005eafa15)
* add solution to describe fixes for table of content (2eb16c69f2b5)
* add linter to verify ascending pages (3db11490e148)
* add linter to verify repeating header content (f779c0b175a6)
* add error message that template does not fit requirements (b4c9741e3dd2)
* improve solution result finder (35e95b99d104)
* extend interface to use module name directly (7d6f2e15a881)
* use automate checker to run footnote validation (cc5c57cd968c)
* add method to parse validator function (a946f168c9e4)
* add Solutions parser to ease defining SOLUTIONS (eaf45c2098ed)
* add method to verify size of foot note content (9c5a1c3d0aa4)
* add linter to verify linter font family (2b67c888c296)
* add highnote rise and size checker (10a9ec4a16af)
* add method to determine most common style of FootNotes (ec2c42ef3ada)

### Documentation

* add overview of decider features (213b855f71ec)

## v0.4.7

## v0.4.6

### Feature

* use template {%number%} to specify error message (3940f6146517)
* add feature footnotes (2ad32d25af57)

## v0.4.5

## v0.4.4

## v0.4.3

### Documentation

* Happy New Year! (131a538ea5be)

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
