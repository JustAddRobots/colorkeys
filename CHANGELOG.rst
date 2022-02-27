Changelog
=========

0.13.0 (2022-02-27)
-------------------
- ISSUE-163: Fixed usage whitespace. (4d21669) [Roderick Constance]
- ISSUE-163: Updated usage, example, added demo video. (17c4f11) [Roderick Constance]

0.12.0 (2022-02-27)
-------------------
- Stage: Changed channel_axis back to multichannel for older scikit version. (91b1b47) [Roderick Constance]
- Stage: Switched transform.rescale() kwargs order "channel_axis" (3cebe98) [Roderick Constance]
- Stage: Moved matplotlib to conditional import for non-AWS. (37a06c2) [Roderick Constance]
- Stage: Moved matplotlib backened to fix qt binding error after pyplot import. (bbc7b0e) [Roderick Constance]
- ISSUE-158: Added /tmp/colorkeys subdir to unark function. (1377798) [Roderick Constance]
- ISSUE-158: Fixed get_epoch_seconds. (0d5a042) [Roderick Constance]
- ISSUE-158: Added cpu, memory, epoch_seconds for task_arn. (3a2cf80) [Roderick Constance]
- ISSUE-158: Removed imagepath module, filepath replaces it. (cb44144) [Roderick Constance]
- ISSUE-158: Changed imagepath tests to filepath. (5599c85) [Roderick Constance]
- ISSUE-158: Fixed random blake2b hash generation. (07dc107) [Roderick Constance]
- ISSUE-158: Added JSON export. (3fdabfe) [Roderick Constance]
- ISSUE-154: Added channel_axis to image rescale. (f84a8be) [Roderick Constance]
- ISSUE-154: Switched to standardised debug-api logger. (de4097e) [Roderick Constance]
- ISSUE-154: Removed deprecated "multichannel" for rescale, fixed comments. (963fef6) [Roderick Constance]
- ISSUE-154: Added PyQt5 backend for pyplot. (aee56e6) [Roderick Constance]
- ISSUE-133: Added comments, docstrings, changed imagepath -> filepath. (c19b760) [Roderick Constance]
- ISSUE-133: Renamed ckdb->colordb. (61ca188) [Roderick Constance]
- ISSUE-133: Renamed ckdb -> colordb. (05b0a94) [Roderick Constance]
- ISSUE-133: Replaced pprint with pformat for logger. (10b22fb) [Roderick Constance]
- ISSUE-133: Added Decimal conversion from dynamodb. (b23318a) [Roderick Constance]
- ISSUE-133: Added xor_group, mean/std analytics, back to engcommon@main. (ee13d2b) [Roderick Constance]
- ISSUE-133: Updated for logger_noformat. (a117f75) [Roderick Constance]
- ISSUE-133: Added setting debug_api loglevels, updated to engcommon@dev. (1c90fec) [Roderick Constance]
- ISSUE-142: Removed dbquery, dbloader after ckdb converge. (cf8595e) [Roderick Constance]
- ISSUE-142: Fixed push_item exeception handling for duplicates. (3dd6f1e) [Roderick Constance]
- ISSUE-142: Condensed db subcommands into single module. (36e2c0f) [Roderick Constance]
- ISSUE-134: Fixed miscellaneous for dbquery. (8884399) [Roderick Constance]
- ISSUE-134: Added precommit install, fixed whitespace. (eed6207) [Roderick Constance]
- ISSUE-134: Added dbloader and dbquery. (1a0c458) [Roderick Constance]
- ISSUE-134: Fixed wrong method name. (6aad579) [Roderick Constance]
- ISSUE-134: Readded get_timestamp. (954ba61) [Roderick Constance]
- ISSUE-134: Added DynamoDB loader, renamed codecjson. (f722700) [Roderick Constance]
- ISSUE-134: Updated for pre-commit fixes. (8030526) [Roderick Constance]
- ISSUE-134: Added generic filepath, local dynamodb loader. (9453a02) [Roderick Constance]

0.11.10 (2022-02-15)
--------------------
- Stage: Updated for stage-colorkeys-tmp bucket rename. (2d758e4) [Roderick Constance]

0.11.9 (2021-07-09)
-------------------
- Stage: Added tag hash to build output artifact for later use. (719bc9d) [Roderick Constance]
- ISSUE-130: Added boto3 to setup.py. (a0bfb0c) [Roderick Constance]

0.11.8 (2021-06-12)
-------------------
- Stage: Migrated terraform to its own separate repo. (54fcbb5) [JustAddRobots]
- Stage: Changed separators for better visibility. (3f2c648) [JustAddRobots]
- Stage: Updated TODO, added main.tf in root dir. (ab65118) [JustAddRobots]
- Stage: Added CodePipeline "load" stage. (d8e7e91) [JustAddRobots]
- Stage: Added run stage fixes. (a96192f) [JustAddRobots]
- Stage: Added codepipeline "run" stage to terraform. (7b7d2dd) [JustAddRobots]
- Stage: Added run stage to codepipeline. (3e14f9b) [JustAddRobots]
- Stage: Figuring out mod deps. (1074a04) [JustAddRobots]
- ISSUE-127: Updated ECR repo for buildspec. (70d2d78) [JustAddRobots]
- ISSUE-127: Fixed vars/tags symlinks, buildspec for ECR_REPO. (b6365fa) [JustAddRobots]
- ISSUE-127: Updated for CodeBuild git full clone. (c187966) [JustAddRobots]

0.11.7 (2021-05-19)
-------------------
- ISSUE-124: Converted hist_centroids to list of dicts. (0d77feb) [JustAddRobots]

0.11.6 (2021-05-16)
-------------------
- Stage: Added COLORSPACES ENV VAR. (9823ac7) [JustAddRobots]
- ISSUE-118: Cleaned up added comments. (5891c85) [JustAddRobots]
- ISSUE-118: Updated for separated img and hist colorspaces. (a2d67b5) [JustAddRobots]
- ISSUE-118: Moved figure_size, figure_name to render module. (39f8ab1) [JustAddRobots]
- ISSUE-118: Refactored for 1 histogram per colorkey. (7c42d1d) [JustAddRobots]

0.11.5 (2021-05-11)
-------------------
- ISSUE-062: Removed extra json.dumps(), renamed vars. (8c898e6) [JustAddRobots]

0.11.4 (2021-05-08)
-------------------
- Stage: Updated to use task_hash, basename.ext of file. (d5d3b30) [JustAddRobots]
- ISSUE-062: Fixed bumpme.sh for changelog release. (bad82b8) [JustAddRobots]
- ISSUE-062: Added blake2b, task_arn in JSON, ISO-8601 timestamp. (f21f259) [JustAddRobots]

0.11.3 (2021-05-05)
-------------------
- Stage: Added comments to aws module. (a5090e9) [JustAddRobots]
- Stage: Removed json dumps indent (was spawning pprint) (afe4213) [JustAddRobots]
- Stage: Added zipfile close() before s3 upload. (d1cd1a9) [JustAddRobots]
- Stage: Added BytesIO seek for S3 zipfile upload. (888a826) [JustAddRobots]
- Stage: Removed manual close() of zipfile. (8a781d5) [JustAddRobots]
- Stage: Fixed write mode for ZipFile. (879b987) [JustAddRobots]
- Stage: Fixed ZipFile typo, shortened jsonfile hash. (2a13c91) [JustAddRobots]
- Stage: Removed unnecessary @property from method. (7b5e8d4) [JustAddRobots]
- Stage: Fixed task_desc resolution. (4c14036) [JustAddRobots]
- Stage: Fixed AWS naming convention. (9c7da99) [JustAddRobots]
- Stage: Removed unnecessary container ARN bits. (d43f720) [JustAddRobots]
- Stage: Added cluster option to task description detection. (6edc7fa) [JustAddRobots]
- Stage: Fixed data type for getting task description. (12ce456) [JustAddRobots]
- Stage: Fixed typo. (7d843a6) [JustAddRobots]
- Stage: Added exception handling, exit(1) for console_scripts. (3b8e84e) [JustAddRobots]
- Stage: Added AWS var to Dockerfile, changed from container to task arn. (1b943bc) [JustAddRobots]
- ISSUE-109: Added aws class for container/task detection. (3fa0186) [JustAddRobots]
- ISSUE-106: Added bump2version dev tag. (73325e5) [JustAddRobots]

0.11.2 (2021-05-01)
-------------------
- Stage: Added python requires >=3.6 to setup.py. (31492cf) [JustAddRobots]
- ISSUE-062: Updated buildspec to use stage tag, artifact. (13779c6) [JustAddRobots]
- ISSUE-101: Added S3 bucket tarball handling. (c2f68a1) [JustAddRobots]

0.11.0 (2021-04-28)
-------------------
- ISSUE-101: Added S3 bucket tarball handling. (b16ea86) [JustAddRobots]

0.10.1 (2021-04-28)
-------------------
- Stage: Removed sort_dicts for pprint, python < 3.8. (1e7342a) [JustAddRobots]
- ISSUE-062: Re-added $DEFAULT docker push, added bzip2 for img tarballs. (9c51706) [JustAddRobots]

0.10.0 (2021-04-26)
-------------------
- ISSUE-094: Added img.shape to createjson. (6a2731d) [JustAddRobots]
- ISSUE-090: Fixed tar archive extraction, added comments. (997865e) [JustAddRobots]
- ISSUE-090: Added image tarball handling. (786c965) [JustAddRobots]
- ISSUE-089: Changed default algo from kmeans to mbkmeans. (e59b315) [JustAddRobots]
- ISSUE-089: Removed alpha-blending to simply disregard channel. (4b77ae2) [JustAddRobots]
- ISSUE-089: Added alpha conversion for scikit imread() (07dd39e) [JustAddRobots]
- ISSUE-062: Changed HASHLONG/SHORT to just HASH. (c72b237) [JustAddRobots]
- ISSUE-062: Fixed YAML colon + space syntax. (e6212fe) [JustAddRobots]
- ISSUE-062: Fixed buildspec var exports. (30d2c25) [JustAddRobots]
- ISSUE-062: Added AWS CodeBuild buildspec. (b7771bf) [JustAddRobots]

0.9.0 (2021-04-22)
------------------
- ISSUE-082: Added docstrings to createjson. (a0d6959) [JustAddRobots]
- ISSUE-070: Added MiniBatchKMeans (mbkmeans) as algorithm. (1c1c242) [JustAddRobots]
- ISSUE-070: Added MiniBatchKMeans (mbkmeans) as algorithm. (123aaed) [JustAddRobots]

0.8.0 (2021-04-21)
------------------
- ISSUE-075: Cleaning up pre-commit, matplotlib debug logger. (9ca807d) [JustAddRobots]
- ISSUE-075: Unpinned setup.py versions. (4b38885) [JustAddRobots]
- ISSUE-075: Added debug_api CLI option. (2506736) [JustAddRobots]
- ISSUE-061: Added setup.py versions, updated Dockerfile/Makefile. (17cce69) [JustAddRobots]
- ISSUE-061: Removed commented-out cv2, fixed comments. (3006d9a) [JustAddRobots]
- ISSUE-061: Removed cv2 calls. (c47688a) [JustAddRobots]
- ISSUE-061: Updated Dockerfile for centos7 tests. (6e5d5b6) [JustAddRobots]
- ISSUE-061: Updated Dockerfile for build tests. (df9fd93) [JustAddRobots]
- ISSUE-061: Added Makefile stub for Docker build. (c07cee8) [JustAddRobots]
- ISSUE-061: Added Dockerfile. (c11bd51) [JustAddRobots]
- ISSUE-060: Refactored object compile JSON encode, added stopwatch. (11b9848) [JustAddRobots]
- ISSUE-060: Fixed help messages, tweaked plot display options. (ca615c4) [JustAddRobots]
- ISSUE-060: Added JSON encoding output. (e983c0c) [JustAddRobots]
- ISSUE-062: Fixed hist centroids sorting. (662ffba) [JustAddRobots]
- ISSUE-062: Changed hist centroids dict sort reverse. (636c288) [JustAddRobots]
- ISSUE-062: Refactored for hist_centroids and public hist_bar generation. (c391d45) [JustAddRobots]
- ISSUE-062: Added hist.centroids to stdout, fixed comments. (9f6bdc4) [JustAddRobots]

0.7.0 (2021-04-15)
------------------
- ISSUE-056: Added URL as image source. (2395559) [JustAddRobots]

0.6.0 (2021-04-14)
------------------
- ISSUE-038: Cleaned up commented code. (7ffa55f) [JustAddRobots]
- ISSUE-038: Fixed typo in package name. (351bfc1) [JustAddRobots]
- ISSUE-038: Added ffmpeg-python to setup.py. (b41dd22) [JustAddRobots]
- ISSUE-038: Replaced ffmpeg with ffmpeg-python bits. (527ff54) [JustAddRobots]
- ISSUE-038: Added ffmpeg check to filmstrip. (0a91428) [JustAddRobots]

0.5.4 (2021-04-11)
------------------
- ISSUE-039: Added comments, fixed docstrings, cleaned up. (690b53b) [JustAddRobots]
- ISSUE-039: Fixed image file globbing, added comments, fixed tests. (4d9bb31) [JustAddRobots]
- ISSUE-039: Simplified image file globbing with pathlib. (236e320) [JustAddRobots]
- ISSUE-039: Flattened nested Hist ["algo"]["cs"] to ["algo_cs"] (f4f81b9) [JustAddRobots]
- ISSUE-039: Fixed image file path resolution. (384baa8) [JustAddRobots]

0.5.3 (2021-03-12)
------------------
- ISSUE-042: Added scikit-image to setup.py. (5e09d62) [JustAddRobots]
- ISSUE-039: Added more fstrings. (784903d) [JustAddRobots]
- ISSUE-039: Testing fstrings replacement. (af9414b) [JustAddRobots]
- ISSUE-038: Added docstrings. (f22ab4b) [JustAddRobots]
- ISSUE-038: Added basic frame extraction. (7199809) [JustAddRobots]

0.5.2 (2021-02-16)
------------------
- ISSUE-033: Update README. (d53a9a5) [JustAddRobots]
- ISSUE-033: Added header image. (938a0b6) [JustAddRobots]

0.5.1 (2021-02-16)
------------------
- ISSUE-011: Updated docstrings, added imagepath pytest. (942c3d6) [JustAddRobots]
- ISSUE-011: Disabled HAC algorithm (too slow) (6fb26fc) [JustAddRobots]

0.5.0 (2021-02-15)
------------------
- ISSUE-011: Removed diff patch bits. (a71ac88) [JustAddRobots]
- ISSUE-025: Fixed multiple file handing, added non-blocking plot exit. (e73de4f) [JustAddRobots]
- ISSUE-025: Added basename extraction for figure title. (06b7dde) [JustAddRobots]
- ISSUE-025: Added multiple file handling. (8376b98) [JustAddRobots]
- ISSUE-025: Added NearestCentroid for AgglomerativeClustering. (fca008d) [JustAddRobots]

0.4.0 (2021-02-12)
------------------
- ISSUE-007: Fixed HSV histogram bar generation. (69cffb8) [JustAddRobots]
- ISSUE-007: Added HSV conversion, palette handling. (30f6357) [JustAddRobots]

0.3.0 (2021-02-11)
------------------
- ISSUE-020: Refactored Hist as derived from Clust. (2b39237) [JustAddRobots]
- ISSUE-020: Refactored Hist as derived from Clust. (c3980b5) [JustAddRobots]

0.2.0 (2021-02-08)
------------------
- ISSUE-017: Changed color to American spelling, fixed typos. (7b0a4f8) [JustAddRobots]
- ISSUE-017: Removed DP/colorist references, no github font sizing. (155066d) [JustAddRobots]
- ISSUE-017: Added more readme fixes. (8df6ea6) [JustAddRobots]
- ISSUE-017: Fixed DP captioning, other misc. (f895263) [JustAddRobots]
- ISSUE-017: Added readme bits. (1b1d6ac) [JustAddRobots]
- ISSUE-015: Added docstrings/comments. (4fc6a37) [JustAddRobots]
- ISSUE-013: Added unit tests and fixtures. (c951b52) [JustAddRobots]
- ISSUE-011: Updated after successful RGB, K-Means testing. (f12cca0) [JustAddRobots]
- ISSUE-008: Added pre-commit bits, flake8. (0cfc2af) [JustAddRobots]
- ISSUE-006: Refactored, added classes, added HSV, HCA. (47d9da2) [JustAddRobots]
- ISSUE-004: Tested in venv, started palette layout fix. (5e20249) [JustAddRobots]
- ISSUE-004: Added testvar import. (24ffdf4) [JustAddRobots]
- ISSUE-004: Added prefix for engcommon compatibility. (d369058) [JustAddRobots]
- ISSUE-004: Readded logid for engcommon compatibility. (5e19451) [JustAddRobots]
- ISSUE-004: Fixed typo (need to add flake8) (90a8ad2) [JustAddRobots]
- ISSUE-004: Fixed cv2 import. (44d7936) [JustAddRobots]

0.1.0 (2021-02-01)
------------------
- ISSUE-001: Adding pkg bits after successful test. (3c93280) [JustAddRobots]
- ISSUE-001: Added basic image manipulation cluster tests. (212aa5f) [JustAddRobots]
- ISSUE-001: Added basic repo bits. (4fca487) [JustAddRobots]
- Initial commit. (9af23c0) [JustAddRobots]
