from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import FileSystemStorage
from io import BytesIO
import json
# 測試東西 import一堆,之後整理
# Create your views here.

def home(request):
	return render(request, 'index.html')


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
		fs = FileSystemStorage()
		fileName = timeStrData+'_'+valueStrData+Extension
		fs.save(fileName,data)
	return render(request,'upload.html')
