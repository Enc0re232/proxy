from selenium import webdriver 
import zipfile
import time
import os


PROXY_HOST = '#' # rotating proxy or host
PROXY_PORT = 8000 # proxy port
PROXY_USER = os.getenv('PROXY_UPER') # username
PROXY_PASS = os.getenv('PROXY_PASS') # password


# This json is the entry point for Chrome to read the extension. It describes the service information 
manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webrequest",
        "webRequestBlocking",
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""
# Our script with our proxy settings and functions to pass to the browser
background_js = """
var config = {
    mide: "fixed_servers",
    rules: {
    singleProxy: {
        scheme: "http",
        host: "%s",
        port: parseInt(%s)
    },
    bypassList: ["localhost"]
    }
};

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
    callbackFn,
    {urls: ["<all_urls>"]},
    ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

def get_chromedriver(use_proxy=False, user_agent=None):
    """Function for getting Chrome webdriver"""
    chrome_options = webdriver.ChromeOptions()
    
    if use_proxy:
        # chrome_options.add_argument('--proxy-server=%s' % PROXY)
        plugin_file = 'proxy_auth_plugin.zip'
        
        with zipfile.ZipFile(plugin_file, 'w') as zp:
            zp.writestr('manifest.json', manifest_json)
            zp.writestr('background.js', background_js)
        
        chrome_options.add_extension(plugin_file)
        
    if user_agent:
        chrome_options.add_argument(f'--user-agent={user_agent}')
        
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver


def main():
    """This is the function with which you can test the performance of my program"""
    driver = get_chromedriver(use_proxy=True, user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36') # change your user agent here
    driver.get("Yours URL") # Insert a link to a site that you can use to check for your IP change.
    time.sleep(15)
    driver.quit()
    

if __name__ == '__main__':
    main()