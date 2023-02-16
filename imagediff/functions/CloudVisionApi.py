# import re
# import json
# import requests
import base64
# import os
# import SigmaWind.settings as settings
from google.cloud import vision

class CloudVisionApi:

    def run_text_detection(self, imgData):

        # 画像データの有無を確認
        if imgData is None: return 1, "撮影に失敗しています。"

        client = vision.ImageAnnotatorClient()
        img = base64.b64decode(imgData.replace("data:image/jpeg;base64,", ""))
        image = vision.Image(content=img)
        response = client.document_text_detection(image=image)

        return 0, response.full_text_annotation.text

    # URL = "https://vision.googleapis.com/v1/images:annotate?key="

    # def runTextDetection(self, key, imgData):

    #     # 画像データの有無を確認
    #     if imgData is None: return 1, "撮影に失敗しています。"
        
    #     # リクエストBody作成
    #     reqBody = json.dumps({
    #         "requests": [{
    #             "image": {
    #                 "content": re.search(r"base64,(.*)", imgData).group(1)
    #             },
    #             "features": [{
    #                 "type": "TEXT_DETECTION"
    #             }]
    #         }]
    #     })

    #     # リクエスト発行
    #     res = requests.post(self.URL + key, data=reqBody)

    #     # リクエストから画像情報取得
    #     resJson = res.json()
    #     tests = resJson['responses'][0]['textAnnotations']

    #     return 0, tests[0].get("description")