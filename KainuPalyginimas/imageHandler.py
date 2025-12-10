import os
import shutil
from Scraper import scrape_all_stores

def downloadImages(dict):

    folder_name = "temp"
    #os.system(f'curl -O "{link}"')

    try:
        os.makedirs(folder_name, exist_ok=True)
        print(f"Directory {folder_name} created")
    except Exception as e:
        print(f"Error creating directory: {e}")
    
    print("current directory: ", os.getcwd())
    os.chdir(f"{os.getcwd()}/{folder_name}")
    print("current directory: ", os.getcwd())

    #print(dict)
    #print(type(dict))
    #print(len(dict))

    for x in range (0, len(dict)):
        print(dict[x]["image"])
        if dict[x]["image"] != None:
            os.system(f'curl -O "{dict[x]["image"]}"')
            filename = dict[x]["image"].rsplit('/', 1)
            dict[x]["image"] = f"temp/{filename[1]}"
        else:
            print("None")

    print(dict)

    os.chdir('..')
    print("current directory: ", os.getcwd())

def deleteTemp():
    folder_name = "temp"

    try:
        #os.rmdir("temp")
        shutil.rmtree("temp")
        print(f"Directory {folder_name} deleted")
    except Exception as e:
        print(f"Error deleting directory: {e}")



if __name__ == "__main__":
    results = scrape_all_stores("duona")

    downloadImages(results)
    #deleteTemp()