from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import FileSystemStorage
import json
from django.conf import settings
from tensorflow.python.keras import backend as K
from tensorflow.python.keras.models import load_model
from tensorflow.python.keras.preprocessing import image
import numpy as np
import os


#model = load_model('capture/model/(300X300)model-resnet50-final.h5')

def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')



@csrf_exempt
def classifyResult(request):
	file_ = open(os.path.join(settings.BASE_DIR, 'test.txt'))
	f = file_.read()
	a = {'answer':f}
	return render(request,'classify.html',a)

@csrf_exempt
def predictResult(request):
	file_ = open(os.path.join(settings.BASE_DIR, 'test.txt'))
	f = file_.read()
	a = {'answer':f}
	return render(request,'predict.html',a)

@csrf_exempt
def upload(request):
	Extension = '.jpg'
	if request.method == 'POST':
		dictData = json.loads(request.POST.get('jsonData', ''))
		photoStrData = dictData['photoData']
		valueStrData = dictData['valueData']
		timeStrData = dictData['timeData']
		format, imgstr = photoStrData.split(';base64,')
		ext = format.split('/')[-1] 
		data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
		fs = FileSystemStorage(location='./media/photos')
		fileName = timeStrData+'_'+valueStrData+Extension
		fs.save(fileName,data)
	return render(request,'upload.html')


@csrf_exempt
def classify(request):
	Extension = '.jpg'
	if request.method == 'POST':
		model = load_model('capture/model/(300X300)model-resnet50-final.h5')
		dictData = json.loads(request.POST.get('jsonData', ''))
		photoStrData = dictData['photoData']
		timeStrData = dictData['timeData']
		format, imgstr = photoStrData.split(';base64,')
		cls_list = ['10', '100', '1000', '50', '500']
		ext = format.split('/')[-1]
		data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
		fs = FileSystemStorage(location='./media/predict')
		fileName = timeStrData+Extension
		fs.save(fileName,data)
		img_path = 'media/predict/'+fileName
		img = image.load_img(img_path, target_size=(300, 300))
		x = image.img_to_array(img)
		prex = np.expand_dims(x, axis = 0)
		print('predicting...')
		pred = model.predict(prex)[0]
		top_inds = pred.argsort()[::-1][:5]
		result = {}
		for i in top_inds:
		    result[int(pred[i]+0.5)] = cls_list[i]
		answer = {'ending':result[1]}
		file_ = open(os.path.join(settings.BASE_DIR, 'test.txt'),'w')
		file_.write(answer['ending'])
		file_.close()
		print(answer['ending'])
		return render(request,'classify.html')
	else:
		return render(request,'classify.html')


@csrf_exempt
def predict(request):
	Extension = '.jpg'
	if request.method == 'POST':
		model = load_model('capture/model/(withNg)model-resnet50-final.h5')
		dictData = json.loads(request.POST.get('jsonData', ''))
		photoStrData = dictData['photoData']
		timeStrData = dictData['timeData']
		format, imgstr = photoStrData.split(';base64,')
		cls_list = ['NG', 'OK']
		ext = format.split('/')[-1]
		data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
		fs = FileSystemStorage(location='./media/predict')
		fileName = timeStrData+Extension
		fs.save(fileName,data)
		img_path = 'media/predict/'+fileName
		img = image.load_img(img_path, target_size=(300, 300))
		x = image.img_to_array(img)
		prex = np.expand_dims(x, axis = 0)
		print('predicting...')
		pred = model.predict(prex)[0]
		top_inds = pred.argsort()[::-1][:5]
		result = {}
		for i in top_inds:
		    result[int(pred[i]+0.5)] = cls_list[i]
		answer = {'ending':result[1]}
		file_ = open(os.path.join(settings.BASE_DIR, 'test.txt'),'w')
		file_.write(answer['ending'])
		file_.close()
		print(answer['ending'])
		return render(request,'predict.html')
	else:
		return render(request,'predict.html')
	