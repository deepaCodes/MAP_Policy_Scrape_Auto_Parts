import requests

def get_page():



    url = "https://staging.surfair.com/mav2/admin/flights/flightschedule/upload-csv-schedule/"

    payload = {}
    headers = {
        'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': ' gzip, deflate, br',
        'Accept-Language': ' en-GB,en-US;q=0.9,en;q=0.8',
        'Cache-Control': ' max-age=0',
        'Connection': ' keep-alive',
        'Host': ' staging.surfair.com',
        'Sec-Fetch-Dest': ' document',
        'Sec-Fetch-Mode': ' navigate',
        'Sec-Fetch-Site': ' none',
        'Sec-Fetch-User': ' ?1',
        'Upgrade-Insecure-Requests': ' 1',
        'User-Agent': ' Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36',
        'Cookie': 'csrftoken=wsyGxJVfRcNuANVRVHIbNo7GGa4DxbQNrX7Eqdz5OiQUYt6bIKhKKGl1ywv8IWbP; sessionid=0q39adfeh3zfpuxgb83ygkrvegzr4t8m; ac_=oahEVHq_p1c7ep3P1SpAkLX_HxF3-Y4EYglg0zGgbBOnIbk0wpZ-7R2uuW3FeudXU5u8DOdIwmW11w59vA; oc_=Pw7Cjal6FJqYAT5-ttgVb3T7xxBnfLiYCBgEbJ1prwIwgnuxNvLJO4Fm1PMXqkSCElPjbHCnmFyYb_pAYw'
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
