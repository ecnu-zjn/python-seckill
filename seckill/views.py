# coding:utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from seckill.models import ExposedNoId,ExposedNoOpen,ExposedOpen
from seckill.models import Seckill,SuccessKilled
from seckill.serializers import SeckillSerializer
from seckill.serializers import SuccessKilledSerializer
import time
from getMd5 import getMd5
import json
import datetime


# Create your views here.

# class JSONResponse(HttpResponse):
#     """
#     """
#     def __init__(self,data,**kwargs):
#         content=JSONRenderer().render(data)
#         kwargs['content_type']='application/json'
#         super(JSONResponse,self).__init__(content,**kwargs)

@csrf_exempt
def SeckillList(request):
    """

    :param request:
    :return:
    """
    if request.method == 'GET':
        seckills=Seckill.objects.all()
        serializer=SeckillSerializer(seckills,many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data=JSONParser().parse(request)
        serializer=SeckillSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def seckill_detail(request,pk):
    """
    :param request:
    :param seckill_id:
    :return:
    """
    if pk == None:
        return HttpResponseRedirect("list")
    try:
        seckill=Seckill.objects.get(seckill_id=pk)
    except Seckill.DoesNotExist:
        return HttpResponseRedirect("list")

    if request.method == 'GET':
        serializer=SeckillSerializer(seckill)
        return JsonResponse(serializer.data)

@csrf_exempt
def seckill_time(request):
    if request.method == 'GET':
        now=time.time()
        now={"now":now}
        return JsonResponse(now)

@csrf_exempt
def expose_url(request,pk):
    if request.method == 'GET':

        seckill = Seckill.objects.get(seckill_id=pk)

        if seckill == None:
            return HttpResponse(json.dumps(ExposedNoId(False,pk).__dict__))

        now=datetime.datetime.fromtimestamp( time.time())
        start=seckill.start_time.replace(tzinfo=None)
        end=seckill.end_time.replace(tzinfo=None)
        print now,start,end
        if start > now or end < now:
            nowStr=now.strftime('%Y-%m-%d %H:%M:%S')
            staStr = start.strftime('%Y-%m-%d %H:%M:%S')
            endStr = end.strftime('%Y-%m-%d %H:%M:%S')
            return HttpResponse(json.dumps(ExposedNoOpen(False,pk,nowStr,staStr,endStr).__dict__))
        md5=getMd5(pk)
        return HttpResponse(json.dumps(ExposedOpen(True,pk,md5).__dict__))

@csrf_exempt
def set_phone(request):
    if request.method == 'POST':
        phone=request.POST.get('phone','')
        request.session['phone']=phone
        return HttpResponseRedirect('set ok.')
    else:
        return HttpResponse("set failure.")


@csrf_exempt
def killone(request):
    """
    :param request:
    :return:
    """
    if request.method == 'GET':
        successKilled=SuccessKilled.objects.all()
        serializer=SuccessKilledSerializer(successKilled,many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
            user_phone = long(request.POST.get('user_phone'))
            seckill_id = long(request.POST.get('seckill_id'))
            if seckill_id not in [i.seckill_id for i in Seckill.objects.all()]:
                print seckill_id==1000L
                print [i.seckill_id for i in Seckill.objects.all()]
                return HttpResponse('秒杀商品不存在')

            if user_phone==None:
                return HttpResponse('电话号码未输入')

            seckill = Seckill.objects.get(seckill_id=seckill_id)
            if datetime.datetime.fromtimestamp( time.time())<seckill.start_time.replace(tzinfo=None):
                return HttpResponse('还未开始')
            if datetime.datetime.fromtimestamp(time.time()) > seckill.end_time.replace(tzinfo=None):
                return HttpResponse('已经结束')

            idstr = [str(i.seckill_id) for i in SuccessKilled.objects.all()]
            phstr = [str(i.user_phone) for i in SuccessKilled.objects.all()]
            if str(user_phone)+str(seckill_id) not in [phstr[i]+idstr[i] for i in range(len(phstr))]:
                seckill.number=seckill.number-1
                seckill.save()
                obj=SuccessKilled(seckill_id=seckill_id, user_phone=user_phone,state=1,create_time=seckill.create_time)
                return HttpResponse('抢杀成功')
            else:
                return HttpResponse('重复秒杀')
