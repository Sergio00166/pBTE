# pBTE

**pBTE** (python-based Basic Text Editor) is a lightweight, cross-platform terminal editor written in Python. It minimizes external dependencies while providing essential editing features and Unicode support.

---

## Table of Contents
- [Features](#features)
- [Supported Encodings](#supported-encodings)
- [Dependencies](#dependencies)
- [Compatibility](#compatibility)
- [Usage](#usage)
- [Configuration](#configuration)
- [Keybindings](#keybindings)
  - [Main Mode](#main-mode)
  - [Open File Menu](#open-file-menu)
  - [Save As Menu](#save-as-menu)
  - [Find Menu](#find-menu)
  - [Replace Menu](#replace-menu)
- [License](#license)

---

## Features
- UTF-8, UTF-16 (LE/BE, with or without BOM), and ASCII support
- Automatic detection of file encoding and line endings
- Runtime switching of output encoding and newline style (only affects file saves)
- Clipboard operations: copy, cut, paste (line-oriented)
- Text search (`Find`) and batch replacement (`Replace`)
- Indentation, dedentation, commenting/uncommenting lines
- Go-to-line functionality
- Toggleable selection mode
- Batch cursor movements with Ctrl + arrow keys

---

## Supported Encodings
- UTF-8 (default for new files)
- UTF-16 LE/BE (with or without BOM)
- ASCII (for reading binary data)

Line endings: LF (default), CRLF, CR

---

## Dependencies
- Python 3.6+
- colorama (bundled in `lib.zip`)
- wcwidth (bundled in `lib.zip`)

Licenses for bundled libraries are included in `lib.zip`.

---

## Compatibility
Tested on:
- Windows
- Linux
- macOS

Key remapping can be configured in `bin/data.py` if needed.

---


## Usage
```
python bin/pbte.py [path/to/file]
```

- Without an argument, a new blank buffer opens (UTF-8 + LF by default).
- Use `^O` to open a file, `^S` to save, and `^A` for "Save As".

---

## Configuration
To change keyboard bindings, edit the mappings in:
```
bin/data.py
```

---

## Keybindings

### Main Mode
- `^Q`: Quit
- `^S`: Save
- `^A`: Save As
- `^O`: Open File
- `^C`: Copy
- `^X`: Cut
- `^P`: Paste
- `^G`: GOTO line
- `^I`: Indent
- `^D`: Dedent
- `^K`: Comment line
- `^U`: Uncomment line
- `^F`: Find
- `^R`: Replace
- `^J`: Insert newline without moving cursor
- `^Y`: Toggle line selection mode
- `Ctrl + Arrow Keys`: Move in steps of 4 characters
- `^T` then `S` or `L`: Change output charset or line ending

### Open File Menu
- `^C`: Exit
- `^O`: Open file
- `Tab` / `Enter`: Autocomplete filenames
- `^N`: New file

### Save As Menu
- `^C`: Exit
- `^S`: Save file
- `Tab` / `Enter`: Autocomplete filenames
- `^B`: Back up

### Find Menu
- `^C`: Exit
- `<-`: Previous match
- `->`: Next match

### Replace Menu
- `^C`: Exit
- `^A`: Replace all
- `<-`: Previous match
- `->`: Next match

---

## License
GPLv3 License. See the `LICENSE` file for details.
