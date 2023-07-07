from django.shortcuts import render
from django.http import JsonResponse
import json
from django.core import serializers

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import numpy as np
import pandas as pd 
from .models import *
#from ..core.models import *



@method_decorator(csrf_exempt)
def Dashboard(request,*args, **kwargs):
    if request.method == 'GET':
        #Calculando Entradas y Salidas globales.
        total_ingresos = Ingreso.objects.filter(owner=request.user).aggregate(total=Sum('cantidad'))
        suma_ingresos = total_ingresos['total'] if total_ingresos['total'] else 0
        total_egreso = Gasto.objects.filter(owner=request.user).aggregate(total=Sum('cantidad'))
        suma_egresos = total_egreso['total'] if total_egreso['total'] else 0
        
        ## Last Egresos y Last Ingresos
        #Last_Egresos = Gasto.objects.all()[:10]
        Last_Egresos = list(Gasto.objects.filter(owner=request.user).values()[:30])
        Last_Ingesos = list(Ingreso.objects.filter(owner=request.user).values()[:30])
        
        ## TimeLine
        TLE = Gasto.objects.filter(owner=request.user).values('fecha','cantidad','descripcion','categoria__nombre','date_create','date_time_c','status')
        TLI = Ingreso.objects.filter(owner=request.user).values('fecha','cantidad','descripcion','categoria__nombre','date_create','date_time_c','status')
        TLP = PagoMensual.objects.filter(owner=request.user).values('fecha_vencimiento','cantidad','descripcion','categoria__nombre','date_create','date_time_c','status')
        CAT = Categoria.objects.filter(owner=request.user).order_by('nombre').values()
        
        
        TLF = []
        for i in TLE:
            TLF.append({
                'fecha':i['fecha'],
                'date_create':i['date_create'],
                'date_time_c':i['date_time_c'],
                'cantidad':float(i['cantidad']),
                'descripcion':i['descripcion'],
                'categoria':i['categoria__nombre'],
                'tipo':'Egreso',
                'color':'red',
                'icon': 'mdi-thumb-down',
                'status':i['status']
            })
        for i in TLI:
            TLF.append({
                'fecha':i['fecha'],
                'date_create':i['date_create'],
                'date_time_c':i['date_time_c'],
                'cantidad':float(i['cantidad']),
                'descripcion':i['descripcion'],
                'categoria':i['categoria__nombre'],
                'tipo':'Ingreso',
                'color':'green',
                'icon':'mdi-thumb-up',
                'status':i['status']
            })
        for i in TLP:
            TLF.append({
                'fecha':i['fecha_vencimiento'],
                'date_create':i['date_create'],
                'date_time_c':i['date_time_c'],
                'cantidad':float(i['cantidad']),
                'descripcion':i['descripcion'],
                'categoria':i['categoria__nombre'],
                'tipo':'Programado',
                'color':'grey',
                'icon':'mdi-currency-usd',
                'status':i['status']
            })
        #TLFOrdered = sorted(TLF, key=lambda x: (x['fecha'] , x['date_time_c']) )
        #TLF_ordered = sorted(TLF, key=lambda x: (x['date_create'], x['date_time_c']))
        import datetime
        fecha_actual = datetime.date.today()
        hora_actual = datetime.datetime.now().time()
        TLF.append({
            'fecha':fecha_actual,
            'date_create':fecha_actual,
            'date_time_c':hora_actual,
            'cantidad':0,
            'descripcion':'Ahorra tu dinero 😓 ',
            'categoria':'Linea',
            'tipo':'Ingreso',
            'color':'purple',
            'icon':'mdi-hand-heart',
            'status':True
        })
        
        TLF_ordered = sorted(TLF, key=lambda x: (x.get('fecha'), x.get('date_time_c')), reverse=True)
        
        ## Lista de Categorias
        
        
        
        Exportacion = []
        Exportacion.append({
            'Ingresos':suma_ingresos - suma_egresos,
            'Egresos':suma_egresos,
            'Last_Egresos':Last_Egresos,
            'Last_Ingesos':Last_Ingesos,
            'TLF':TLF_ordered,
            'Categoria': list(CAT),
            
        })
        
        
        
        return JsonResponse(Exportacion,safe=False)
    
    


@method_decorator(csrf_exempt)
def registro(request,*args, **kwargs):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print(body)
        if body['tipo'] == 'Ingreso':
            i = Ingreso()
            i.categoria = Categoria.objects.get(pk=int(body['categoria'])) 
            i.descripcion = body['descripcion']
            i.fecha= body['fecha']
            i.cantidad=body['cantidad']
            i.owner = request.user
            i.save()
            
        if body['tipo'] == 'Egreso':
            i = Gasto()
            i.categoria = Categoria.objects.get(pk=int(body['categoria'])) 
            i.descripcion = body['descripcion']
            i.fecha= body['fecha']
            i.cantidad=body['cantidad']
            i.owner = request.user
            i.save()
        if body['tipo'] == 'Agendado':
            i = PagoMensual()
            i.categoria = Categoria.objects.get(pk=int(body['categoria'])) 
            i.descripcion = body['descripcion']
            i.fecha_vencimiento= body['fecha']
            i.cantidad=body['cantidad']
            i.owner = request.user
            i.save()
        return JsonResponse({'Hola':'Hola'},safe=False)
        
           