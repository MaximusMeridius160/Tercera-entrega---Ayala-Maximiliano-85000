import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt 
import io
import base64
from .models import *
from django.db.models import Sum


def grafico_pedidos():
    nuevos = PedidosProv.objects.filter(tipo="nuevo").count()
    existentes = PedidosProv.objects.filter(tipo="existente").count()

    labels = ['Nuevos', 'Existentes']
    valores = [nuevos, existentes]

    #crear grafico
    plt.figure()
    plt.bar(labels,valores)
    plt.close

    #guardar en memoria
    buffer = io.BytesIO()
    plt.savefig(buffer,format='png')
    buffer.seek(0)

    #convertir a base64

    imagen_png= buffer.getvalue()
    grafico_barras= base64.b64encode(imagen_png).decode('utf-8')
    buffer.close
    
    return grafico_barras

def grafico_ventas():
    venta = (Venta.objects.values('fecha').annotate(total=Sum('cantidad')).order_by('fecha'))
    fechas =[v['fecha'].strftime('%d/%m') for v in venta]
    totales = [v['total'] for v in venta]

    plt.figure()
    plt.plot(fechas,totales,marker='o')
    plt.title("Ventas por día")
    plt.xlabel("Fecha")
    plt.ylabel("Cantidad")
    plt.xticks(rotation=45)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)

    grafico_linea = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    return grafico_linea