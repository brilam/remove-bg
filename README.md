# remove-bg
A Python API wrapper for removing backgrounds from picture using [remove.bg](https://www.remove.bg)'s [API](https://www.remove.bg/api).

# License
This code is licensed under the MIT License. See [here](https://github.com/brilam/remove-bg/blob/master/LICENSE) for more details.

# Installation
`pip install removebg`

# Usage
## `remove_background_from_img_file`

Removes the background given an image file.

| Parameter     | Default Value | Description   |
| ------------- | ------------- | ------------- |
| img_file_path | req. param    | path to the source image file |
| size          | `'regular'`   | size of the output image (`'auto'` = highest available resolution, `'preview'`|`'small'`|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`|`'4k'` = original size) |
| type          | `'auto'`      | foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'car'`) |
| type_level    | `'none'`      | classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification) |
| format        | `'auto'`      | image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`) |
| roi       | `'0 0 100% 100%'` | region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%) |
| crop          | `None`        | px or relative, single val = all sides, two vals = top/bottom, left/right, four vals = top, right, bottom, left |
| scale         | `'original'`  | image scale relative to the total image size |
| position      | `'original'`  | `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical |
| channels      | `'rgba'`      | request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`) |
| shadow        | `False`       | whether to add an artificial shadow (some types aren't supported) |
| semitransparency | `True`     | semitransparency for windows or glass objects (some types aren't supported) |
| bg            | `None`        | background (`None` = no background, path, url, color hex code (e.g. `'81d4fa'`, `'fff'`), color name (e.g. `'green'`)) |
| bg_type       | `None`        | background type (`None` = no background, `'path'`, `'url'`, `'color'`) |
| new_file_name | `'no-bg.png'` | file name of the result image |

### Code Example:
```python
from removebg import RemoveBg

rmbg = RemoveBg("YOUR-API-KEY", "error.log")
rmbg.remove_background_from_img_file("joker.jpg")
```


## `remove_background_from_img_url`

Removes the background given an image URL.

| Parameter     | Default Value | Description   |
| ------------- | ------------- | ------------- |
| img_url       | req. param    | URL to the source image |
| size          | `'regular'`   | size of the output image (`'auto'` = highest available resolution, `'preview'`|`'small'`|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`|`'4k'` = original size)
| type          | `'auto'`      | foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'car'`) |
| type_level    | `'none'`      | classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification) |
| format        | `'auto'`      | image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`) |
| roi       | `'0 0 100% 100%'` | region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%) |
| crop          | `None`        | px or relative, single val = all sides, two vals = top/bottom, left/right, four vals = top, right, bottom, left |
| scale         | `'original'`  | image scale relative to the total image size |
| position      | `'original'`  | `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical |
| channels      | `'rgba'`      | request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`) |
| shadow        | `False`       | whether to add an artificial shadow (some types aren't supported) |
| semitransparency | `True`     | semitransparency for windows or glass objects (some types aren't supported) |
| bg            | `None`        | background (`None` = no background, path, url, color hex code (e.g. `'81d4fa'`, `'fff'`), color name (e.g. `'green'`)) |
| bg_type       | `None`        | background type (`None` = no background, `'path'`, `'url'`, `'color'`) |
| new_file_name | `'no-bg.png'` | file name of the result image |

### Code Example:
```python
from removebg import RemoveBg

rmbg = RemoveBg("YOUR-API-KEY", "error.log")
rmbg.remove_background_from_img_url("http://www.example.com/some_image.jpg")
```


## `remove_background_from_base64_img`

Removes the background given a base64 image string.

| Parameter     | Default Value | Description   |
| ------------- | ------------- | ------------- |
| base64_img    | req. param    | base64 image string |
| size          | `'regular'`   | size of the output image (`'auto'` = highest available resolution, `'preview'`|`'small'`|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`|`'4k'` = original size)
| type          | `'auto'`      | foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'car'`) |
| type_level    | `'none'`      | classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification) |
| format        | `'auto'`      | image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`) |
| roi       | `'0 0 100% 100%'` | region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%) |
| crop          | `None`        | px or relative, single val = all sides, two vals = top/bottom, left/right, four vals = top, right, bottom, left |
| scale         | `'original'`  | image scale relative to the total image size |
| position      | `'original'`  | `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical |
| channels      | `'rgba'`      | request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`) |
| shadow        | `False`       | whether to add an artificial shadow (some types aren't supported) |
| semitransparency | `True`     | semitransparency for windows or glass objects (some types aren't supported) |
| bg            | `None`        | background (`None` = no background, path, url, color hex code (e.g. `'81d4fa'`, `'fff'`), color name (e.g. `'green'`)) |
| bg_type       | `None`        | background type (`None` = no background, `'path'`, `'url'`, `'color'`) |
| new_file_name | `'no-bg.png'` | file name of the result image |

### Code Example:
```python
from removebg import RemoveBg
import base64

rmbg = RemoveBg("YOUR-API-KEY", "error.log")
with open("joker.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
rmbg.remove_background_from_base64_img(encoded_string)
```

# Contributions
Contributions and feature requests are always welcome.
