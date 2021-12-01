with open('urls.txt', 'r+', encoding='utf-8') as f:
    text = f.readlines()
    url = 'http://194.58.102.114'
    f.seek(0)
    for line in text:
        new_line = f'{url}{line}'
        f.write(new_line)
