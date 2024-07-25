import random
import webbrowser
import cv2
import requests
from PIL import Image


class AiPhotoBooth:
    def __int__(self):
        pass

    def RemoveBackround(self, imagename: str):

        url = "https://engine.prod.bria-api.com/v1/background/remove"

        payload = {}
        files = [
            ('file', (f'{imagename}.jpeg', open(f'ImageCache/{imagename}', 'rb'), 'image/jpeg'))
        ]
        headers = {
            'api_token': 'nuhuh'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        data = response.json()

        if data["result_url"] != None:
            # print(data["result_url"])
            return data["result_url"]
        else:
            return None

    def GenerateBackground(self, imageurl: str, userprompt: str):

        url = "https://engine.prod.bria-api.com/v1/background/replace"

        payload = {
            "bg_prompt": userprompt,
            "num_results": 1,
            "refine_prompt": True,
            "sync": True,
            "image_url": imageurl,
            "fast": True
        }

        headers = {
            "Content-Type": "application/json",
            "api_token": 'nuh uh'
        }

        response = requests.post(url, json=payload, headers=headers)

        data = response.json()

        imgJson = data["result"][0][0]


        imgSeed = data["result"][0][1]
        while not webbrowser.open(imgJson):
            print("loading")


        print("loading")
        while True:
            try:
                img = Image.open(fr"C:\Users\Crestview Robotics\Downloads\seed_{imgSeed}.png")
                break
            except:
                print("loading")



        try:

            img.save(f"GeneratedImages/userImage_seed_{imgSeed}.png")
        except:
            print("Error no file generated")

        return imgJson
    def TakePicture(self):
        cam_port = 0
        cam = cv2.VideoCapture(cam_port)
        while True:
            result, image = cam.read()

            if result:
                # saving image in local storage
                number = random.randint(1, 999999999)


                if cv2.imwrite(fr"ImageCache/userImage_{number}.jpeg", image):
                    print("saved")
                else:
                    print("not saved")

                return f"userImage_{number}.jpeg"

    def test(self):
        self.TakePicture()

    def run(self):
        picture = self.TakePicture()
        url = self.RemoveBackround(picture)#write code to take a picture
        prompt = str(input("enter prompt: "))
        image = self.GenerateBackground(url, prompt)


booth = AiPhotoBooth()
booth.run()
