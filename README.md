# 3D Texture Importer

A [Blender](https://www.blender.org) Add-on that automatically imports texture files and creates appropriate shader nodes from a given directory.

- [Setup](#setup)
- [Usage](#usage)
- [Development](#development)

## Setup

Download the "Source code (zip)" from the [latest release](https://github.com/gbaptista/blender_texture_importer/releases) and follow the [Installing Add-ons](https://docs.blender.org/manual/en/latest/editors/preferences/addons.html#installing-add-ons) sections from the Blender documentation.

## Usage

Go to the _Shading_ workspace or open a _Shader Editor_ panel in Blender. Make sure you have selected the material you want to work with.

To import a texture, right-click in the _Shader Editor_ and choose _Import Texture_. A dialog box will appear asking you to pick a directory. Once you select a folder, the add-on will scan through all image files inside and set up the required nodes for your texture.

Be aware that the process will **delete** all existing nodes. It will then automatically set up a _Principled BSDF_ shader node and connect your imported texture nodes to it, ultimately hooking everything up to a 'Material Output' node.

To tidy up your node layout after import, consider using the [_NodeRelax-Blender-Addon_](https://github.com/specoolar/NodeRelax-Blender-Addon), which can help organize your nodes neatly and save time.

## Development

```sh
pip install -r requirements-dev.txt

pycodestyle *.py

pylint *.py

pytest
```

Read Blender's [Tips and Tricks](https://docs.blender.org/api/current/info_tips_and_tricks.html) and [Gotchas](https://docs.blender.org/api/current/info_gotcha.html).

Developing inside Blender:

Go to the _Scripting_ workspace inside Blender, create a new _text data-block_, paste the following code, and press _Run Script_:

```python
init_path = '/home/your-user/blender_texture_importer/__init__.py'

exec(
    compile(open(init_path).read(), init_path, 'exec'),
    {'init_path': init_path}
)
```

Rerun the script every time you change the code: It will reload all your updated code inside Blender.
