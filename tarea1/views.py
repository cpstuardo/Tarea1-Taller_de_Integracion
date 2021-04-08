from django.http import HttpResponse
from django.template.loader import get_template
import requests
from django.shortcuts import render

def inicio(request):
    return render(request, "inicio.html",{})

def temporadas(request):
    serie = request.GET["subject"]
    nombre_serie = serie.replace(" ", "+")
    response = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series='+ nombre_serie)
    todo = response.json()
    temporadas = []
    for elemento in todo:
        if not (elemento["season"] in temporadas):
            temporadas.append(elemento["season"])      
    return render(request, "temporadas.html",{"serie": serie, "temporadas": temporadas, "nombre_serie": nombre_serie})

def episodios(request, serie):
    nombre_serie = serie.replace("+", " ")
    temporada = request.GET["subject"]
    response = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes?series='+ serie)
    todo = response.json()
    episodios = []
    for elemento in todo:
        if elemento["season"] == temporada:
            episodios.append(elemento)
    return render(request, "episodios.html",{"serie": nombre_serie, "nombre_serie": serie, "episodios": episodios, "temporada": temporada})

def episodio(request):
    episodio_id = request.GET["subject"]
    response = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/episodes/'+ str(episodio_id))
    episodio = response.json()
    return render(request, "episodio.html", {"episodio": episodio[0]})

def personaje(request):
    personaje = request.GET["subject"]
    personaje_nombre = personaje.replace(" ", "+")
    response = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?name='+ personaje_nombre)
    personaje = response.json()
    return render(request, "personaje.html", {"personaje": personaje[0]})

def citas(request):
    personaje = request.GET["subject"]
    personaje_nombre = personaje.replace("+", " ")
    response = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/quote?author='+ personaje)
    citas = response.json()
    return render(request, "citas.html", {"citas": citas, "autor": personaje_nombre})

def personajes(request):
    buscado = request.GET["subject"] 
    buscado_plus =buscado.replace(" ", "+")
    response = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?name='+ buscado_plus)
    personajes = response.json()
    if buscado == " ":
        i = 10
        response2 = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?' + f'?limit=10&offset={i}')
        lista = response2.json()
        while lista != []:
            personajes += lista
            i += 10
            response2 = requests.get('https://tarea-1-breaking-bad.herokuapp.com/api/characters?' + f'?limit=10&offset={i}')
            lista = response2.json()
    return render(request, "personajes.html", {"personajes": personajes, 'buscado': buscado})