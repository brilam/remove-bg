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
        if size not in ["preview", "full", "auto", "regular", "hd", "4k"]:
            raise ValueError("size argument wrong")

        if type not in ["person", "car", "product", "auto"]:
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
        Removes the background given an image file and outputs the file as the original file name with "no_bg.png"
        appended to it.
        :param img_file_path: the path to the image file
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        :param type: foreground object (auto = autodetect, person, product, car)
        :param type_level: classification level. none = no classification, 1 coarse classification, 2 specific classification (car_interior...), latest
        :param format: png, jpg, zip
        :param roi: region of interest, where to look for foreground object. (x1, y1, x2, y2) in px or relative (%)
        :param crop: px or relative, single value = all sides, two vals = top/bottom and left/right, four vals (top, right, bottom, left)
        :param scale: relative scale
        :param position: center, original, single val (horizontal and vertical) or two vals (horizontal, vertical)
        :param channels: rgba or alpha
        :param shadow: true or false (some types aren't supported)
        :param semitransparency: semitransparency for windows or glass objects...
        :param bg: background (color, image_url, image_file)
        :param bg_type: path, url or color
        :param new_file_name: the new file name of the image with the background removed
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
            'add_shadow': "true" if shadow else 'false"',
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
        Removes the background given an image URL and outputs the file as the given new file name.
        :param img_url: the URL to the image
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        :param type: foreground object (auto = autodetect, person, product, car)
        :param type_level: classification level. none = no classification, 1 coarse classification, 2 specific classification (car_interior...), latest
        :param format: png, jpg, zip
        :param roi: region of interest, where to look for foreground object. (x1, y1, x2, y2) in px or relative (%)
        :param crop: px or relative, single value = all sides, two vals = top/bottom and left/right, four vals (top, right, bottom, left)
        :param scale: relative scale
        :param position: center, original, single val (horizontal and vertical) or two vals (horizontal, vertical)
        :param channels: rgba or alpha
        :param shadow: true or false (some types aren't supported)
        :param semitransparency: semitransparency for windows or glass objects...
        :param bg: background (color, image_url, image_file)
        :param bg_type: path, url or color
        :param new_file_name: the new file name of the image with the background removed
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
            'add_shadow': "true" if shadow else 'false"',
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
        Removes the background given a base64 image string and outputs the file as the given new file name.
        :param base64_img: the base64 image string
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        :param type: foreground object (auto = autodetect, person, product, car)
        :param type_level: classification level. none = no classification, 1 coarse classification, 2 specific classification (car_interior...), latest
        :param format: png, jpg, zip
        :param roi: region of interest, where to look for foreground object. (x1, y1, x2, y2) in px or relative (%)
        :param crop: px or relative, single value = all sides, two vals = top/bottom and left/right, four vals (top, right, bottom, left)
        :param scale: relative scale
        :param position: center, original, single val (horizontal and vertical) or two vals (horizontal, vertical)
        :param channels: rgba or alpha
        :param shadow: true or false (some types aren't supported)
        :param semitransparency: semitransparency for windows or glass objects...
        :param bg: background (color, image_url, image_file)
        :param bg_type: path, url or color
        :param new_file_name: the new file name of the image with the background removed
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
            'add_shadow': "true" if shadow else 'false"',
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