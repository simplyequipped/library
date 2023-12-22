# library

Offline library services for locally hosting ZIM content and other files.

## Features
- All services are designed to run without internet access
- All services are designed to run from a USB flash drive or other external drive
- The only dependencies are Python3, the contents of this repository (after content has been downloaded)
- Automatic selection of the appropriate kiwix-tools based on the platform (see the **kiwix-tools** section for supported platforms)

## Services

### Reference
The *reference* service uses `kiwix-serve` to host ZIM content, and is intended for reference content such as [Wikipedia](https://library.kiwix.org/#lang=eng&category=wikipedia). ZIM files should be added to *kiwix/zim-reference* and added to the *kiwix/library_reference.xml* library file.

### Forums
The *forums* service uses `kiwix-serve` to host ZIM content, and is intended for forum content such as [StackExchange](https://library.kiwix.org/#lang=eng&category=stack_exchange). ZIM files should be added to *kiwix/zim-forum* and added to the *kiwix/library_forum.xml* library file.

### Files
The *files* service uses `python http.server` to host miscellaneous file content. Files should be added to *files/*

### Landing
The *landing* service uses a subclassed `python http.server` instance to host a landing webpage which makes navigating to the other servies easier.

## kiwix-tools

The following kiwix-tools are included in this repositiory:
- kiwix-manage
- kiwix-serve
- kiwix-search

The following platforms are supported by the included kiwix-tools:
- Windows x86
- Linux x86
- Linux ARM HF (Raspberry Pi)
- Linux ARM v6
- Linux ARM v8
- Darmin (MacOS) x86
- Darmin (MacOS) ARM
