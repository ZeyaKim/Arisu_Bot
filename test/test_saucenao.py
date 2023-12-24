import os
import enum
import io
import requests
from PIL import Image


class ImageSource(enum.Enum):
    PIXIV = 5
    DANBOORU = 9
    GELBOORU = 25
    TWITTER = 41


def convert_image_to_bytes(image_file):
    image = Image.open(image_file)
    image = image.convert('RGB')
    imageData = io.BytesIO()
    image.save(imageData, format='JPEG')
    imageData.seek(0)
    image_bytes = imageData.getvalue()
    imageData.close()
    return image_bytes


def search_from_saucenao(image_path):
    api_key = "42218dd95c8802cc066b761aed6f1a90aa15e58e"
    api_url = 'https://saucenao.com/search.php'
    payload = {
        'output_type': '2',
        'numres': '1',
        'minsim': '80',
        'api_key': api_key,
    }
    image_bytes = convert_image_to_bytes(image_path)
    files = {'file': ("image.jpg", image_bytes)}
    try:
        response = requests.post(api_url, files=files, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return
    return response.json()


script_dir = os.path.dirname(__file__)
test_images_dir = os.path.join(script_dir, '../images/test')
file_list = [name for name in os.listdir(test_images_dir)
             if os.path.isfile(os.path.join(test_images_dir, name))]
print(file_list)
while True:
    for index, file_name in enumerate(file_list):
        print(f"{index}: {file_name}")
    selected_index = int(input("Select index: "))
    info = search_from_saucenao(os.path.join(test_images_dir, file_list[selected_index]))

    results = info['results']
    results = [res for res in results if float(res['header']['similarity']) >= 80.0]
    idxs = [res['header']['index_id'] for res in results]

    if ImageSource.PIXIV.value in idxs:
        res = [res for res in results if res['header']['index_id'] == ImageSource.PIXIV.value][0]
        refined_res = {
            'Type': 'Pixiv',
            'Creator': res['data']['member_name'],
            'Source': res['data']['ext_urls'][0]}
    elif ImageSource.DANBOORU.value in idxs or ImageSource.GELBOORU.value in idxs:
        res = [res for res in results
               if res['header']['index_id'] == ImageSource.DANBOORU.value or
               res['header']['index_id'] == ImageSource.GELBOORU.value][0]
        refined_res = {
            'Type': 'Danbooru',
            'Creator': res['data']['creator'],
            'Source': res['data']['source']}
        if refined_res['Source'].startswith('https://i.pximg.net'):
            pix_id = refined_res['Source'].split('/')[-1]
            refined_res['Source'] = f"https://www.pixiv.net/artworks/{pix_id}"
    elif ImageSource.TWITTER.value in idxs:
        ...
