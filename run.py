import getid 
import price
import os
from imports import *
#name = (getid.read_image('img\\001_A.jpg'))
#print(getid.yuyu(name))


#integrates the main functions above, returns info = yuyu(text)
#img is the path relative to the current directory
def collect_data(img, letter):
    text = getid.read_image(img)
    if text == -1:
        print(f'{img} cannot be read')
        return
    info = getid.yuyu(text)
    if text == -1:
        print(f'{text} cannot be found in yuyutei')
        return
    price.mercari(info, letter)
    print("looking for next....")
    return info   

#collects all the data from the images in the img folder
def collect_all(x,y):
    all_files = os.listdir('img')
    for file in all_files:
        # Split the filename into its components
        name, ext = os.path.splitext(file)
        
        # Check if the file is a JPEG
        if ext.lower() == '.jpg':
            # Split the name into its numeric and letter components
            try:
                num, let = name.split('_')
                num = int(num)
            except ValueError:
                continue  # Skip files that don't match the expected format
            
            # Check if the file matches the given criteria
            if x <= num <= y and let in ['A', 'B', 'C', 'D', 'E', 'F']:
                collect_data('img\\'+file, let)
    print("Finished collecting all")

def add_ind_data(text, letter):
    info = getid.yuyu(text)
    if info == -1:
        print(f'{text} cannot be found in yuyutei')
        return
    price.mercari(info, letter)
    return info   


#removes the csv files
def remove_all():
    os.remove(price_csv_path)
    os.remove(raw_csv_path)

def remove_row(id):
    id = re.sub(r'\s+', '', id)
    df = pd.read_csv(raw_csv_path)
    if id not in df.id.values:
        print(f'{id} not found in database')
        return
    df = df[df.id != id]
    df.reset_index(drop=True, inplace=True)
    df.to_csv(raw_csv_path, index=False)  
    df = pd.read_csv(price_csv_path)
    df = df[df.id != id]
    df.reset_index(drop=True, inplace=True)
    df.to_csv(price_csv_path, index=False)
    return

if __name__ == '__main__':
    add_ind_data('BD/W54-031SSP','A')
    #remove_all()