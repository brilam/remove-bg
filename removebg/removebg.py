from __future__ import absolute_import
import requests
import logging

API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"

class RemoveBg(object):

    def __init__(self, api_key, error_log_file):
        self.__api_key = api_key
        logging.basicConfig(filename=error_log_file)

    def _check_arguments(self, size, type, type_level, format, channels):
        """Check if arguments are valid."""
        if size not in ["auto", "preview", "small", "regular", "medium", "hd", "full", "4k"]:
            raise ValueError("size argument wrong")

        if type not in ["auto", "person", "product", "animal", "car", "car_interior", "car_part", "transportation", "graphics", "other"]:
            raise ValueError("type argument wrong")

        if type_level not in ["none", "latest", "1", "2"]:
            raise ValueError("type_level argument wrong")

        if format not in ["jpg", "zip", "png", "auto"]:
            raise ValueError("format argument wrong") 
 
        if channels not in ["rgba", "alpha"]:
            raise ValueError("channels argument wrong") 
        
    def _output_file(self, response, new_file_name):
        # If successful, write out the file
        if response.status_code == requests.codes.ok:
            with open(new_file_name, 'wb') as removed_bg_file:
                removed_bg_file.write(response.content)
        # Otherwise, print out the error
        else:
            error_reason = response.json()["errors"][0]["title"].lower()
            logging.error("Unable to save %s due to %s", new_file_name, error_reason)
        
    def remove_background_from_img_file(self, img_file_path, size="regular", 
                                       type="auto", type_level="none", 
                                       format="auto", roi="0 0 100% 100%", 
                                       crop=None, scale="original", 
                                       position="original", channels="rgba", 
                                       shadow=False, semitransparency=True,
                                       bg=None, bg_type=None, new_file_name="no-bg.png"):
        """
        Removes the background given an image file.
        
        :param img_file_path: path to the source image file
        :param size: size of the output image (`'auto'` = highest available resolution, `'preview'`|`'small'`|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`|`'4k'` = original size)
        :param type: foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'car'`)
        :param type_level: classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification)
        :param format: image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`)
        :param roi: region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%)
        :param crop: px or relative, single val = all sides, two vals = top/bottom, left/right, four vals = top, right, bottom, left
        :param scale: image scale relative to the total image size
        :param position: `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical
        :param channels: request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`)
        :param shadow: whether to add an artificial shadow (some types aren't supported)
        :param semitransparency: semitransparency for windows or glass objects (some types aren't supported)
        :param bg: background (`None` = no background, path, url, color hex code (e.g. `'81d4fa'`, `'fff'`), color name (e.g. `'green'`))
        :param bg_type: background type (`None` = no background, `'path'`, `'url'`, `'color'`)
        :param new_file_name: file name of the result image
        """

        self._check_arguments(size, type, type_level, format, channels)

        img_file = open(img_file_path, 'rb')
        files = {'image_file': img_file}
        
        data = {
            'size': size,
            'type': type,
            'type_level': type_level,
            'format': format,
            'roi': roi,
            'crop': 'true' if crop else 'false',
            'crop_margin': crop,
            'scale': scale,
            'position': position,
            'channels': channels,
            'add_shadow': 'true' if shadow else 'false',
            'semitransparency': 'true' if semitransparency else 'false',
        }

        if bg_type == 'path':
            files['bg_image_file'] = open(bg, 'rb')
        elif bg_type == 'color':
            data['bg_color'] = bg
        elif bg_type == 'url':
            data['bg_image_url'] = bg

        # Open image file to send information post request and send the post request
        response = requests.post(
            API_ENDPOINT,
            files=files,
            data=data,
            headers={'X-Api-Key': self.__api_key})
        response.raise_for_status()
        self._output_file(response, new_file_name)

        # Close original file
        img_file.close()

    def remove_background_from_img_url(self, img_url, size="regular", 
                                       type="auto", type_level="none", 
                                       format="auto", roi="0 0 100% 100%", 
                                       crop=None, scale="original", 
                                       position="original", channels="rgba", 
                                       shadow=False, semitransparency=True,
                                       bg=None, bg_type=None, new_file_name="no-bg.png"):
        """
        Removes the background given an image URL.
        
        :param img_url: URL to the source image
        :param size: size of the output image (`'auto'` = highest available resolution, `'preview'`|`'small'`|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`|`'4k'` = original size)
        :param type: foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'car'`)
        :param type_level: classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification)
        :param format: image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`)
        :param roi: region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%)
        :param crop: px or relative, single val = all sides, two vals = top/bottom, left/right, four vals = top, right, bottom, left
        :param scale: image scale relative to the total image size
        :param position: `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical
        :param channels: request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`)
        :param shadow: whether to add an artificial shadow (some types aren't supported)
        :param semitransparency: semitransparency for windows or glass objects (some types aren't supported)
        :param bg: background (`None` = no background, path, url, color hex code (e.g. `'81d4fa'`, `'fff'`), color name (e.g. `'green'`))
        :param bg_type: background type (`None` = no background, `'path'`, `'url'`, `'color'`)
        :param new_file_name: file name of the result image
        """

        self._check_arguments(size, type, type_level, format, channels)

        files = {}
        
        data = {
            'image_url': img_url,
            'size': size,
            'type': type,
            'type_level': type_level,
            'format': format,
            'roi': roi,
            'crop': 'true' if crop else 'false',
            'crop_margin': crop,
            'scale': scale,
            'position': position,
            'channels': channels,
            'add_shadow': 'true' if shadow else 'false',
            'semitransparency': 'true' if semitransparency else 'false',
        }

        if bg_type == 'path':
            files['bg_image_file'] = open(bg, 'rb')
        elif bg_type == 'color':
            data['bg_color'] = bg
        elif bg_type == 'url':
            data['bg_image_url'] = bg

        response = requests.post(
            API_ENDPOINT,
            data=data,
            headers={'X-Api-Key': self.__api_key}
        )
        response.raise_for_status()
        self._output_file(response, new_file_name)

    def remove_background_from_base64_img(self, base64_img, size="regular", 
                                          type="auto", type_level="none", 
                                          format="auto", roi="0 0 100% 100%", 
                                          crop=None, scale="original", 
                                          position="original", channels="rgba", 
                                          shadow=False, semitransparency=True,
                                          bg=None, bg_type=None, new_file_name="no-bg.png"):
        """
        Removes the background given a base64 image string.
        
        :param base64_img: base64 image string
        :param size: size of the output image (`'auto'` = highest available resolution, `'preview'`|`'small'`|`'regular'` = 0.25 MP, `'medium'` = 1.5 MP, `'hd'` = 4 MP, `'full'`|`'4k'` = original size)
        :param type: foreground object (`'auto'` = autodetect, `'person'`, `'product'`, `'car'`)
        :param type_level: classification level of the foreground object (`'none'` = no classification, `'1'` = coarse classification (e.g. `'car'`), `'2'` = specific classification (e.g. `'car_interior'`), `'latest'` = latest classification)
        :param format: image format (`'auto'` = autodetect, `'png'`, `'jpg'`, `'zip'`)
        :param roi: region of interest, where to look for foreground object (x1, y1, x2, y2) in px or relative (%)
        :param crop: px or relative, single val = all sides, two vals = top/bottom, left/right, four vals = top, right, bottom, left
        :param scale: image scale relative to the total image size
        :param position: `'center'`, `'original'`, single val = horizontal and vertical, two vals = horizontal, vertical
        :param channels: request the finalized image (`'rgba'`) or an alpha mask (`'alpha'`)
        :param shadow: whether to add an artificial shadow (some types aren't supported)
        :param semitransparency: semitransparency for windows or glass objects (some types aren't supported)
        :param bg: background (`None` = no background, path, url, color hex code (e.g. `'81d4fa'`, `'fff'`), color name (e.g. `'green'`))
        :param bg_type: background type (`None` = no background, `'path'`, `'url'`, `'color'`)
        :param new_file_name: file name of the result image
        """

        self._check_arguments(size, type, type_level, format, channels)

        files = {}
        
        data = {
            'image_file_b64': base64_img,
            'size': size,
            'type': type,
            'type_level': type_level,
            'format': format,
            'roi': roi,
            'crop': 'true' if crop else 'false',
            'crop_margin': crop,
            'scale': scale,
            'position': position,
            'channels': channels,
            'add_shadow': 'true' if shadow else 'false',
            'semitransparency': 'true' if semitransparency else 'false',
        }

        if bg_type == 'path':
            files['bg_image_file'] = open(bg, 'rb')
        elif bg_type == 'color':
            data['bg_color'] = bg
        elif bg_type == 'url':
            data['bg_image_url'] = bg

        response = requests.post(
            API_ENDPOINT,
            data=data,
            headers={'X-Api-Key': self.__api_key}
        )
        response.raise_for_status()
        self._output_file(response, new_file_name)