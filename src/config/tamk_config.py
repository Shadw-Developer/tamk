import os

class Config:
    def __init__(self):
        self.VERSION = "2026.1.0-alpha"
        self.DEV_DIR = os.path.join(os.getcwd(), "development")
        self.SDK_PATH = os.path.join(self.DEV_DIR, "sdk/android.jar")
        self.KEYSTORE = os.path.join(self.DEV_DIR, "secret/debug.keystore")
        self.SMARTIDE_PATH = "/data/data/org.smartide.code/files/home/"
