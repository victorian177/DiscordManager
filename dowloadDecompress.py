import gdown

url = 'https://drive.google.com/uc?id=1rayup1_O0MPb-r6oT2pt-dWEttIsXVfFFOzHsI_NaR0'
output = 'responses.xlsx'
gdown.download(url, output, quiet=False)