
import requests
import cv2

class FoodInfoProvider:
    def get_product_nutriscore(self, ):
        product = self.readBarcode()
        url = f"https://world.openfoodfacts.org/api/v2/product/{product}"
        response = requests.get(url)
        data = response.json()
       
        if data["status"] == 1:
            nutriscore = data["product"]["nutriscore_data"]["grade"]
            print("test ex_date")
            print(data["product"])
        else:
            nutriscore = None
        return nutriscore
    
    def readBarcode(self):
        cap = cv2.VideoCapture(0)
        detector = cv2.barcode.BarcodeDetector()
        while True:
            _,img = cap.read()
            read,data,_, _= detector.detectAndDecode(img)
            if read:
                a = data[0]
                break
            cv2.imshow("produto", img)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()
        return a
    def getRecipe(self,recipe):
        recipe = recipe.replace(" ", "+")
        url = f"https://serpapi.com/search.json?q=receita+{recipe}&location=Aveiro+District,+Portugal&hl=pt&gl=pt&google_domain=google.pt&api_key=b900b243ffe51aa14f2804107ca563b207ec1a9ca0af8b0437e823abe1010100"
        response = requests.get(url)
        data = response.json()
        if data["search_metadata"]["status"] == "Success":
            if len(data["recipes_results"]) > 0:
                recipe_url = data["recipes_results"][0]["link"]
            else:
                recipe_url = None
        else:
            recipe_url = None
        return recipe_url