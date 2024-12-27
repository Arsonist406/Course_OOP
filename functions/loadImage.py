from pygame import image, transform

class LoadImage:
    def __init__(self, path, size):
        self.path = path
        self.size = size

    def execute(self):
        photo = image.load(self.path)
        photo = transform.scale(photo, self.size)
        return photo
