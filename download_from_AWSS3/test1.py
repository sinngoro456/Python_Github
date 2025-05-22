# -*- coding: utf-8 -*-
{
    'method': 'POST'
    'body': {'user_id': '37f4aa98-2031-7033-d361-c120bc2bb604',
            'command': 'set',
            'writtenDateTime': '2025-03-14T13:43:48Z',
            'pins': [
                {
                    'pin_id': 'EFEB78EE-226C-48C1-A5E6-792418521405',
                    'date': '2025-03-14T13:33:47Z',
                    'title': '',
                    'latitude': 345328449037580,
                    'color': {'red': 0.5, 'green': 0, 'blue': 0.5, 'alpha': 1},
                    'category': '',
                    'description': '',
                    'user_id': '37f4aa98-2031-7033-d361-c120bc2bb604',
                    'longitude': 1335615233133332, 'images': '',
                    'tags': [], 'visibility': 'private'}]},
                    'headers': {'accept': '*/*', 'accept-encoding': 'gzip;q=1.0, compress;q=0.5', 'accept-language': 'ja-JP;q=1.0, ko-JP;q=0.9', 'Authorization': 'eyJraWQiOiIxVmFkanBub3o4Yzd3cEMzRGVpM0tiWVwvTFwvUG5hQzVKeGJQMTd6eHdMZFE9IiwiYWxnIjoiUlMyNTYifQ.eyJhdF9oYXNoIjoiQmgxZWVualJOZEpSNTlxSEtCbUU1USIsInN1YiI6IjM3ZjRhYTk4LTIwMzEtNzAzMy1kMzYxLWMxMjBiYzJiYjYwNCIsImNvZ25pdG86Z3JvdXBzIjpbImFwLW5vcnRoZWFzdC0xX2I5b2V5SUpnbV9Hb29nbGUiXSwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAuYXAtbm9ydGhlYXN0LTEuYW1hem9uYXdzLmNvbVwvYXAtbm9ydGhlYXN0LTFfYjlvZXlJSmdtIiwiY29nbml0bzp1c2VybmFtZSI6Imdvb2dsZV8xMTUxMzMwODI3NjU1NDU1MDE5NTkiLCJub25jZSI6Ilhwai0zaG1rWE1pNTNDNTBIel9pWnB5cjA0R3JSMUxtVngtYjE3YzVObnVGc0hlN1VFOGJwMmtSQUQ3NGVfb2M0US15dFZ4V3ZtZjAySDllalJzeEpwUVFEaWpld2pDcUtNamZlUWZETm8wazB3cmRGT25qYmZJZHVtWXlSUnlvS1N3bGM1YS1nTTRRT3JFYjhnRWd5Z0Yyb1FHYklRcVFyYmJ1b29LSjdlUSIsIm9yaWdpbl9qdGkiOiIyZTEwZDZmYi04MzJiLTRmNzUtYmY2Yi1hZjIzMzkxODFiNzkiLCJhdWQiOiI1c240azRhdmhnczFwNTNvdXRkczMxaDMzMCIsImlkZW50aXRpZXMiOlt7ImRhdGVDcmVhdGVkIjoiMTc0MTk1ODQ0MDY4OSIsInVzZXJJZCI6IjExNTEzMzA4Mjc2NTU0NTUwMTk1OSIsInByb3ZpZGVyTmFtZSI6Ikdvb2dsZSIsInByb3ZpZGVyVHlwZSI6Ikdvb2dsZSIsImlzc3VlciI6bnVsbCwicHJpbWFyeSI6InRydWUifV0sInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzQxOTU4NDUzLCJleHAiOjE3NDE5NjIwNTMsImlhdCI6MTc0MTk1ODQ1MywianRpIjoiN2ViNjljZDctYzhlYS00Mzg0LTk3OTgtZTI3N2Q5YmI2MDY5IiwiZW1haWwiOiJzaW5uZ29yb3U0NTZAZ21haWwuY29tIn0.dao-FB0EDGHWdKmhjn1T76vX44bZHfUUPfD9uGv-_poVnEWrCG0HirZNoG0mWZof9XgFlfDnDw1oOMNe9LpHeSA0r8xPTV66pC1tMicGZgcaLD1xC-HcouKWsbizYH8FCLDgVt8Udz3j9fP-EE4ZUYK24mX3d1t_UfWXm0VzBxfyeV09WLWuLp0p1ALog0pZbmzoTschfveb29GdRWdyOlOTpY2siWTf_rYwU3KSpfpZI-QnshdjtfrD34BILbNdumRO8g_M8eMmHw7WQEmGifVv_IAJGyQEy5xOygsTdsihdKzyxsKT8sX4jQ43ePe8ROduKaNmkqk9iHdup8kYdg',
    'content-type': 'application/json', 'Host': 'wz4q6hl5oa.execute-api.ap-northeast-1.amazonaws.com', 'User-Agent': 'MyGpsMap/1.0 (sinngoro456.MyGpsMap; build:1; iOS 16.7.10) Alamofire/4.9.1', 'X-Amzn-Trace-Id': 'Root=1-67d43294-3140fa4969ae9b1c0a51eb8b', 'X-Forwarded-For': '14.10.145.128', 'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'}}

import requests


def download_image_from_presigned_url(presigned_url: str) -> bytes:
    """
    Presigned URL から画像をダウンロードする関数

    :param presigned_url: 画像のダウンロード用 Presigned URL
    :return: 画像データ (バイナリ形式)。失敗時は None を返す。
    """
    try:
        # HTTP GET リクエストを送信
        response = requests.get(presigned_url)

        # ステータスコードが 200 の場合、画像データを返す
        if response.status_code == 200:
            return response.content
        else:
            # エラーレスポンスを表示
            print(f"Error: Invalid status code - {response.status_code}")
            print(f"Response Body: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        # ネットワークエラーを表示
        print(f"Error: Network request failed - {e}")
        return None


# 使用例
presigned_url = "https://mygpsmapdb.s3.amazonaws.com/67845a78-c061-704f-10a6-407ada615de3/726AF3FC-F712-47F1-9B41-F0FB534491D2?AWSAccessKeyId=ASIA6GBMF7EKKIKFHZNU&Signature=okTIYpxIjNdxBOtbVNvE8RDxBeM%3D&x-amz-security-token=IQoJb3JpZ2luX2VjEKH%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaDmFwLW5vcnRoZWFzdC0xIkcwRQIhAIfuQPK1RNJtTzq5RpMtPC5nfi5J%2BguC1B4HwLq3ktHvAiBFoaZy4Ry1R0zwfEeRryqoJOVf%2FlEiood0Ow9BHGTrcSr0Agjq%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDk3NTA1MDI0MjMyNCIMqiJoivaO2y%2BYq8wMKsgCMX1pAM%2BWtgoe3gR0%2FAaIs4YvRfYo9ktW5FnSuiKQFe3QIGKuXDbPNG9PN9KVGW84xA614OezhpykQc4LxYdEHZBg2kJKhWrJfWe2UYnkHvJ5%2B6YT08t%2FIdNXRg%2Fq%2FBBnDSFZC2PCPggoe6t%2FAH74nEOtYyp1dewtbsc80qO0RUxVQ56WAP8Vz%2FtvWLYhFAR8DMm8HxVWB74udS9pWPYA7tpvvbgGIBeJ8WpRtsHvAbAYpmRU2z4Jgh4C%2FGbLAV2jN4mwH2ybXWBiJ%2BOgSQ4Zz2jIBON5zrI3h4wqrHNU0UPy01oAveADOBPXlS2xKKMkX4NvVW18E51%2BKurZ8IcTWpdJhB6U2hBJ0qQ60PAsFu%2B1iXsA%2BQtOR8j2%2FnCmlqyIunbLUxuPZgOjVY6L5rVIVeKKkU0el0wYF4DiP9Y51e4foLQoipYeljDS4M%2B%2BBjqeASEWuCDYbso9f4tEcc79nnVGEqh4p60Wqkm1r6s73tiobNpwvb0yVBsKoEqJV0vrbOwcz4uk4tRhZGuPjMaVP2sYIyynKTAipFGnBjQOQbgTS82GOOPgpW7NasEelD3rXjjelq2mVH3IBbKmY2wqgUyu140E7XDuUPVqRdVWMDhRI%2B98fcPKYLoHQZPXTdaDraNbVYkGRf4sBLRuDXGp&Expires=1741943187"  # ここに Presigned URL を指定
image_data = download_image_from_presigned_url(presigned_url)

if image_data:
    # 画像データをファイルに保存
    with open("downloaded_image.jpg", "wb") as file:
        file.write(image_data)
    print("Image downloaded and saved successfully.")
else:
    print("Failed to download image.")
