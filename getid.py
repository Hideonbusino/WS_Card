#Use read_image(image_path) to get the id from the image
#Image path is the path of the image relative to the run.py file
#Then, use yuyu(text) to get the name and price from yuyutei

from imports import *

#helper function: for image processing
def resize(frame, scale=0.3):
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    return cv2.resize(frame, (width,height), interpolation=cv2.INTER_AREA)
def final(frame):
    return cv2.resize(frame, (630,880), interpolation=cv2.INTER_AREA)
def wait():
    cv2.waitKey(0)

#helper function:returns a string with only characters
def extract_characters(s):
    whitelist = r'[a-zA-Z0-9\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]'
    return ''.join(re.findall(whitelist, s))

#helper function: extract the id name from the string
def extract_id(s):
        pattern = r"[A-Za-z]+[A/]?[SW35][Ss\d]+-[Ss\d]+\s*(?:RR|SEC|SP|SSP|OFR|PR|HYR|RRR|R|SPM|5P|S5P)"
        matches = re.findall(pattern, s)[0]
        if matches[2] == 'A' and matches[3] in ['S', 'W','3', '5']:
            matches = matches[:2] + '/' + matches[3:]
        if matches[3] == 'A' and matches[4] in ['S', 'W','3', '5']:
            matches = matches[:3] + '/' + matches[4:]
        if matches[3] in ['3','5'] and matches[2] == '/':
            matches = matches[:3] + 'S' + matches[4:]
        if matches[4] in ['3','5'] and matches[3] == '/':
            matches = matches[:4] + 'S' + matches[5:]
        if matches[-2] == '5':
            matches = matches[:-2] + 'S' + matches[-1]
        if '/' not in matches:
        # Check if the fourth character is a digit
            if matches[3].isdigit():
                # Add '/' after the 2nd character
                matches = matches[:2] + '/' + matches[2:]
            else:
                # Add '/' after the 3rd character
                matches = matches[:3] + '/' + matches[3:]
        return matches

#helper function: gets the left corner of the image
def resize(image_path):
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' not found.")
        return -1
    # Preprocess image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Error: Couldn't read the image '{image_path}'.")
        return -1
    height, width, _ = img.shape

    # Crop the left quarter of the image
    left_quarter = img[int(height/2):height, 0:int(width/2)]

    # Resize the left quarter to original dimensions
    resized_left_quarter = cv2.resize(left_quarter, (width, height), interpolation=cv2.INTER_CUBIC)

    # Save the processed image
    tem_file = current_dir + 'tem.jpg'
    cv2.imwrite(tem_file, resized_left_quarter)
    return tem_file

#not used: returns the cropped image
def crop_image(image_file):
    try:
        # Ensure the file exists
        if not os.path.exists(image_file):
            print(f"Error: File '{image_file}' not found.")
            return None

        # Preprocess image
        img = cv2.imread(image_file)
        if img is None:
            print(f"Error: Couldn't read the image '{image_file}'.")
            return None

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        egray = cv2.equalizeHist(gray)
        binary = cv2.adaptiveThreshold(egray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                       cv2.THRESH_BINARY_INV, 11, 2)
        blur = cv2.GaussianBlur(binary, (9, 9), cv2.BORDER_DEFAULT)
        canny = cv2.Canny(blur, 175, 250)
        dilated = cv2.dilate(canny, (11,11), iterations=3)

        # Create contours
        contours, hierarchies = cv2.findContours(dilated, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out small contours
        min_contour_area = 150
        filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > min_contour_area]

        # Check if any valid contours were found
        if not filtered_contours:
            print("Error: No valid contours found.")
            return None

        # Merge all contour points
        merged_contours = np.vstack(filtered_contours)
        rect = cv2.minAreaRect(merged_contours)
        box = cv2.boxPoints(rect)
        box = np.intp(box)

        # Warp image
        box = sorted(box, key=lambda x: x[1])
        if box[0][0] > box[1][0]:
            box[0], box[1] = box[1], box[0]
        if box[2][0] > box[3][0]:
            box[2], box[3] = box[3], box[2]

        width = int(rect[1][0])
        height = int(rect[1][1])
        dst = np.array([
            [0, 0],
            [width-1, 0],
            [0, height-1],
            [width-1, height-1],
        ], dtype="float32")
        M = cv2.getPerspectiveTransform(np.array(box, dtype="float32"), dst)
        warped = cv2.warpPerspective(img, M, (width, height))
        f = final(warped)  

        # Preprocess cropped image
        x_start, y_start, x_end, y_end =  63, 770, 170, 788 
        roi = f[y_start:y_end, x_start:x_end]
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        roi_egray = cv2.equalizeHist(roi_gray)
        roi_resized = cv2.resize(roi_egray, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        tem_file = 'tem.jpg'
        cv2.imwrite(tem_file, roi_resized)
        return tem_file

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

#main function: for finding the text in the image. Returns the text
def read_image(image_path):
    try:
        # Check if chromedriver exists at the specified path
        '''if not os.path.exists(service_path):
            print(f"Error: Chromedriver not found at '{service_path}'.")
            return -1'''

        # Check if the image exists
        final_path = current_dir + image_path
        if not os.path.exists(final_path):
            print(f"Error: Image not found at '{final_path}'.")
            return -1

        # Initialize web driver
        #service = Service(service_path)
        driver = webdriver.Chrome(service=service)
        driver.get('https://www.google.com/imghp')
        driver.implicitly_wait(1)
        # Interact with web elements using original logic
        camera_button = driver.find_element(By.CLASS_NAME, 'Gdd5U')
        camera_button.click()

        upload_button = driver.find_element(By.CLASS_NAME, 'DV7the')
        upload_button.click()
        
        time.sleep(0.5)
        pyautogui.write(resize(final_path))
        time.sleep(0.5)
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.press('enter')
        text_button = driver.find_element(By.XPATH, '//*[@id="ucj-4"]/span[1]')
        text_button.click()
        select_button = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/div/div[2]/c-wiz/div/div/div/div[2]/div[1]/div/div/div/div[2]/div/button/span')
        select_button.click()
        time.sleep(0.5)
        element = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/c-wiz/div/div[2]/c-wiz/div/div/span/div/div[2]')
        text = re.split(r'CH',element.text.upper())[1]
        print(text)
        return extract_id(text)
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1

    finally:
        # Ensure the browser is closed at the end
        if 'driver' in locals() and driver:
            driver.quit()

#main function: searching the details in yuyutei. Returns list of [id, name, yuyutei price, available] 0,1,2,4
def yuyu(text):
    try:
        no_spaces = re.sub(r'\s+', '', text)
        split = re.split(r'/', no_spaces)
        series = split[0]
        id_no = re.search(r'([A-Z]+\d+-\d+)', split[1]).group(0)
        rarity = re.search(r'[A-Z]+$', split[1]).group(0)
        rarity_name = '' if rarity == 'RR' else rarity
        yu_url = 'https://yuyu-tei.jp/game_ws/sell/sell_price.php?name='+series+'%2F'+ id_no+rarity_name+'&rare=&type&kizu=0'
        
        s = requests.Session()
        headers = {'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7'}
        s.headers.update(headers)
        response = s.get(yu_url)
        
        # Check if the request was successful
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        card_list = soup.find("ul", class_="card_list")
        
        # Check if BeautifulSoup finds the expected elements
        if card_list:
            img_element = card_list.find("img")
            price_element = card_list.find("p", class_='price')
            stock = card_list.find("p", class_='stock')
            if img_element and price_element:
                name = img_element["alt"]
                price = price_element.text
                price = re.findall("[0-9]+", price)[0]
                name = re.findall("\S[^(]*", name) 
                yuyu_name = re.sub('["“”#]',' ',name[0])
                if stock.text == '残：×':
                    available = 0
                else:
                    available = int((re.findall("[0-9]+", stock.text)[0]))
                #print(text, yuyu_name, price)
                return [text, yuyu_name, price, available]
            else:
                print(f"Couldn't find expected elements in {text}.")
                return -1
        else:
            print(f"Card list not found in {text}.")
            return -1

    except requests.RequestException as e:
        print(f"Request error for {text}: {e}")
        return -1
    except Exception as e:
        print(f"An error occurred for {text}: {e}")
        return -1