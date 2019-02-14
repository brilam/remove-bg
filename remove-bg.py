import requests

API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"


class RemoveBg:

    def __init__(self, api_key):
        self.__api_key = api_key

    def remove_background_from_img_file(self, img_file_path, size="regular"):
        # Open image file to send information post request and send the post request
        img_file = open(img_file_path, 'rb')
        response = requests.post(
            API_ENDPOINT,
            files={'image_file': img_file},
            data={'size': size},
            headers={'X-Api-Key': self.__api_key})

        # If successful, write out the file
        if response.status_code == requests.codes.ok:
            with open(img_file.name + "_no_bg.png", 'wb') as removed_bg_file:
                removed_bg_file.write(response.content)
        # Otherwise, print out the error
        else:
            print("Error: ", response.status_code, response.text)

        # Close original file
        img_file.close()

    def remove_background_from_img_url(self, img_url, size="regular", new_file_name="no-bg.png"):
        response = requests.post(
            API_ENDPOINT,
            data={
                'image_url': img_url,
                'size': size
            },
            headers={'X-Api-Key': self.__api_key},
        )

        # If successful, write out the file
        if response.status_code == requests.codes.ok:
            with open(new_file_name, 'wb') as removed_bg_file:
                removed_bg_file.write(response.content)
        # Otherwise, print out the error
        else:
            print("Error: ", response.status_code, response.text)

    def remove_background_from_base64_img(self, img_file, size="regular", new_file_name="no-bg.png"):
        pass
