# Changelog

## v0.1.2

### Add
- Choices for downloader.
- Call curl to download files, for better downloading experience.
- Added argument type hint for functions in `cli.py`.

### Modify
- Changed `cli.ask_parser()` to `cli.ask_module(module_path:str,module_type:str="module")`.
- Moved file downloading function `network.download()` to `downloaders.interrnal.download()`.

### Remove
- Removed `network.download_all()`, which is for testing at first and not needed anymore.

## v0.1.1

### Add
- Retry downloading a file when it fails.
- More useful logs for cli.choose_from().

### Modify
[NONE]

### Remove
[NONE]

(Or in other words, why should I remove anything at this early version?)

## v0.1.0
The first ever version of this project