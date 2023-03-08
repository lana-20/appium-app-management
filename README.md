# Appium App Management

In addition to all the device management commands that Appium provides, there is a set of commands specifically related to managing apps on devices.

What are all the things we can do with apps? We can install them, and conversely uninstall them. We can start them (or activate them), and conversely stop them (or terminate them). Why would we want to use Appium to do these things? There are a couple of prominent use cases.

First, we might want to test our own app upgrade flow. Mobile apps are often upgraded, and during the upgrade, apps often need to migrate internally stored user data. It might be a requirement to test that this migration proceeds as expected. The way to test this would be to install the new app over the old one in the course of a test.

Second, we might run into a requirement where we need to test multiple apps in the same scenario. If our app under test integrates with another app, for example, we might need to make sure that the other app is installed as expected, so that our app can launch it in the course of walking through its features.

OK, how do we do these things with Appium?

The set of commands here is fairly symmetrical:

1. To install an app, we simply call <code>driver.install_app</code>, passing in a single parameter which is an absolute path to the application. This is the path to the application on the filesystem where the Appium server is running. Note that just like with the <code>app</code> capability, this path needs to be local to the Appium server, not the client. So if you are using a cloud service, for example, you'll need to use a different strategy for uploading an app to the device on the cloud service. For Android, there are a number of optional keyword arguments we can pass along with this command as well. A couple of the interesting ones are: <code>grantPermissions</code> is a boolean flag that tells Appium whether to automatically grant permissions to Android applications. This is false by default, so if the app you're trying to install requires special permissions, it might be useful to set this to true. <code>replace</code> is another boolean flag that tells Appium whether to overwrite an existing application with the one you are trying to install. This is true by default, but set it to false if you want to be sure never to overwrite existing applications on accident.
2. We can also uninstall an app by calling <code>driver.remove_app</code>. This takes a single parameter, which is the ID of an application on the system. On both Android and iOS, every app has a unique identifier that the system uses to keep track of apps and distinguish them from one another. The developer of the app sets this ID, so it should be a piece of information which is given to you when it comes time to automate the app. If you don't have access to the ID, there are ways you can discover it. If you need the ID for an iOS application, which is called a "bundle ID" for iOS, you can run this little script on a Mac, using the appropriate path to a <code>.app</code> file: <code>osascript -e 'id of app "/path/to/TheApp.app"'</code>. It will spit out the bundle ID for you. Or if you need the ID for an Android application, called an application package ID, we can use a little tool called <code>apkanalyzer</code> which is part of Android studio, and is hopefully now on your path. This command will run <code>apkanalyzer</code> and print out the application ID on macOS or Linux: <code>apkanalyzer -h manifest application-id /path/to/TheApp.apk</code>. If you're on Windows, it's easiest to find the menu item called "Analyze APK" from within Android Studio, which will let you select an APK file to inspect. OK, so if you have the application ID, you can call <code>driver.remove_app</code> to uninstall it for you! Like the previous command, this one has an interesting keyword argument that's only relevant for Android: <code>keepData</code>, which defaults to false, but you can set to true if you want. If you do that, then the app will be uninstalled but any user data will remain!
3. In addition to installing and uninstalling, we can start applications using <code>driver.activate_app</code>. This command assumes the app is installed and takes an app ID as its single parameter. Note that on Android, starting applications can be a little bit more complex, and we have a whole unit dedicated to this, about Android Activities. So just know that if you use this command on Android, what you're doing is essentially equivalent to a user tapping the app's icon on the home screen. And this is often exactly what you want to do!
4. As you might imagine, we can also stop or terminate apps using <code>driver.terminate_app</code>, and passing in the app ID. This just stops the app from running, it doesn't remove it from the device.
5. And finally, we have access to the <code>driver.is_app_installed</code> command, which also takes an app ID, and whose purpose is to tell us whether an app is installed or not. It will return true if the app represented by the app ID is installed, and false otherwise.

Here is a Python example exhibiting the management commands for an open source [app](https://github.com/cloudgrey-io/the-app/releases):

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


We're launching the session with TheApp, but we also have the ApiDemos APK handy. Let's test with it. But first, I want to find out the package ID of this ApiDemos application, so I'll switch over to the terminal and run the following command:

    apkanalyzer -h manifest application-id ./ApiDemos.apk

And the output we get shows us the package ID:

    io.appium.android.apis

Great, so now I know the package ID of this app is <code>io.appium.android.apis</code>. So let's do a few things. First, let's save references to the path to the ApiDemos app and to its package ID, since we'll use them later:

    app = path.join(CUR_DIR, 'ApiDemos.apk')
    app_id = 'io.appium.android.apis'

I'm just assuming that the ApiDemos apk file is in the same directory as this script, like the other test app.

Alright, now let's remove the ApiDemos app, and reinstall it:

    driver.remove_app(app_id)
    driver.install_app(app)

Just in case you're wondering, calling <code>remove_app</code> has no effect if the app is not already installed. It doesn't raise an exception that we have to worry about. OK, so that this point, the ApiDemos app should be installed. Now let's just start it and stop it.

    driver.activate_app(app_id)
    driver.terminate_app(app_id)

And that's it. If we're watching this test run we should just first see TheApp open up, since that's our app under test as defined via the <code>app</code> capability. But then we should see the ApiDemos app briefly flash on screen as it's activated and then go away as it's terminated. This is exactly what we expected, and demonstrates how easy it is to work with apps on the device using Appium.






















