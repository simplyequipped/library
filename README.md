# library

Offline library services for hosting and accessing ZIM content and other files locally.

## Features
- All services are designed to run without internet access (after content has been downloaded)
- All services are designed to run from a USB flash drive or other external drive
- Only requires Python3 and the contents of this repository (after content has been downloaded)
- Automatic selection of the appropriate kiwix-tools based on device platform (see the **kiwix-tools** section for supported platforms)

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

## Recommended Content

### Reference
| Title             | Language | Variant   | Date    | Size    | Link                                                                                            |
| ----------------- | -------- | --------- | ------- | ------- | ----------------------------------------------------------------------------------------------- |
| Wikipedia         | English  | All Maxi  | 2023-11 | 109 GB  | [Kiwix Library](https://download.kiwix.org/zim/wikipedia/wikipedia_en_all_maxi_2023-11.zim)     |
| Wiktionary        | English  | All Maxi  | 2023-10 | 60 GB   | [Kiwix Library](https://download.kiwix.org/zim/wiktionary/wiktionary_en_all_maxi_2023-10.zim)   |
| Wikiversity       | English  | All Maxi  | 2021-03 | 2.5 GB  | [Kiwix Library](https://download.kiwix.org/zim/wikiversity/wikiversity_en_all_maxi_2021-03.zim) |
| Wikibooks         | English  | All Maxi  | 2021-03 | 4.5 GB  | [Kiwix Library](https://download.kiwix.org/zim/wikibooks/wikibooks_en_all_maxi_2021-03.zim)     |
| Wikihow           | English  | Maxi      | 2023-03 | 51 GB   | [Kiwix Library](https://download.kiwix.org/zim/wikihow/wikihow_en_maxi_2023-03.zim)             |
| Gutenberg Library | English  | All       | 2023-11 | 74 GB   | [Kiwix Library](https://download.kiwix.org/zim/gutenberg/gutenberg_en_all_2023-11.zim)          |
| iFixit            | English  | All       | 2023-10 | 3 GB    | [Kiwix Library](https://download.kiwix.org/zim/ifixit/ifixit_en_all_2023-10.zim)                |

