
import json
class ImageMeta:
    def __init__(self, fileName, customName, fullPath, uploadURL, id, width, height, displayWidth, displayHeight):
        self.fileName = fileName
        self.customName = customName
        self.fullPath = fullPath
        self.uploadURL = uploadURL
        self.id = id
        self.width = width
        self.height = height
        self.displayWidth = displayWidth
        self.displayHeight = displayHeight
        
    def __dict__(self):
        return {
            "fileName": self.fileName,
            "customName": self.customName,
            "fullPath": self.fullPath,
            "uploadURL": self.uploadURL,
            "id": self.id,
            "width": self.width,
            "height": self.height,
            "displayWidth": self.displayWidth,
            "displayHeight": self.displayHeight,
        }
        
    def __json__(self):
        return json.dumps({f"{str(self.id)}:": {
                    "fileName": self.fileName,
                    "customName": self.customName,
                    "fullPath": self.fullPath,
                    "uploadURL": self.uploadURL,
                    "id": self.id,
                    "width": self.width,
                    "height": self.height,
                    "displayWidth": self.displayWidth,
                    "displayHeight": self.displayHeight,
                }})