# remove-bg

A Python API wrapper for removing backgrounds from picture using [remove.bg](https://www.remove.bg)'s [API](https://www.remove.bg/api).

## License

Licensed under the MIT License. See the [LICENSE](https://github.com/brilam/remove-bg/blob/master/LICENSE) file for details.

## Installation

```bash
pip install removebg
```

## Usage

### `remove_background_from_img_file`

Removes the background given an image file.

| Parameter     | Default Value | Description   |
| ------------- | ------------- | ------------- |
| timeout       | `30`          | request timeout in seconds (optional, set when creating `RemoveBg`) |
| img_file_path | req. param    | path to the source image file |
| size          | `'regular'`   | size of the output image (`'auto'` = highest available resolution, `'preview'`\|`'small'`\|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`\|`'4k'` = original size) |
| type          | `'auto'`      | foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'animal'`, `'car'`, `'car_interior'`, `'car_part'`, `'transportation'`, `'graphics'`, `'other'`) |
| type_level    | `'none'`      | classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification) |
| format        | `'auto'`      | image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`) |
| roi       | `'0 0 100% 100%'` | region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%) |
| crop          | `None`        | crop margin (px or relative). Enables cropping when set. |
| scale         | `'original'`  | image scale relative to the total image size |
| position      | `'original'`  | `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical |
| channels      | `'rgba'`      | request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`) |
| shadow        | `False`       | whether to add an artificial shadow (some types aren't supported) |
| semitransparency | `True`     | semitransparency for windows or glass objects (some types aren't supported) |
| bg            | `None`        | background path / url / color hex (`'81d4fa'`, `'fff'`) / color name (`'green'`) when `bg_type` provided |
| bg_type       | `None`        | background kind (`'path'`, `'url'`, `'color'`) |
| new_file_name | `'no-bg.png'` | file name of the result image |
| return_bytes  |  `'return_bytes'` | return raw image bytes (for service integration) |

#### Code Example (URL)

```python
from removebg import RemoveBg

rmbg = RemoveBg("YOUR-API-KEY", "error.log", timeout=15)
rmbg.remove_background_from_img_file("joker.jpg")

# for new_file_name:
rmbg.remove_background_from_img_file("joker.jpg", new_file_name="file-no-bg.png")
```

### `remove_background_from_img_url`

Removes the background given an image URL.

| Parameter     | Default Value | Description   |
| ------------- | ------------- | ------------- |
| timeout       | `30`          | request timeout in seconds (optional, set when creating `RemoveBg`) |
| img_url       | req. param    | URL to the source image |
| size          | `'regular'`   | size of the output image (`'auto'` = highest available resolution, `'preview'`\|`'small'`\|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`\|`'4k'` = original size) |
| type          | `'auto'`      | foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'animal'`, `'car'`, `'car_interior'`, `'car_part'`, `'transportation'`, `'graphics'`, `'other'`) |
| type_level    | `'none'`      | classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification) |
| format        | `'auto'`      | image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`) |
| roi       | `'0 0 100% 100%'` | region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%) |
| crop          | `None`        | crop margin (px or relative). Enables cropping when set. |
| scale         | `'original'`  | image scale relative to the total image size |
| position      | `'original'`  | `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical |
| channels      | `'rgba'`      | request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`) |
| shadow        | `False`       | whether to add an artificial shadow (some types aren't supported) |
| semitransparency | `True`     | semitransparency for windows or glass objects (some types aren't supported) |
| bg            | `None`        | background path / url / color hex (`'81d4fa'`, `'fff'`) / color name (`'green'`) when `bg_type` provided |
| bg_type       | `None`        | background kind (`'path'`, `'url'`, `'color'`) |
| new_file_name | `'no-bg.png'` | file name of the result image |
| return_bytes  |  `'return_bytes'` | return raw image bytes (for service integration) |

#### Code Example (Base64)

```python
from removebg import RemoveBg

rmbg = RemoveBg("YOUR-API-KEY", "error.log", timeout=15)
rmbg.remove_background_from_img_url("http://www.example.com/some_image.jpg")

# for new_file_name:
rmbg.remove_background_from_img_url("http://www.example.com/some_image.jpg", new_file_name="url-no-bg.png")
```

### `remove_background_from_base64_img`

Removes the background given a base64 image string.

| Parameter     | Default Value | Description   |
| ------------- | ------------- | ------------- |
| timeout       | `30`          | request timeout in seconds (optional, set when creating `RemoveBg`) |
| base64_img    | req. param    | base64 image string |
| size          | `'regular'`   | size of the output image (`'auto'` = highest available resolution, `'preview'`\|`'small'`\|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`\|`'4k'` = original size) |
| type          | `'auto'`      | foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'animal'`, `'car'`, `'car_interior'`, `'car_part'`, `'transportation'`, `'graphics'`, `'other'`) |
| type_level    | `'none'`      | classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification) |
| format        | `'auto'`      | image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`) |
| roi       | `'0 0 100% 100%'` | region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%) |
| crop          | `None`        | crop margin (px or relative). Enables cropping when set. |
| scale         | `'original'`  | image scale relative to the total image size |
| position      | `'original'`  | `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical |
| channels      | `'rgba'`      | request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`) |
| shadow        | `False`       | whether to add an artificial shadow (some types aren't supported) |
| semitransparency | `True`     | semitransparency for windows or glass objects (some types aren't supported) |
| bg            | `None`        | background path / url / color hex (`'81d4fa'`, `'fff'`) / color name (`'green'`) when `bg_type` provided |
| bg_type       | `None`        | background kind (`'path'`, `'url'`, `'color'`) |
| new_file_name | `'no-bg.png'` | file name of the result image |
| return_bytes  |  `'return_bytes'` | return raw image bytes (for service integration) |

#### Code Example

```python
from removebg import RemoveBg
import base64

rmbg = RemoveBg("YOUR-API-KEY", "error.log", timeout=15)
with open("joker.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
rmbg.remove_background_from_base64_img(encoded_string)

# for new_file_name:
rmbg.remove_background_from_base64_img(encoded_string, new_file_name="b64-no-bg.png")
```

## Contributions

Contributions and feature requests are always welcome.
