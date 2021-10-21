"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

import config as cf
import model
import csv
import time

"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def initCatalog():
    return model.newCatalog()

# Funciones para la carga de datos
def loadData(catalog):
    loadArtists(catalog)
    loadArtWorks(catalog)

def loadArtWorks(catalog):
    artworksfile = cf.data_dir + 'MoMA/Artworks-utf8-large.csv'
    input_file = csv.DictReader(open(artworksfile, encoding = 'utf-8'))
    for artwork in input_file:
        model.addArtWork(catalog, artwork)
        model.addDepartment(catalog['department'], artwork)
        model.addNationality(catalog["nationality"], catalog["artists"], artwork)
        model.addArtworkDate(catalog["artworksdate"],artwork)

def loadArtists(catalog):
    artistsfile = cf.data_dir + "MoMA/Artists-utf8-large.csv"
    input_file = csv.DictReader(open(artistsfile, encoding= "utf-8"))
    for artist in input_file:
        model.addArtist(catalog,artist)
        model.addName(catalog, artist)
        model.addDate(catalog['artdate'],artist )

# Funciones de ordenamiento

def sortArtworksByDate(map, key):
    lst = model.onlyMapValue(map, key)
    model.sortArtworksByDate(lst, 'cmpArtworksByDate')

# Funciones de consulta sobre el catálogo
def artistByDate(catalog, date1, date2):
    #start_time = time.process_time()
    list =  model.getRange(catalog['artdate'], date1, date2)
    getSix = model.getSix(list[0])
    #stop_time = time.process_time()
    #print((stop_time - start_time)*1000)
    return list[1],getSix

def artworksByDate(artworksdate,artists,inicial,final):
    #start_time = time.process_time()
    data = model.getArtworksRange(artworksdate,inicial,final)
    uniqueArtists = model.countUniqueArtists(data[0],data[1])
    purchasedArtworks = model.getPurchasedArtworks(data[0],data[1])
    getSix = model.getSixArtWorks(data[0],artists)
    #stop_time = time.process_time()
    #print((stop_time - start_time)*1000)
    return (getSix,data[1],uniqueArtists,purchasedArtworks)

def obrasArtista(catalog, name):
    #start_time = time.process_time()
    info = model.onlyMapValue(catalog['names'], name)
    mapArtworks = model.artworksByArtist(catalog, info)
    #stop_time = time.process_time()
    #print((stop_time - start_time)*1000)
    return mapArtworks

def masAntic(map, len, medium):
    #start_time = time.process_time()
    sortArtworksByDate(map, medium)
    lst = model.getMapSubList(map,medium, len)
    #stop_time = time.process_time()
    #print((stop_time - start_time)*1000)
    for a in lst['elements']:
        print(a)

def natRank(nats,artists):
    #start_time = time.process_time()
    top10lst = model.top10lst(nats) 
    top10DataFrame = model.top10DataFrame(top10lst)
    topNat = model.getTopNationality(nats,top10lst,artists)
    topDataFrame = model.getSixArtWorks(topNat[2],artists)
    #stop_time = time.process_time()
    #print((stop_time - start_time)*1000)
    return (top10DataFrame,topDataFrame,topNat[0],topNat[1])

def costoDepartamento(catalog, department):
    #start_time = time.process_time()
    artworks = model.getArtworkByDep(catalog, department)
    to_print = model.getCost(artworks, catalog['artists'], department)
    #stop_time = time.process_time()
    #print((stop_time - start_time)*1000)
    return to_print
