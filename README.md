# remove-bg
A Python API wrapper for removing backgrounds from picture using remove.bg's API

# License
This code is licensed under the MIT License. See [here](https://github.com/brilam/remove-bg/blob/master/LICENSE) for more details.

# Installation
`pip install removebg`

# How to Use
## `remove_background_from_img_file`

| Parameter     | Required      | Description  |
| ------------- |:-------------:| -------------|
| img_file_path | Y             | the path to the image file      |
| size          | N             | the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP). Default value is "regular"|
| bg_color      | N             | adds a solid color background. Can be a hex color code (e.g. 81d4fa, fff) or a color name (e.g. green).|

### Code Example:
```python
from removebg import RemoveBg

rmbg = RemoveBg("YOUR-API-KEY", "error.log")
rmbg.remove_background_from_img_file("joker.jpg")
```


## `remove_background_from_img_url`
| Parameter     | Required      | Description  |
| ------------- |:-------------:| -------------|
| img_url | Y                   | the URL to the image|
| size          | N             | the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP). Default value is "regular"|
| new_file_name | N             | the new file name of the image with the background removed |
| bg_color      | N             | adds a solid color background. Can be a hex color code (e.g. 81d4fa, fff) or a color name (e.g. green).|

### Code Example:
```python
from removebg import RemoveBg

rmbg = RemoveBg("YOUR-API-KEY", "error.log")
rmbg.remove_background_from_img_url("http://www.example.com/some_image.jpg")
```


## `remove_background_from_base64_img`
| Parameter     | Required      | Description  |
| ------------- |:-------------:| -------------|
| base64_img    | Y             | the base64 image string|
| size          | N             | the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP). Default value is "regular"|
| new_file_name | N             | the new file name of the image with the background removed |
| bg_color      | N             | adds a solid color background. Can be a hex color code (e.g. 81d4fa, fff) or a color name (e.g. green).|

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
