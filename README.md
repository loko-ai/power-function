# Import and use additional python libraries in LOKO

_power-function_ is LOKO extension that allows arbitrary python libraries to get imported and used in low code blocks.
The extension comes with numpy and pandas pre-installed available as "np" and "pd" respectively.

To add a new library edit the _imports.json_ file to add the import and alias used and add the library to requirements.txt.

The default content of the _import_json_ file is this:

```json
{
  "pd": "pandas",
  "np": "numpy"
}
```

Where they keys of this json file represent the alias name that you will later use as reference name in the block code, and the values are the name of the library itself. So if you want to call pandas in your code without using the alias, you will have to write something like this:


```json
{
  "pandas": "pandas",
  "np": "numpy"
}
```