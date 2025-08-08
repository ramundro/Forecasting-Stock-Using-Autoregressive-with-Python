import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import os
from statsmodels.tsa.ar_model import AR


#os.system('cls')

# Input Kode Emiten
namaStok = input('Masukkan Kode Emiten : ');

# Web Scrapping
url = 'https://finance.yahoo.com/quote/'+namaStok+'.JK/history?p='+namaStok+'.JK'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
hasil = [[] for k in range(2)]
errors = []

for tbody in soup.select('tbody'):
	i = 0
	for tr in tbody.select('tr'):
		j = 0
		for td in tr.select('td'):
			data = td.text
			if (j==0):
				dataTgl = data
			if (j==5):
				dataHarga = data.replace(',','').replace('-','0')

			j = j+1

		if (dataHarga != '0') :
			hasil[0].append(dataTgl)
			hasil[1].append(float(dataHarga))

		i = i + 1

hasil[0].reverse()
hasil[1].reverse()
dataTgl = hasil[0]
dataharga = hasil[1]

# Pecah Data
X = dataharga
test = X[len(X)-10:]
Y = dataTgl
testTgl = Y[len(Y)-10:]

for i in range(len(test)):
	train = X[0:len(X)-len(test)+i]
	model = AR(train)
	model_fit = model.fit()
	
	predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-i, dynamic=False)
	errors.append(abs(predictions[0]-test[i]))	
	print('Date=%s, predicted=%f, expected=%f, error=%f' % (testTgl[i], predictions[0], test[i], errors[i]))

train = X
model = AR(train)
model_fit = model.fit()
	
predictions = model_fit.predict(start=len(train), end=len(train)+1, dynamic=False)
print('==========================================')
print('Tomorrow => Forecast=%f' % (predictions[0]))

sumMAPE = 0
for i in range(len(errors)):
	sumMAPE = sumMAPE + (float(errors[i])*100/float(test[i]))

print("Accuration = {:.2f}".format(100-(sumMAPE/len(errors))))

// Finish




