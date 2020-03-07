from __future__ import absolute_import
import requests
import logging

API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"


class RemoveBg(object):

    def __init__(self, api_key, error_log_file):
        self.__api_key = api_key
        logging.basicConfig(filename=error_log_file)

    def remove_background_from_img_file(self, img_file_path, size="regular", bg_color=None):
        """
        Removes the background given an image file and outputs the file as the original file name with "no_bg.png"
        appended to it.
        :param img_file_path: the path to the image file
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        """
        # Open image file to send information post request and send the post request
        img_file = open(img_file_path, 'rb')
        response = requests.post(
            API_ENDPOINT,
            files={'image_file': img_file},
            data={
                'size': size,
                'bg_color': bg_color
            },
            headers={'X-Api-Key': self.__api_key})
        response.raise_for_status()
        self.__output_file__(response, img_file.name + "_no_bg.png")

        # Close original file
        img_file.close()

    def remove_background_from_img_url(self, img_url, size="regular", new_file_name="no-bg.png", bg_color=None):
        """
        Removes the background given an image URL and outputs the file as the given new file name.
        :param img_url: the URL to the image
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        :param new_file_name: the new file name of the image with the background removed
        """
        response = requests.post(
            API_ENDPOINT,
            data={
                'image_url': img_url,
                'size': size,
                'bg_color': bg_color
            },
            headers={'X-Api-Key': self.__api_key}
        )
        response.raise_for_status()
        self.__output_file__(response, new_file_name)

    def remove_background_from_base64_img(self, base64_img, size="regular", new_file_name="no-bg.png", bg_color=None):
        """
        Removes the background given a base64 image string and outputs the file as the given new file name.
        :param base64_img: the base64 image string
        :param size: the size of the output image (regular = 0.25 MP, hd = 4 MP, 4k = up to 10 MP)
        :param new_file_name: the new file name of the image with the background removed
        """
        response = requests.post(
            API_ENDPOINT,
            data={
                'image_file_b64': base64_img,
                'size': size,
                'bg_color': bg_color
            },
            headers={'X-Api-Key': self.__api_key}
        )
        response.raise_for_status()
        self.__output_file__(response, new_file_name)

    def __output_file__(self, response, new_file_name):
        # If successful, write out the file
        if response.status_code == requests.codes.ok:
            with open(new_file_name, 'wb') as removed_bg_file:
                removed_bg_file.write(response.content)
        # Otherwise, print out the error
        else:
            error_reason = response.json()["errors"][0]["title"].lower()
            logging.error("Unable to save %s due to %s", new_file_name, error_reason)
