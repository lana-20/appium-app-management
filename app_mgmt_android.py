from os import path
from appium import webdriver

CUR_DIR = path.dirname(path.abspath(__file__))
APP = path.join(CUR_DIR, 'TheApp-v1.10.0.apk')
APPIUM = 'http://localhost:4723'
CAPS = {
    'platformName': 'Android',
    'platformVersion': '13.0',
    'deviceName': 'Android Emulator',
    'automationName': 'UiAutomator2',
    'app': APP,
}

driver = webdriver.Remote(APPIUM, CAPS)
try:
    app = path.join(CUR_DIR, 'ApiDemos.apk')
    app_id = 'io.appium.android.apis'
    driver.remove_app(app_id)
    driver.install_app(app)
    driver.activate_app(app_id)
    driver.terminate_app(app_id)
finally:
    driver.quit()
