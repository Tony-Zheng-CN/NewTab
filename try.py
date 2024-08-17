import os
import re
import json
import requests
from lxml import etree

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
REFERER = 'https://music.163.com/'
HOST = 'music.163.com'


def get_request_headers():
    return {
        'User-Agent': USER_AGENT,
        'Referer': REFERER,
        'Host': HOST
    }


def download_songs(url=None):
    if url is None:
        url = 'https://music.163.com/#/playlist?id=2384642500'

    url = url.replace('/#', '').replace('https', 'http')  # 对字符串进行去空格和转协议处理
    out_link = 'http://music.163.com/song/media/outer/url?id='
    headers = get_request_headers()

    try:
        res = requests.get(url=url, headers=headers).text
    except requests.RequestException as e:
        print(f"Failed to fetch the page: {e}")
        return

    tree = etree.HTML(res)

    song_list = tree.xpath('//ul[@class="f-hide"]/li/a')

    artist_name_tree = tree.xpath('//h2[@id="artist-name"]/text()')
    artist_name = artist_name_tree[0] if artist_name_tree else None

    song_list_name_tree = tree.xpath('//h2[contains(@class,"f-ff2")]/text()')
    song_list_name = song_list_name_tree[0] if song_list_name_tree else None

    folder = './' + (artist_name or song_list_name)

    if not os.path.exists(folder):
        os.makedirs(folder)

    for i, s in enumerate(song_list):
        href = s.xpath('./@href')[0]
        song_id = href.split('=')[-1]
        src = out_link + song_id
        title = s.xpath('./text()')[0]
        filename = title + '.mp3'
        filepath = os.path.join(folder, filename)

        if not os.path.exists(filepath):
            print(f'开始下载第{i + 1}首音乐：{filename}')
            try:
                data = requests.get(src, headers=headers).content
                with open(filepath, 'wb') as f:
                    f.write(data)
            except requests.RequestException as e:
                print(f"Failed to download the file: {e}")
        else:
            print(f'文件已存在，跳过下载：{filename}')

    print(f'{len(song_list)}首全部歌曲已经下载完毕！')


def download_lyric(song_name, song_id):
    url = f'http://music.163.com/api/song/lyric?id={song_id}&lv=-1&kv=-1&tv=-1'
    headers = get_request_headers()

    try:
        res = requests.get(url=url, headers=headers).text
        json_obj = json.loads(res)
        lyric = json_obj['lrc']['lyric']
        reg = re.compile(r'\[.*\]')
        lrc_text = re.sub(reg, '', lyric).strip()
        print(song_name, lrc_text)
    except (requests.RequestException, KeyError, json.JSONDecodeError) as e:
        print(f"Failed to download lyrics: {e}")


if __name__ == '__main__':
    music_list = 'https://music.163.com/#/playlist?id=7743939886'
    download_songs(music_list)
