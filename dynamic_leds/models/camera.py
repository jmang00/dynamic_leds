import urllib.request
import requests
from PIL import Image
from io import BytesIO
import cv2
from abc import ABC, abstractmethod


class CameraGroup:
    def __init__(self, config):
        self.cameras = []
        for cam_id, cam_source in config['CAMS'].items():
            if int == type(cam_source):
                self.cameras.append(LocalCamera(cam_id, cam_source))
            elif str == type(cam_source):
                self.cameras.append(UrlCamera(cam_id, cam_source))

    def __iter__(self):
        return iter(self.cameras)

    def __getitem__(self, index):
        return self.cameras[index]

    def __len__(self):
        return len(self.cameras)

    def test_all(self):
        for camera in self.cameras:
            print(f'Testing {camera}...')
            if camera.is_open():
                print(f'{camera} is open')
            else:
                print(f'{camera} is not open')

    def release_all(self):
        for camera in self.cameras:
            camera.release()


class Camera(ABC):
    """
    Abstract base class for a camera.
    """

    def __init__(self, camid):
        """
        Initialize the camera with an ID.
        """
        self.id = camid

    @abstractmethod
    def is_open(self):
        """
        Check if the camera is open.
        """
        pass

    @abstractmethod
    def take_photo(self):
        """
        Take a photo using the camera.
        """
        pass

    @abstractmethod
    def save_photo(self, filename):
        """
        Save the photo taken by the camera.
        """
        pass


class UrlCamera(Camera):
    """
    A camera that takes photos from a URL.
    """

    def __init__(self, camid, url):
        """
        Initialize the URL camera with an ID and a URL.
        """
        self.url = url
        super().__init__(camid)

    def __repr__(self):
        """
        Return a string representation of the camera.
        """
        return f'Camera {self.id} (URL: {self.url})'

    def is_open(self):
        """
        Check if the URL is accessible.
        """
        try:
            response = requests.get(self.url)
            img = Image.open(BytesIO(response.content))
            return True
        except:
            return False

    def take_photo(self):
        """
        Take a photo from the URL.
        """
        response = requests.get(self.url)
        img = Image.open(BytesIO(response.content))
        img = img.rotate(270, expand=True)
        return img

    def save_photo(self, filename):
        """
        Save the photo from the URL.
        """
        urllib.request.urlretrieve(self.url, filename)

    def release(self):
        """
        Release the URL camera. (Doesn't actually need to do anything)
        """
        pass


class LocalCamera(Camera):
    """
    A camera that takes photos from a local source.
    """

    def __init__(self, camid, source):
        """
        Initialize the local camera with an ID and a source.
        """
        self.cam = cv2.VideoCapture(source)
        super().__init__(camid)

    def __repr__(self):
        """
        Return a string representation of the camera.
        """
        return f'Camera {self.id} (Source: {self.source})'

    def is_open(self):
        """
        Check if the local source is accessible.
        """
        check, frame = self.cam.read()
        return check

    def take_photo(self):
        """
        Take a photo from the local source.
        """
        check, frame = self.cam.read()

        if check:
            return frame
        else:
            print('Error reading camera')
            return None

    def save_photo(self, filename):
        """
        Save the photo from the local source.
        """
        frame = self.take_photo()

        if frame is not None:
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            cv2.imwrite(filename, frame)

    def release(self):
        """
        Release the local source.
        """
        self.cam.release()
