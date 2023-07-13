"""
Video upload and conversion tests for Elvishmedia
Please make sure that local server is running before running tests

To run tests use the following command:
python manage.py test
"""

import time
from django.test import TestCase 
from django.test import LiveServerTestCase
from django.conf import settings
from django.core.files.storage import default_storage
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select


DRIVER_OPTIONS = Options() # Define chromedriver options
DRIVER_OPTIONS.add_experimental_option('excludeSwitches', ['enable-logging'])
MEDIA_TEST_PATH = settings.MEDIA_ROOT + '/tests/' # Define path to test files in media root

# Define tests below
class VideoConverterTests(TestCase, webdriver.Chrome):

    serve_static = True

    @classmethod
    def setUpClass(cls):
        
        super().setUpClass()
        try:
            cls.driver = webdriver.Chrome( # Define chromedriver path
                executable_path=MEDIA_TEST_PATH + 'chromedriver.exe',
                options=DRIVER_OPTIONS
                )
        except:
            super().tearDownClass() # Close chromedriver and throw exception
            raise Exception('Could not find chromedriver.exe in ' + MEDIA_TEST_PATH)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit() # Close chromedriver
        super().tearDownClass()

    def test_video_upload_and_conversion(self):
        print('\n--- Testing file upload functionality ---\n')
        self._file_in_path() # Check if sample file is in path
        self._upload_video() # Upload sample file
        print('(OK) File uploaded')

        print('\n--- Testing file conversion functionality ---\n')
        self._uploaded_in_path() # Check if sample file is in uploads folder
        self._convert_video() # Convert sample file

        print('\n--- Finalizing and deleting files ---\n')
        self._close_window() # Close chrome window
        self._remove_files() # Remove files from uploads folder

    """ ----- Tests start here ----- """

    """
    Test (1) 
    Upload functionality
    """

    def _file_in_path(self):
        self._MKV_sample = 'MKV_sample.mkv' # Define sample file name
        try:
            self.assertTrue(self._MKV_sample in default_storage.listdir(MEDIA_TEST_PATH)[1]) # Check if sample file is in path
            print('(OK) Sample file found for test')
        except:
            # Close chromedriver and throw exception if sample file not found
            raise Exception('Sample file not found for test. Please add ' + self._MKV_sample + ' to ' + MEDIA_TEST_PATH)


    def _upload_video(self):
        self._MKV_sample = 'MKV_sample.mkv' # Define sample file name

        try:
            self.driver.get('http://127.0.0.1:8000/') # Open website
            time.sleep(5) # Wait for page to load
            WebDriverWait(self.driver, 10).until( # Wait for dropzone file input to load
                EC.presence_of_element_located((By.CLASS_NAME,
                 'dz-hidden-input')))
            print('(OK) Page loaded')
        except:
            raise Exception('Could not load page') # Throw exception if page not loaded
        
        self.upload = self.driver.find_element( # Define dropzone file input
            By.CLASS_NAME,
            'dz-hidden-input'
            )
        
        try:
            self.upload.send_keys( # Send sample file to dropzone file input
                MEDIA_TEST_PATH + self._MKV_sample
            )
            WebDriverWait(self.driver, 10).until( # Wait for success mark to appear, signaling that file is uploaded
                EC.visibility_of_element_located((By.CLASS_NAME, "dz-success-mark"))
            )
        except:
            raise Exception('Could not upload file')
        
    """
    End of Test (1)
    """
        
    """
    Test (2) 
    Conversion functionality
    """

    def _uploaded_in_path(self):
        try:
            # Check if sample file is in uploads folder
            self.assertTrue(self._MKV_sample in default_storage.listdir(settings.MEDIA_ROOT + '/uploads/videos/')[1])
            print('(OK) Sample file found in uploads folder')
        except:
            raise Exception('Sample file not found in uploads folder')
    
    def _convert_video(self):
        try:
            self.conversion_format = Select(self.driver.find_element(By.ID,'output_format')) # Define conversion format dropdown
            self.conversion_format.select_by_value('.mp4') # Select mp4 conversion format
            WebDriverWait(self.driver, 10).until( # Wait for submit button to appear
                EC.visibility_of_element_located((By.ID,
                 'submitul')))
            self.driver.find_element(By.ID,'submitul').click() # Click submit button
            WebDriverWait(self.driver, 600).until( # Wait for download button to appear, signaling that file is converted
                EC.visibility_of_element_located((By.ID,
                 'download-btn')))
            print('(OK) File converted')
        except:
            raise Exception('Could not convert file')
        
    """
    End of Test (2)
    """
    
    """
    Finalizing and deleting files
    """
    def _close_window(self):
        self.driver.close() # Close chrome window
     
    def _remove_files(self):
        try: # Remove sample files from uploads folder
            default_storage.delete(settings.MEDIA_ROOT + '\\uploads\\videos\\' + self._MKV_sample)
            default_storage.delete(settings.MEDIA_ROOT + '\\uploads\\videos\\' + self._MKV_sample.split('.')[0] + '.mp4')
            print('(OK) Sample files removed')
        except:
            raise Exception('Could not remove sample files')
        