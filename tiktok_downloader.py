import requests, os 

#https://www.tiktok.com/@geeks_osh/video/7312778740512197906
#https://www.tiktok.com/@geeks_osh/video/7312778740512197906?is_from_webapp=1&sender_device=pc&web_id=7289042945105217029

input_url = input('Ссылка на видео: ')
print(input_url)
split_url = input_url.split('/')
print(split_url)
current_id = split_url[5].split('?')[0]
print(current_id)
video_api = requests.get(f'https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/?aweme_id={current_id}').json()
# print(type(video_api))
video_url = video_api.get('aweme_list')[0].get('video').get('play_addr').get('url_list')[0]
print(video_url)
if video_url:
    video_id = video_api.get('aweme_list') [0].get('aweme_id')
    print("Начинаю скачивать видео...", video_id)
    try:
        os.mkdir('video')
    except:
        pass
    try:
        with open(f'video/{video_id}.mp4', 'wb') as video_file:
            video_file.write(requests.get(video_url).content)
            print(f"Видео{video_id} успешно скачан")
    except Exception as error:
        print(f"Ошибка: {error}")