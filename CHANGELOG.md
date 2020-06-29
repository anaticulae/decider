# changelog

Every noteable change is logged here.

## v0.22.1

### Feature

* add physical value checker (7afffeaa9c07)

## v0.22.0

### Feature

* add some character checking steps (30c63c74799f)
* add character decider step (888ecbb345d2)

## v0.21.4

### Fix

* display font name not python repr (883f01272836)

## v0.21.3

## v0.21.2

## v0.21.1

### Fix

* fix changed font store access (4599017da358)

## v0.21.0

### Feature

* remove unnecessary list after introducing magic content (26934f4511ec)
* use general magic line look up to determine pure text lines (5e24ce4692a7)
* use magic content to exclude from text style check (2ec227b8e9ae)
* add option to yield non textual elements with none (8f3e325ca748)
* do not check paragraph length in lists (d426415748ac)

### Fix

* ensure loading empty bib reference (09fc47d53415)
* catch roman page number (52ce72518243)

## v0.20.2

### Fix

* fix Solution2005 font name error (0b744587051f)
* fix too few children validation test (e11fe91a55c2)
* fix sorting bib algorithm (43b34eb481d7)

## v0.20.1

### Fix

* fix str conversion bug (2eae7c1f0e0b)
* remove useless log (18e5fc976b29)

## v0.20.0

### Feature

* send information to use better footnote pattern (41169f3c32c2)
* disable dot and upper case checker if not wanted (77a1884fcf51)

### Fix

* fix linter warnings (7d4a8d40a0a2)
* fix flaky test cause this test modify global state (3eb619acfb84)
* do not fail on roman page numbers (4d6fcf5b8fee)

## v0.19.0

### Feature

* add outlines validator step (b86bc350dcea)
* add linter to verify max citation length (ceb10df8b3d6)
* add method to extract general marks (1fc6c6f3bc93)

### Fix

* add missing __init__ file (790630e4650c)
* catch index error, solve later (3a8cb7c594d2)

## v0.18.2

### Feature

* add strong tag to highlight extracted values (ad55d3b62c1a)

### Fix

* log error on headline access (5a0e689f9a9a)
* catch ambiguous font size rise (0469201be78b)
* ensure to have enough data (658af4e262da)
* fix missing lines template replacing (a6f70be093f7)

## v0.18.1

### Fix

* fix copy paste error (f9a9c4e9637d)

## v0.18.0

### Feature

* add checker to lint to short paragraphs (b8812e762e50)
* add linter to check that page start with text (2e2bf2a9b3a8)
* add page start/end step to detect correct page start/end (febdee210309)
* add step to lint correct using of German language (7633946c1439)

### Fix

* solve some linter warnings (d38c81df8c39)

## v0.17.0

### Feature

* add general step to judge footnotes (6cbcc1386d28)
* add toc linter to to mark wrong located `Eidesstattliche` (f7de57ee6c84)
* add linter step `chapter start not on new page` (1200b5e2e5de)
* add separate `decider_footnote` application (753ac65efe9f)

### Fix

* fix footnote linter messages (839ea794e509)

## v0.16.0

### Feature

* extend linter to display out ranged chapters (769a12088fdc)
* add toc balance extractor out of headline level (1a8d53141849)
* improve duplicated words checker (33e9b76d9ded)
* split rules by meaning into different features (dec586ea477a)
* move toc rules to separate runner `decider_toc` (ef1b2d7139c8)

### Fix

* log non existing fonts on headline validator (466e18ceaa0e)

## v0.15.5

### Fix

* add page size to analysis cause border is defined relative yet (0ef988a18d0d)

## v0.15.4

### Feature

* add text font family linter (59dd93d94141)
* add step to judge content text style (b6ab75be4e4b)

## v0.15.3

### Fix

* fix check for (pdf, page)-pattern (723fd05b6195)

## v0.15.2

### Feature

* enable selective page for every resource (431e0aaec6af)

## v0.15.1

### Feature

* add individual page selector to extend page select behavior (672d7642b0fb)

### Documentation

* extend interface documentation (542897ff480b)

## v0.15.0

### Feature

* add headline distance before and after linter (89bb8cf9d3ea)
* add headline font family validator (7a0825396423)
* add textstyle decider to example generator (7867ae90926e)
* add h2, h3 text size validator (da280331a248)
* add font style headline h1 linter (f10668fbc6e5)
* add basic textstyle cli structure and testing (557349ca9b0d)

### Fix

* verify best selection algo/parser (d530bf36cec0)
* enable master116 title page test (a2cc9cc3bdbc)

## v0.14.1

### Fix

* do not fail if raw_location was not parsed properly (c1311cc5d607)

## v0.14.0

### Feature

* round sizes to reduce probability of multiple detection (d1747bf29bee)
* add toc quotation validator (2c580e5267e6)
* add linter to mark question in table of content (c57a4c762a7f)
* add check to validate max toc length (684798afa49e)
* add linter to detect miss usage in table of content (205282780b00)
* introduce invalid toc mixin (31f4b20bdb57)
* add logging information about raised exception (6f31ac32b713)
* show missing title,toc on separate overview page (8a6d4c124a78)

### Fix

* present toc linter result to correct pdf page (c452d7f1d00d)

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
