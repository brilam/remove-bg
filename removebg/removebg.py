from __future__ import absolute_import
import requests
import logging
from typing import Optional

API_ENDPOINT = "https://api.remove.bg/v1.0/removebg"

_logger = logging.getLogger(__name__)


class RemoveBg(object):

    DEFAULT_TIMEOUT = 30  # seconds

    def __init__(
        self,
        api_key,
        error_log_file,
        timeout: Optional[float] = None,
        session: Optional[requests.Session] = None,
    ):
        """Create a new RemoveBg client.

        :param api_key: Your remove.bg API key.
        :param error_log_file: Path to a log file. A basic file logger will be
            configured if none exists yet.
        :param timeout: Optional request timeout (seconds) for each API
            call (default 30s).
        :param session: Optional ``requests.Session`` for connection reuse /
            custom adapters.
        """
        self.__api_key = api_key
        self._timeout = (
            timeout if timeout is not None else self.DEFAULT_TIMEOUT
        )
        self._session = session or requests.Session()
        # Configure root logging minimally if no handlers exist yet.
        if not logging.getLogger().handlers:
            logging.basicConfig(filename=error_log_file, level=logging.ERROR)
        else:
            # Add a file handler specifically for errors (best effort).
            try:
                fh = logging.FileHandler(error_log_file)
                fh.setLevel(logging.ERROR)
                logging.getLogger().addHandler(fh)
            except Exception:  # pragma: no cover – best-effort logging setup.
                pass

    def _check_arguments(self, size, type, type_level, format, channels):
        """Validate arguments against allowed remove.bg values."""
        if size not in [
                "auto", "preview", "small", "regular", "medium", "hd",
                "full", "4k"]:
            raise ValueError("size argument wrong")
        if type not in [
                "auto", "person", "product", "animal", "car",
                "car_interior", "car_part", "transportation", "graphics",
                "other"]:
            raise ValueError("type argument wrong")
        if type_level not in ["none", "latest", "1", "2"]:
            raise ValueError("type_level argument wrong")
        if format not in ["jpg", "zip", "png", "auto"]:
            raise ValueError("format argument wrong")
        if channels not in ["rgba", "alpha"]:
            raise ValueError("channels argument wrong")

    def _output_file(self, response, new_file_name):
        """Persist response content or log an error if the API call failed."""
        if response.status_code == requests.codes.ok:
            try:
                with open(new_file_name, 'wb') as removed_bg_file:
                    removed_bg_file.write(response.content)
            except Exception as ex:  # pragma: no cover
                _logger.error("Unable to write file %s: %s", new_file_name, ex)
        else:
            error_reason = "unknown error"
            try:
                payload = response.json()
                # remove.bg error schema: {"errors": [{"title": "...", ...}]}
                if isinstance(payload, dict) and payload.get("errors"):
                    error_reason = payload["errors"][0].get(
                        "title", error_reason).lower()
            except ValueError:
                # Not JSON – keep generic reason.
                pass
            _logger.error(
                "Unable to save %s due to %s (status %s)",
                new_file_name, error_reason, response.status_code)

    def _build_common_data(self, size, type, type_level, format, roi, crop,
                           scale, position, channels, shadow,
                           semitransparency):
        """Return dict of common form fields for all request types."""
        return {
            'size': size,
            'type': type,
            'type_level': type_level,
            'format': format,
            'roi': roi,
            # If crop margin provided enable cropping and pass as crop_margin.
            'crop': 'true' if crop else 'false',
            'crop_margin': crop,
            'scale': scale,
            'position': position,
            'channels': channels,
            'add_shadow': 'true' if shadow else 'false',
            'semitransparency': 'true' if semitransparency else 'false',
        }

    def remove_background_from_img_file(self, img_file_path, size="regular",
                                        type="auto", type_level="none",
                                        format="auto", roi="0 0 100% 100%",
                                        crop=None, scale="original",
                                        position="original", channels="rgba",
                                        shadow=False, semitransparency=True,
                                        bg=None, bg_type=None,
                                        new_file_name="no-bg.png",
                                        return_bytes=False):
        """
        Removes the background given an image file.

        :param img_file_path: path to the source image file
        :param size: size of the output image ("auto" highest resolution,
            "preview"|"small"|"regular"=0.25MP, "medium"=1.5MP,
            "hd"=4MP, "full"|"4k" = original size)
        :param type: foreground object ("auto", "person", "product",
            "car")
        :param type_level: classification level ("none", "1" coarse,
            "2" specific, "latest")
        :param format: output format ("auto", "png", "jpg", "zip")
        :param roi: region of interest x1 y1 x2 y2 (px or %)
        :param crop: crop margin (px or relative). Enables cropping when set.
        :param scale: image scale relative to the total image size
        :param position: "center" | "original" or coordinates
        :param channels: "rgba" for image or "alpha" for mask
        :param shadow: add artificial shadow
        :param semitransparency: enable window/glass semitransparency
        :param bg: background path/url/color if bg_type set
        :param bg_type: one of "path", "url", "color" (or None)
        :param new_file_name: file name of the result image
        :param return_bytes: if True, return the raw result bytes.
        :return: None. Result saved to ``new_file_name``.
        """
        self._check_arguments(size, type, type_level, format, channels)

        files = {}
        bg_file_handle = None
        try:
            with open(img_file_path, 'rb') as img_file:
                files['image_file'] = img_file
                data = self._build_common_data(
                    size, type, type_level, format, roi, crop, scale,
                    position, channels, shadow, semitransparency)

                if bg_type == 'path' and bg:
                    bg_file_handle = open(bg, 'rb')
                    files['bg_image_file'] = bg_file_handle
                elif bg_type == 'color' and bg:
                    data['bg_color'] = bg
                elif bg_type == 'url' and bg:
                    data['bg_image_url'] = bg

                response = self._session.post(
                    API_ENDPOINT,
                    files=files,
                    data=data,
                    headers={'X-Api-Key': self.__api_key},
                    timeout=self._timeout)
                response.raise_for_status()
                if return_bytes:
                    content = response.content
                    if new_file_name:
                        self._output_file(response, new_file_name)
                    return content
                if new_file_name:
                    self._output_file(response, new_file_name)
        finally:
            if bg_file_handle:
                try:
                    bg_file_handle.close()
                except Exception:
                    pass

    def remove_background_from_img_url(self, img_url, size="regular",
                                       type="auto", type_level="none",
                                       format="auto", roi="0 0 100% 100%",
                                       crop=None, scale="original",
                                       position="original", channels="rgba",
                                       shadow=False, semitransparency=True,
                                       bg=None, bg_type=None,
                                       new_file_name="no-bg.png",
                                       return_bytes=False):
        """
        Removes the background given an image URL.

    :param img_url: URL to the source image
    :param size: output size (see file variant description above)
    :param type: foreground object type
    :param type_level: classification level
    :param format: output format
    :param roi: region of interest
    :param crop: crop margin (enables cropping when set)
        :param scale: image scale relative to the total image size
    :param position: position of result
    :param channels: rgba or alpha
    :param shadow: add shadow
    :param semitransparency: enable semitransparency
    :param bg: background if provided
    :param bg_type: background kind (path/url/color)
        :param new_file_name: file name of the result image
        :param return_bytes: return raw image bytes instead of / in addition
            to writing a file.
        """

        self._check_arguments(size, type, type_level, format, channels)

        if not return_bytes and new_file_name is None:
            raise ValueError(
                "Either provide new_file_name or set return_bytes=True"
            )

        files = {}
        bg_file_handle = None
        try:
            data = self._build_common_data(
                size, type, type_level, format, roi, crop, scale,
                position, channels, shadow, semitransparency)
            data['image_url'] = img_url

            if bg_type == 'path' and bg:
                bg_file_handle = open(bg, 'rb')
                files['bg_image_file'] = bg_file_handle
            elif bg_type == 'color' and bg:
                data['bg_color'] = bg
            elif bg_type == 'url' and bg:
                data['bg_image_url'] = bg

            response = self._session.post(
                API_ENDPOINT,
                data=data,
                files=files if files else None,
                headers={'X-Api-Key': self.__api_key},
                timeout=self._timeout
            )
            response.raise_for_status()
            if return_bytes:
                content = response.content
                if new_file_name:
                    self._output_file(response, new_file_name)
                return content
            if new_file_name:
                self._output_file(response, new_file_name)
        finally:
            if bg_file_handle:
                try:
                    bg_file_handle.close()
                except Exception:
                    pass

    def remove_background_from_base64_img(self, base64_img, size="regular",
                                          type="auto", type_level="none",
                                          format="auto", roi="0 0 100% 100%",
                                          crop=None, scale="original",
                                          position="original", channels="rgba",
                                          shadow=False, semitransparency=True,
                                          bg=None, bg_type=None,
                                          new_file_name="no-bg.png",
                                          return_bytes=False):
        """
        Removes the background given a base64 image string.

        :param base64_img: base64 image string
    :param size: output size variant
    :param type: foreground object type
    :param type_level: classification level
    :param format: output format
    :param roi: region of interest
    :param crop: crop margin (enables cropping when set)
        :param scale: image scale relative to the total image size
    :param position: position of result
    :param channels: rgba or alpha
    :param shadow: add shadow
    :param semitransparency: enable semitransparency
    :param bg: background if provided
    :param bg_type: background kind (path/url/color)
        :param new_file_name: file name of the result image
        :param return_bytes: return raw image bytes optionally
        """

        self._check_arguments(size, type, type_level, format, channels)

        if not return_bytes and new_file_name is None:
            raise ValueError(
                "Either provide new_file_name or set return_bytes=True"
            )

        files = {}
        bg_file_handle = None
        try:
            data = self._build_common_data(
                size, type, type_level, format, roi, crop, scale,
                position, channels, shadow, semitransparency)
            data['image_file_b64'] = base64_img

            if bg_type == 'path' and bg:
                bg_file_handle = open(bg, 'rb')
                files['bg_image_file'] = bg_file_handle
            elif bg_type == 'color' and bg:
                data['bg_color'] = bg
            elif bg_type == 'url' and bg:
                data['bg_image_url'] = bg

            response = self._session.post(
                API_ENDPOINT,
                data=data,
                files=files if files else None,
                headers={'X-Api-Key': self.__api_key},
                timeout=self._timeout
            )
            response.raise_for_status()
            if return_bytes:
                content = response.content
                if new_file_name:
                    self._output_file(response, new_file_name)
                return content
            if new_file_name:
                self._output_file(response, new_file_name)
        finally:
            if bg_file_handle:
                try:
                    bg_file_handle.close()
                except Exception:
                    pass
