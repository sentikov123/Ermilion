import json

with open('C:/Users/Pavel/Desktop/iStepPython/Ermilion2/blog/main/services/result.json', encoding='utf-8') as file:
    x = file.read()

data = json.loads(x)
s = []
for i in data:
    if i['article_category'] not in s:
        s.append(i['article_category'])
print(s)