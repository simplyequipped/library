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

The total size of recommended content listed below is 403 GB. See the [Kiwix Library](https://library.kiwix.org/) for more ZIM content.

### Reference ZIM Files (304 GB)
| Title              | Language | Variant   | Date    | Size    | Link                                                                                                                    |
| ------------------ | -------- | --------- | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| Wikipedia          | English  | All Maxi  | 2023-11 | 109 GB  | [Download](https://download.kiwix.org/zim/wikipedia/wikipedia_en_all_maxi_2023-11.zim)                                  |
| Wiktionary         | English  | All Maxi  | 2023-10 | 60 GB   | [Download](https://download.kiwix.org/zim/wiktionary/wiktionary_en_all_maxi_2023-10.zim)                                |
| Wikiversity        | English  | All Maxi  | 2021-03 | 2.5 GB  | [Download](https://download.kiwix.org/zim/wikiversity/wikiversity_en_all_maxi_2021-03.zim)                              |
| Wikibooks          | English  | All Maxi  | 2021-03 | 4.5 GB  | [Download](https://download.kiwix.org/zim/wikibooks/wikibooks_en_all_maxi_2021-03.zim)                                  |
| Wikihow            | English  | Maxi      | 2023-03 | 51 GB   | [Download](https://download.kiwix.org/zim/wikihow/wikihow_en_maxi_2023-03.zim)                                          |
| Gutenberg Library  | English  | All       | 2023-11 | 74 GB   | [Download](https://download.kiwix.org/zim/gutenberg/gutenberg_en_all_2023-11.zim)                                       |
| iFixit             | English  | All       | 2023-10 | 3 GB    | [Download](https://download.kiwix.org/zim/ifixit/ifixit_en_all_2023-10.zim)                                             |

### Forums ZIM Files (98 GB)
| Title              | Language | Variant   | Date    | Size    | Link                                                                                                                    |
| ------------------ | -------- | --------- | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| 3D Printing        | English  | All       | 2023-07 | 99 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/3dprinting.stackexchange.com_en_all_2023-07.zim)               |
| Astronomy          | English  | All       | 2023-05 | 155 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/astronomy.stackexchange.com_en_all_2023-05.zim)                |
| Network Eng        | English  | All       | 2023-11 | 121 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/networkengineering.stackexchange.com_en_all_2023-11.zim)       |
| Cooking            | English  | All       | 2023-11 | 217 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/cooking.stackexchange.com_en_all_2023-11.zim)                  |
| Amateur Radio      | English  | All       | 2023-11 | 65 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/ham.stackexchange.com_en_all_2023-11.zim)                      |
| Woodworking        | English  | All       | 2023-11 | 88 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/woodworking.stackexchange.com_en_all_2023-11.zim)              |
| Ubuntu             | English  | All       | 2023-11 | 2 GB    | [Download](https://download.kiwix.org/zim/stack_exchange/askubuntu.com_en_all_2023-11.zim)                              |
| Aviation           | English  | All       | 2023-05 | 384 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/aviation.stackexchange.com_en_all_2023-05.zim)                 |
| Biology            | English  | All       | 2023-05 | 351 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/biology.stackexchange.com_en_all_2023-05.zim)                  |
| Home Improvement   | English  | All       | 2023-08 | 974 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/diy.stackexchange.com_en_all_2023-08.zim)                      |
| Engineering        | English  | All       | 2023-05 | 195 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/engineering.stackexchange.com_en_all_2023-05.zim)              |
| Gardening          | English  | All       | 2023-11 | 678 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/gardening.stackexchange.com_en_all_2023-11.zim)                |
| Cartography        | English  | All       | 2023-11 | 1.2 GB  | [Download](https://download.kiwix.org/zim/stack_exchange/gis.stackexchange.com_en_all_2023-11.zim)                      |
| Sys / Net Admin    | English  | All       | 2023-11 | 1.5 GB  | [Download](https://download.kiwix.org/zim/stack_exchange/serverfault.com_en_all_2023-11.zim)                            |
| Stack Overflow     | English  | All       | 2023-11 | 75 GB   | [Download](https://download.kiwix.org/zim/stack_exchange/stackoverflow.com_en_all_2023-11.zim)                          |
| Super User         | English  | All       | 2023-11 | 2.5 GB  | [Download](https://download.kiwix.org/zim/stack_exchange/superuser.com_en_all_2023-11.zim)                              |
| Pets               | English  | All       | 2023-11 | 80 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/pets.stackexchange.com_en_all_2023-11.zim)                     |
| Physics            | English  | All       | 2023-11 | 1.4 GB  | [Download](https://download.kiwix.org/zim/stack_exchange/physics.stackexchange.com_en_all_2023-11.zim)                  |
| Robotics           | English  | All       | 2023-11 | 203 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/robotics.stackexchange.com_en_all_2023-11.zim)                 |
| Space Exploration  | English  | All       | 2023-11 | 328 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/space.stackexchange.com_en_all_2023-11.zim)                    |
| Cartography        | English  | All       | 2023-11 | 166 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/crypto.stackexchange.com_en_all_2023-11.zim)                   |
| Computer Science   | English  | All       | 2023-03 | 283 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/cs.stackexchange.com_en_all_2023-03.zim)                       |
| Martial Arts       | English  | All       | 2023-11 | 26 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/martialarts.stackexchange.com_en_all_2023-11.zim)              |
| Open Data          | English  | All       | 2023-11 | 40 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/opendata.stackexchange.com_en_all_2023-10.zim)                 |
| Electrical Eng     | English  | All       | 2023-11 | 1.5 GB  | [Download](https://download.kiwix.org/zim/stack_exchange/electronics.stackexchange.com_en_all_2023-11.zim)              |
| Parenting          | English  | All       | 2023-11 | 58 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/parenting.stackexchange.com_en_all_2023-11.zim)                |
| Android            | English  | All       | 2023-10 | 357 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/android.stackexchange.com_en_all_2023-10.zim)                  |
| Bioinformatics     | English  | All       | 2023-10 | 49 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/bioinformatics.stackexchange.com_en_all_2023-10.zim)           |
| Chemistry          | English  | All       | 2023-11 | 344 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/chemistry.stackexchange.com_en_all_2023-11.zim)                |
| Economics          | English  | All       | 2023-11 | 103 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/economics.stackexchange.com_en_all_2023-11.zim)                |
| Earth Science      | English  | All       | 2023-11 | 117 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/earthscience.stackexchange.com_en_all_2023-11.zim)             |
| Law                | English  | All       | 2023-11 | 157 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/law.stackexchange.com_en_all_2023-11.zim)                      |
| Mathematics        | English  | All       | 2023-11 | 5.4 GB  | [Download](https://download.kiwix.org/zim/stack_exchange/math.stackexchange.com_en_all_2023-08.zim)                     |
| Quantum Computing  | English  | All       | 2023-10 | 73 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/quantumcomputing.stackexchange.com_en_all_2023-10.zim)         |
| Raspberry Pi       | English  | All       | 2023-11 | 279 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/raspberrypi.stackexchange.com_en_all_2023-11.zim)              |
| Arduino            | English  | All       | 2023-05 | 231 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/arduino.stackexchange.com_en_all_2023-05.zim)                  |
| Software Eng       | English  | All       | 2023-11 | 465 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/softwareengineering.stackexchange.com_en_all_2023-11.zim)      |
| Vi and Vim         | English  | All       | 2023-11 | 78 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/vi.stackexchange.com_en_all_2023-11.zim)                       |
| Signal Processing  | English  | All       | 2023-11 | 295 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/dsp.stackexchange.com_en_all_2023-11.zim)                      |
| Unix / Linux       | English  | All       | 2023-11 | 1.2 GB  | [Download](https://download.kiwix.org/zim/stack_exchange/unix.stackexchange.com_en_all_2023-11.zim)                     |
| Car Mechanics      | English  | All       | 2023-11 | 276 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/mechanics.stackexchange.com_en_all_2023-11.zim)                |
| Philosophy         | English  | All       | 2023-11 | 155 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/philosophy.stackexchange.com_en_all_2023-11.zim)               |
| Statistics         | English  | All       | 2023-11 | 1.2 GB  | [Download](https://download.kiwix.org/zim/stack_exchange/stats.stackexchange.com_en_all_2023-11.zim)                    |
| Writing            | English  | All       | 2023-11 | 95 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/writers.stackexchange.com_en_all_2023-11.zim)                  |
| Sustainable Living | English  | All       | 2023-11 | 26 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/sustainability.stackexchange.com_en_all_2023-11.zim)           |
| Data Science       | English  | All       | 2023-11 | 249 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/datascience.stackexchange.com_en_all_2023-10.zim)              |
| Outdoors           | English  | All       | 2023-11 | 130 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/outdoors.stackexchange.com_en_all_2023-11.zim)                 |
| Reverse Eng        | English  | All       | 2023-11 | 105 MB  | [Download](https://download.kiwix.org/zim/stack_exchange/reverseengineering.stackexchange.com_en_all_2023-11.zim)       |
| AI                 | English  | All       | 2023-11 | 90 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/ai.stackexchange.com_en_all_2023-10.zim)                       |
| Health             | English  | All       | 2023-11 | 57 MB   | [Download](https://download.kiwix.org/zim/stack_exchange/health.stackexchange.com_en_all_2023-05.zim)                   |

### Files (1 GB)
| Title              | Language | Variant   | Date    | Size    | Link                                                                                                                    |
| ------------------ | -------- | --------- | ------- | ------- | ----------------------------------------------------------------------------------------------------------------------- |
| Ubuntu v22.04 ISO  | English  | Linux     | 2023-12 | 5 GB    | [Download](https://releases.ubuntu.com/22.04.3/ubuntu-22.04.3-desktop-amd64.iso)                                        |
| Digirig Driver     | English  | Windows   | 2023-12 | 0.3 MB  | [Download](https://www.silabs.com/documents/public/software/CP210x_Universal_Windows_Driver.zip)                        |
| Digirig Driver     | English  | MacOS     | 2023-12 | 2 MB    | [Download](https://www.silabs.com/documents/public/software/Mac_OSX_VCP_Driver.zip)                                     |
| Chirp-Next         | English  | Windows   | 2023-12 | 28 MB   | [Download](https://trac.chirp.danplanet.com/chirp_next/next-20231220/chirp-next-20231220-installer.exe)                 |
| Chirp-Next         | English  | MacOS     | 2023-12 | 38 MB   | [Download](https://trac.chirp.danplanet.com/chirp_next/next-20231220/chirp-next-20231220.app.zip)                       |
| Chirp-Next         | English  | Python    | 2023-12 | 2 MB    | [Download](https://trac.chirp.danplanet.com/chirp_next/next-20231220/chirp-20231220-py3-none-any.whl)                   |
| JS8Call v2.2.0     | English  | Windows   | 2023-12 | 20 MB   | [Download](http://files.js8call.com/2.2.0/js8call-2.2.0-win32.exe)                                                      |
| JS8Call v2.2.0     | English  | MacOS     | 2023-12 | 14 MB   | [Download](http://files.js8call.com/2.2.0/js8call-2.2.0-Darwin.dmg)                                                     |
| JS8Call v2.2.0     | English  | Linux     | 2023-12 | 14 MB   | [Download](http://files.js8call.com/2.2.0/js8call_2.2.0_i386.deb)                                                       |
| JS8Call v2.2.0     | English  | Rasp. Pi  | 2023-12 | 11 MB   | [Download](http://files.js8call.com/2.2.0/js8call_2.2.0_armhf.deb)                                                      |
| WSJT-X v2.6.1      | English  | Windows   | 2023-12 | 27 MB   | [Download](https://wsjt.sourceforge.io/downloads/wsjtx-2.6.1-win32.exe)                                                 |
| WSJT-X v2.6.1      | English  | MacOS     | 2023-12 | 27 MB   | [Download](https://wsjt.sourceforge.io/downloads/wsjtx-2.6.1-Darwin.dmg)                                                |
| WSJT-X v2.6.1      | English  | Linux     | 2023-12 | 17 MB   | [Download](https://wsjt.sourceforge.io/downloads/wsjtx_2.6.1_amd64.deb)                                                 |
| WSJT-X v2.6.1      | English  | Rasp. Pi  | 2023-12 | 11 MB   | [Download](https://wsjt.sourceforge.io/downloads/wsjtx_2.6.1_armhf.deb)                                                 |
| WSJT-X User Guide  | English  | Windows   | 2023-12 | 4 MB    | [Download](https://wsjt.sourceforge.io/wsjtx-doc/wsjtx-main-2.6.1.pdf)                                                  |
| JS8Call Guide      | English  | --        | 2023-12 | 2 MB    | [Download](https://docs.google.com/document/d/159S4wqMUVdMA7qBgaSWmU-iDI4C9wd4CuWnetN68O9U/edit?usp=sharing)            |
| Firefox Portable   | English  | Windows   | 2023-12 | 122 MB  | [Download](https://portableapps.com/apps/internet/firefox_portable)                                                     |
| Bible Portable     | English  | Windows   | 2023-12 | 31 MB   | [Download](https://portableapps.com/apps/education/bpbible_portable)                                                    |
| VLC Portable       | English  | Windows   | 2023-12 | 41 MB   | [Download](https://portableapps.com/apps/music_video/vlc_portable)                                                      |
| Notepad++ Portable | English  | Windows   | 2023-12 | 7 MB    | [Download](https://portableapps.com/apps/development/notepadpp_portable)                                                |
| GIMP Portable      | English  | Windows   | 2023-12 | 212 MB  | [Download](https://portableapps.com/apps/graphics_pictures/gimp_portable)                                               |
| Audacity Portable  | English  | Windows   | 2023-12 | 24 MB   | [Download](https://portableapps.com/apps/music_video/audacity_portable)                                                 |
| LibreOffice Portable | English  | Windows | 2023-12 | 197 MB  | [Download](https://portableapps.com/apps/office/libreoffice_portable)                                                   |
| Eraser Portable    | English  | Windows   | 2023-12 | 1 MB    | [Download](https://portableapps.com/apps/security/eraser-portable)                                                      |
| 7-Zip Portable     | English  | Windows   | 2023-12 | 3 MB    | [Download](https://portableapps.com/apps/utilities/7-zip_portable)                                                      |
| BalenaEtcher Portable | English | Windows | 2023-12 | 131 MB  | [Download](https://portableapps.com/apps/utilities/balenaetcher-portable)                                               |

## Attribution

Kiwix tools and the linked ZIM libraries are provided by the [Kiwix Association](https://kiwix.org).
