# Charasort Editor

A simple tool for editing [charasort](https://github.com/execfera/charasort) data files, making it easier to manage characters and filters.

## Requirements

- Python 3.8 or higher  
- Python package:
  - `calmjs.parse`

## Overview

This editor parses a JavaScript data file (typically found at `src/js/data/YYYY-MM-DD.js`) and separates it into two editable components:

- **Filters** – Used to categorize characters.
- **Characters** – The list of characters and their associated filter options.

After making edits, the modified data can either overwrite the original file or be saved to a new one.

## Data Format

### Filters

Each filter is a dictionary with the following structure:

```javascript
{
  // Required fields
  name: string,
  key: string,

  // Optional fields
  tooltip: string,
  checked: boolean,
  sub: [
    {
      name: string,
      key: string
    },
    ...
  ]
}
```

### Characters

Each character entry follows this format:

``` javascript
{
    name: string,
    img:  string,
    opts: {
        key: boolean | string[],
        ...
    }
}
```

- Each `key` in `opts` must match a corresponding `key` defined in the Filters.
- If a filter includes a `sub` field, the corresponding `opts[key]` should be a list of strings referencing valid `sub.key` values.

## Usage (TBD)
