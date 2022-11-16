import urllib.request
response = urllib.request.urlopen('http://naver.com')
print(response.read())