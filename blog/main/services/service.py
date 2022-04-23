import json



def base_filling():
    with open('C:/Users/Pavel/Desktop/iStepPython/Ermilion2/blog/main/services/result.json', encoding='utf-8') as file:
        x = file.read()
    s=[]
    data = json.loads(x)
    for i in data:
        if i['article_category'] not in s:
            s.append(i['article_category'])

    return s

print(base_filling())