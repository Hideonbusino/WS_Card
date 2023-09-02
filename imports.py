import cv2 
import numpy as np
import re
import pytesseract
import pandas as pd
import os
import math
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pyautogui
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

current_dir = 'C:\\Coding\\python\\ws\\'
raw_csv_path = current_dir + 'data/raw.csv'
price_csv_path = current_dir + 'data/price.csv'

service = Service(executable_path=r"C:/SeleniumDriver/chromedriver.exe")
