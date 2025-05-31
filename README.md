# charasort editor

This is an editor for charasort ([GitHub](https://github.com/execfera/charasort)), designed to make editing characters and filters more convenient.

## Requirements

- Python 3.X

## Usage (TBD)

This editor first take `src/js/data/YYYY-MM-DD.js` as input, then parses and seperates it into **Filters** and **Characters**. After editing, it can either modify the original file or save the changes to a new file.

### Filters Structure

```
{
    // Required
    name: string,
    key:  string,

    // Optional
    tooltip: string,
    checked: boolean,
    sub: [
        {
            name: string,
            key:  string 
        },
        ...
    ]
}
```

### Characters Structure

```
{
    name: string,
    img:  string,
    opts: {
        key: boolean | string[],
        ...
    }
}
```

- `key` in `opts` must be a subset of `key` values defined in **Filters**.
- If `key` in **Filters** includes `sub` field, then the corresponding `key` in `opts` should be a list of strings, where each string is a valid `key` from `sub`.