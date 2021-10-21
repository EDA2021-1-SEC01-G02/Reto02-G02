"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import controller
import config as cf
import sys
import controller
from DISClib.ADT import list as lt
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar artistas nacidos en un rango de años.")
    print("3- Consultar obras hechas en un rango de fechas.")
    print("4- Organizar las obras de un artistas por medios/tecnicas.")
    print("5- Consultar el ranking de obras por nacionalidades.")
    print("6- Consultar el costo de transporte de un departamento especifico.")

catalog = None

def initCatalog():
    return controller.initCatalog()

def loadData(catalog):
    controller.loadData(catalog)

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog = initCatalog()
        loadData(catalog)
        num_artworks = lt.size(catalog['artworks'])
        print('Artworks cargados: ' + str(num_artworks))
        num_artists = lt.size(catalog["artists"])
        print("Artistas cargados: " + str(num_artists))
        
    elif int(inputs[0]) == 2:
        print("\nBuscando en un rango de fechas: ")
        initialDate = input("Año inicial del rango: ")
        finalDate = input("Año final del rango: ")
        to_print = controller.artistByDate(catalog, initialDate,finalDate)
        for item in to_print:
            print(item)

    #Requerimiento 2
    elif int(inputs[0]) == 3:
        initialDate = input("Fecha Inicial (YYYY-MM-DD): ")

        finalDate = input("Fecha Final (YYYY-MM-DD): ")

        temp = controller.artworksByDate(catalog["artworksdate"],catalog["artists"],initialDate,finalDate)
        print("\nEl MoMA adquirio %s piezas unicas entre los dias %s y %s, con %s artistas distintos y compro %s de estas obras" %(temp[1],initialDate,finalDate,temp[2],temp[3]))
        print("Los primeros y ultimos 3 artistas en este rango son:")
        print(temp[0])

    elif int(inputs[0]) == 4:
        name =  input('Digite el nombre del artista a buscar: ')
        to_print = controller.obrasArtista(catalog, name)
        for item in to_print:
            print(item)

    #Requerimiento 4
    elif int(inputs[0]) == 5:
        temp = controller.natRank(catalog["nationality"],catalog["artists"])
        print("TOP 10 Nacionalidades:")
        print(temp[0])
        print("La nacionalidad TOP en el museo es %s con %s piezas unicas." %(temp[2],temp[3])) 
        print("Los primeros y ultimos 3 objetos en la lista de trabajos %s son: " %(temp[2]))
        print(temp[1])
    
    elif int(inputs[0]) == 6:
        departamento = input('Digite el departamento a consultar: ')
        to_print = controller.costoDepartamento(catalog, departamento)
        for item in to_print:
            print(item)
        

    else:
        sys.exit(0)
sys.exit(0)