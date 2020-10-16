from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.conf import settings
import datetime

from django.db.models import Sum
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *


# Create your views here.

@unauthenicated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            esAdmin = False
            rol = user.groups.all()
            for i in rol:
                if i.name == "Administrador":
                    esAdmin = True
            login(request, user)
            if esAdmin:
                return redirect('homeAdmin')
            else:
                return redirect('home')
        else:
            messages.info(request, 'Usuario o Contraseña incorrecta')

    return render(request, "login.html")

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def home(request):

    return render(request, "home.html")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Administrador'])
def homeAdmin(request):

    return render(request,"homeAdmin.html")

@login_required(login_url='login')
@allowed_users(allowed_roles=['Administrador'])
def ganancias(request):

    today = datetime.date.today()
    mes = today.month
    year = today.year
    totalVentas = 0
    totalPerdidas = 0

    if request.GET != {}:
        mes = request.GET["mes"]
        year = request.GET["year"]

    ventas = TransaccionesClientes.objects.values('Fecha','CostoTotal').annotate(Sum('CostoTotal')).filter(Fecha__month = int(mes)).filter(Fecha__year = int(year))
    perdidas = TransaccionesProbedores.objects.values('Fecha','CostoTotal').annotate(Sum('CostoTotal')).filter(Fecha__month = int(mes)).filter(Fecha__year = int(year))
    
    
    for i in ventas:
        totalVentas = totalVentas + i["CostoTotal"]

    for i in perdidas:
        totalPerdidas = totalPerdidas + i["CostoTotal"]
    
    yearFront = 0
    if year != "2020":
        yearFront = 1

    data = {"ventas":ventas, "perdidas":perdidas,"mes":mes, "year":yearFront, "totalVentas":totalVentas,"totalPerdidas":totalPerdidas}

    return render(request, "ganancias.html",data)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Trabajador', 'Administrador'])
def clientes(request):

    rol = request.user.groups.values_list('name', flat=True).first()
    
    if request.GET == {}:

        productos = Inventario.objects.all()
        mensaje = ""
        data = {"productos":productos,"mensaje":mensaje, "rol":rol}

        return render(request, "transaccionClientes.html", data)
    else:

        numeroProductos = request.GET["cantProd"]
        usuario = request.user

        for i in range(int(numeroProductos)):
            nomProd = "nomProd" + str(i)
            cant = "cant" + str(i)
            cantTotal = "cantTotal" + str(i)
            valNomProd = request.GET[nomProd]
            valCant = request.GET[cant]
            valCantTotal = request.GET[cantTotal]
            producto = Inventario.objects.get(id=valNomProd)

            if producto.Cantidad - int(valCant) >= 0:
                producto.Cantidad = producto.Cantidad - int(valCant)
                producto.save()
                transaccion = TransaccionesClientes(Usuario=usuario,Producto=producto,Cantidad=valCant,CostoTotal=valCantTotal)
                transaccion.save()
                mensaje = "Se ha realizado exitosamente la transaccion"
            else:
                mensaje = "No se cuenta con esa cantidad de productos en el inventario"

        productos = Inventario.objects.all()
        data = {"productos":productos,"mensaje":mensaje, "rol":rol}
        return render(request, "transaccionClientes.html", data)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Trabajador', 'Administrador'])
def provedores(request):

    rol = request.user.groups.values_list('name', flat=True).first()

    if request.GET == {}:

        productos = Inventario.objects.all()
        provedores = Probedor.objects.all()
        mensaje = ""
        datos = {"productos":productos, "provedores":provedores,"mensaje":mensaje, "rol":rol}

        return render(request, "transaccionProbedor.html", datos)
    
    else:

        usuario = request.user
        numeroProductos = request.GET["cantProd"]

        for i in range(int(numeroProductos)):
            prov = "prov" + str(i)
            nomProd = "nomProd" + str(i)
            cant = "cant" + str(i)
            cantTotal = "cantTotal" + str(i)
            valProv = request.GET[prov]
            valNomProd = request.GET[nomProd]
            valCant = request.GET[cant]
            valCantTotal = request.GET[cantTotal]
            provedor = Probedor.objects.get(id=valProv)
            producto = Inventario.objects.get(id=valNomProd)
            producto.Cantidad = producto.Cantidad + int(valCant)
            producto.save()
            transaccion = TransaccionesProbedores(Usuario=usuario, Probedor=provedor, Producto=producto, Cantidad=valCant, CostoTotal=valCantTotal)
            transaccion.save()
            mensaje = "Se ha realizado exitosamente la transaccion"


        productos = Inventario.objects.all()
        provedores = Probedor.objects.all()

        datos = {"productos":productos, "provedores":provedores,"mensaje":mensaje, "rol":rol}

        return render(request, "transaccionProbedor.html", datos)