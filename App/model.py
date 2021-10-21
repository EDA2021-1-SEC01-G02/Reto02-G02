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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

from DISClib.DataStructures.chaininghashtable import keySet
import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa 
from DISClib.Algorithms.Sorting import mergesort as ms 
import pandas as pd
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    """ Inicializa el catálogo de obras

    Crea una lista vacia para guardar las obras

    Se crean indices para los mediums

    Retorna el catalogo inicializado.
    """
    catalog = {'artworks': None,
               "artists" : None,
               'medium': None,
               "nationality": None,
               }

    catalog['artworks'] = lt.newList('ARRAY_LIST', compareArtworks)

    catalog['artists'] = mp.newMap(2000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=None)

    catalog['names'] = mp.newMap(2000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=None)

    catalog['department'] = mp.newMap(34500,
                                maptype='CHAINIING',
                                loadfactor=2,
                                comparefunction=None)

    catalog["nationality"] = mp.newMap(34500,
                                maptype='CHAINING',
                                loadfactor=2,
                                comparefunction=None)  

    catalog['artdate'] =  mp.newMap(2000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=None)
    
    catalog['artworksdate'] =  mp.newMap(2000,
                                maptype='PROBING',
                                loadfactor=0.5,
                                comparefunction=None)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtWork(catalog, artwork):
    """
        Añade artworks
    """
    lt.addLast(catalog['artworks'], artwork)

def addName(catalog, artist):
    artists =  catalog['names']
    artistName =  artist['DisplayName']
    if not mp.contains(artists,artistName) and artistName != '':
        mp.put(artists, artistName,artist)

def addArtist(catalog, artist):
    """
        Añade artistas
    """
    artists =  catalog['artists']
    artistCode =  artist['ConstituentID']
    if not mp.contains(artists,artistCode):
        mp.put(artists, artistCode,artist)

def addDepartment(departments, artwork):
    """
    Añade mediums al mapa de Mediums y agrega artworks a una lista que tiene como valor
    """
    departmentName = artwork['Department']
    if not mp.contains(departments, departmentName):
        mp.put(departments, departmentName, lt.newList('ARRAY_LIST', None))
    art = onlyMapValue(departments,departmentName)
    lt.addLast(art, artwork)

def addDate(dates, artist):
    """
    Añade mediums al mapa de Mediums y agrega artworks a una lista que tiene como valor
    """
    artistDate = artist['BeginDate']
    if not mp.contains(dates, artistDate):
        mp.put(dates, artistDate, lt.newList('ARRAY_LIST', None))
    art = onlyMapValue(dates,artistDate)
    lt.addLast(art, artist)

def addArtworkDate(artworksDates, artwork):
    """
    Añade artworks al mapa de fechas para artworks y agrega artworks a una lista que tiene como valor
    """
    artworkDate = artwork['DateAcquired']
    if not mp.contains(artworksDates, artworkDate):
        mp.put(artworksDates, artworkDate, lt.newList('ARRAY_LIST', None))
    date = onlyMapValue(artworksDates,artworkDate)
    lt.addLast(date, artwork)

def addNationality(nationalities, artists, artwork):
    """
    Añade nacionalidades al mapa de Nationality y agrega artworks a una lista que tiene como valor
    """
    artistid = artwork["ConstituentID"].split(",")
    
    for i in artistid:
        i = i.strip("[").strip("]").strip()
        if i != "":
            artistnat = getArtistNationality(str(i),artists) #Posiblemente haya que crear una funcion que recorra la lista y adquiera la nacionalidad
            if artistnat != None: #Si encontro el artista
                if (artistnat == ""): 
                    artistnat = "Nationality unknown"
                if mp.contains(nationalities, artistnat) == False:
                    mp.put(nationalities, artistnat, lt.newList('ARRAY_LIST', None))
                art = onlyMapValue(nationalities, artistnat)
                lt.addLast(art, artwork)
    
# Funciones para creacion de datos
def calCost(dimensions):
    pri2 = 0
    peso = 0
    if dimensions[3] != '':
        if float(dimensions[3]) > 0:
            peso = 72 * float(dimensions[3])

    if dimensions[0] == '' or dimensions[1] == '':
        pri1 = 0
    else:
        pri1 = (float(dimensions[0]) * float(dimensions[1]))/10000
    if dimensions[2] != '' and pri1 != 0:
        if float(dimensions[2]) > 0:
            pri2 = ((pri1 * float(dimensions[2]))/100)

    if pri1 > 0 :
        pri1 =  72 * float(pri1)
    if pri2 > 0:
        pri2 = 72 * float(pri2)
    
    tup =  pri1,pri2, peso
    fin = max(tup)
    if fin > 0:
        return fin
    else:
        return 48

def agregarTabla(list, artists):
    artStr = { }
    
    for pos in range(1, 6): 
        temp = lt.getElement(list, pos)
        artista =  getArtistsByCode(temp['ConstituentID'], artists)
        artStr[pos] = temp['ObjectID'],temp['Title'],temp['Medium'], temp['Date'],artista,temp['cost'],temp['Classification'], temp['URL'] 
    return  (pd.DataFrame.from_dict(artStr, orient='index', columns= ['ObjaectID', 'Title', 'Medium', 'Date', 'Artists', 'TranCost (USD)', 'Classification', 'URL']))

def crearStr(map,consID, leng, medium ):
    temp = medium
    stri = 'Louise Bourgeois con id de MoMa %s tiene %s obras a su nombre en el museo\n' %(consID, leng)
    stri += 'Hay %s diferentes medios/tecnicas en su trabajo\n' %(mp.size(map))
    stri += 'Medio/Tecnica' + 31 * ' ' + 'Conteo\n'
    if lt.size(medium) < 6 :
        fin = lt.size(medium)
    else:
        fin = 6
    for pos in range(1, fin):
        temp = lt.getElement(medium ,pos)
        stri +=  temp[0] +   ' '* (50 - (len(temp[0] + str(temp[1])))) + str(temp[1]) + '\n'
        
    stri += 'Tres ejemplos de %s en la coleccion son:' %(lt.firstElement(medium )[0])
    return stri

def top10lst (nationalities):
    """
    Extrae las nacionalidades y el numero de obras para organizarlas y sacar el top 10 en forma de lista
    """
    data = lt.newList("ARRAY_LIST",None) #Lista en donde se almacenaran la nacionalidad y el numero de obras
    nats = mp.keySet(nationalities) #Para recorrer el map de nacionalidades, viene en forma de lista
    
    for pos in range(lt.size(nats)+1): #Recorre nacionalidades
        nat = lt.getElement(nats,pos) #Obtiene una nacionalidad de la lista de nacionalidades
        temp = onlyMapValue(nationalities,nat) #Obtiene los valores de la nacionalidad
        lt.addLast(data,{"Nacionalidad":nat,"Numero":lt.size(temp)})
    ms.sort(data,cmpNationalitiesByArtworks)
    result = lt.subList(data,1,10)
    return result

def top10DataFrame (lst):
    """
    Convierte la lista de top 10 en un DataFrame para mostrar
    """
    data = {}
    for pos in range(0, 10):
        temp = lt.getElement(lst, pos)
        data[pos] = temp['Nacionalidad'], temp["Numero"]
    return pd.DataFrame.from_dict(data,orient = "index",columns=["Nationality","ArtWorks"])

# Funciones de consulta

def getRange(map, date1, date2):
    #Obtiene los artistas segun un rango
    list = lt.newList('ARRAY_LIST', None)
    for date in range(int(date1), int(date2)+1):
        date =  str(date)
        if mp.contains(map,date):
            temp = onlyMapValue(map, date)
            for pos in range(1, lt.size(onlyMapValue(map, date))+1 ):
                lt.addLast(list, lt.getElement(temp, pos))
    ms.sort(list, sortDateAr)
    str1 = 'Hay %s artistas nacidos entre %s y %s' %(lt.size(list), date1, date2)
    return list, str1

def getArtworksRange(map, date1, date2):
    """
    Obtiene los artworks segun un rango de fechas #TODO: Arreglar para que funcione con fechas y no como numeros de ser posible
    """
    date1 = date1.replace("-","")
    date2 = date2.replace("-","")

    list = lt.newList('ARRAY_LIST', None)
    for date in range(int(date1), int(date2)+1):
        date = str(date)
        date = date[:4]+"-"+date[4:6]+"-"+date[6:8]
        if mp.contains(map,date):
            temp = onlyMapValue(map, date)
            for pos in range(1, lt.size(onlyMapValue(map, date))+1 ):
                lt.addLast(list, lt.getElement(temp, pos))
    ms.sort(list, cmpArtworkByDateAdquired)
    return (list,lt.size(list))

def countUniqueArtists(artworks,artworksSize):
    """
    Recorrera las obras en el rango y contara el numero de artistas. Solo una vez por artista
    """

    temp = lt.newList('ARRAY_LIST', None)
    
    for i in range(1,artworksSize+1):
        artwork = lt.getElement(artworks,i)
        artistsTemp = artwork['ConstituentID'].split(',')
        for artist in artistsTemp:
            artist = artist.strip().strip('[').strip(']')
            lt.addLast(temp,artist)
                
    return lt.size(temp)

def getPurchasedArtworks(artworks,artworksSize):
    """
    Retorna la cantidad de obras que hayan sido compradas
    """
    resultado = 0

    for i in range(0,artworksSize+1):
        artwork = lt.getElement(artworks,i)
        artworkTemp = artwork['CreditLine'].lower()
        artworkTemp = artworkTemp.split(' ')
        if "purchase" in artworkTemp:
            resultado += 1
    return resultado


def getSix(list):
    #Saca los primeros 3 y los ultimos 3 elementos de la lista
    size = lt.size(list)+1
    dict = {}
    for pos in range(1,4):
        temp = lt.getElement(list, pos)
        dict[pos] = temp['ConstituentID'], temp['DisplayName'],temp['BeginDate'], temp['Nationality'], temp['Gender'],temp['ArtistBio'], temp['Wiki QID'],temp['ULAN']
    for pos in range(size-4, size):
        temp = lt.getElement(list, pos)
        dict[pos] = temp['ConstituentID'], temp['DisplayName'],temp['BeginDate'], temp['Nationality'], temp['Gender'],temp['ArtistBio'], temp['Wiki QID'],temp['ULAN']
    to_print = pd.DataFrame.from_dict(dict, orient = 'index',columns=['ConstituentID', 'DisplayName', 'BeginDate', 'Nationality', 'Gender', 'ArtistBio','Wiki QID', 'ULAN'])
    return to_print

def getSixArtWorks(list,artists):
    """
    Saca los primeros 3 y los ultimos 3 elementos de la lista, usado en el requerimiento de obras por fecha y de nacionalidades 
    """
    size = lt.size(list)+1
    dict = {}
    for pos in range(1,4):
        temp = lt.getElement(list, pos)
        artistsTemp = getArtistsByCode(temp["ConstituentID"],artists)
        dict[pos] = temp['ObjectID'], temp['Title'], artistsTemp, temp['Medium'], temp['Date'], temp['Dimensions'], temp['Department'], temp['Classification'], temp['URL']
    for pos in range(size-3, size):
        temp = lt.getElement(list, pos)
        artistsTemp = getArtistsByCode(temp["ConstituentID"],artists)
        dict[pos] = temp['ObjectID'], temp['Title'], artistsTemp, temp['Medium'], temp['Date'], temp['Dimensions'], temp['Department'], temp['Classification'], temp['URL']
    to_print = pd.DataFrame.from_dict(dict, orient = 'index',columns=['ObjectID',"Title","ArtistsNames","Medium","Date","Dimensions","Department","Classification","URL"])
    return to_print

def artworksByArtist(catalog, info):
    #Saca las obras por artistas
    consID =  info['ConstituentID']
    artworksList = getArtWorksList(catalog['artworks'], consID)
    tecs = (mp.keySet(artworksList))
    list =  lt.newList('ARRAY_LIST', None)
    leng = 0
    for pos in range(0,lt.size(tecs)+1):
        temp =  lt.getElement(tecs, pos)
        size = lt.size(onlyMapValue(artworksList, temp))
        tup = temp, size
        if lt.isPresent(list, tup) == 0:
            lt.addLast(list, tup)
            leng += size
    ms.sort(list,compareAlf)
    ms.sort(list, compareCont)
    artworks =  onlyMapValue(artworksList, lt.firstElement(list)[0])
    
    stri = crearStr(artworksList,consID, leng, list )
    
    artStr = {}
    for pos in range(1,lt.size(artworks)+1):
        temp =  lt.getElement(artworks, pos)
        artStr[pos] = temp['ObjectID'],temp['Title'],temp['Medium'], temp['Date'],temp['DateAcquired'],temp['Department'],temp['Classification'], temp['URL'] 
    data = pd.DataFrame.from_dict(artStr, orient= 'index', columns=['ObjaectID', 'Title', 'Medium', 'Date', 'DateAcquired', 'Department', 'Classification', 'URL' ])
    return stri, data

def getArtWorksList(artworks , consID):

    map = mp.newMap(15223,
                    maptype='PROBING',
                    loadfactor=0.5,
                    comparefunction=None)
    
    size = lt.size(artworks)
    for pos in range(1, size+1):
        temp = lt.getElement(artworks,pos)
        new = temp['ConstituentID'].split(',')
        for item in new:
            if item.strip().strip('[').strip(']')  ==  consID:
                addMedium(map, temp)
                break

    return map
    
def addMedium(mediums, artwork):
    """
    Añade mediums al mapa de Mediums y agrega artworks a una lista que tiene como valor
    """
    mediumName = artwork['Medium']
    if not mp.contains(mediums, mediumName):
        mp.put(mediums, mediumName, lt.newList('ARRAY_LIST', None))
    art = onlyMapValue(mediums,mediumName)
    lt.addLast(art, artwork)

def onlyMapValue(map, key):
    # Dado un mapa y una llave, retorna el valor de la pareja
    """
    Se encarga de buscar el valor de un par, dado el mapa y la llave
    """
    pair =  mp.get(map,key)
    return me.getValue(pair)

def getMapSubList(map,medium, len):
    """
    Crea una sublista a partir de los elementos de una lista que hay almacenada en una pareja en el mapa.
    """
    lst = onlyMapValue(map, medium)
    new = lt.subList(lst,1,len)
    return new

def getArtistNationality(artistid,artists):
    """
    Recibe por parametro el ID del artista junto con el info de los artistas y devuelve su nacionalidad
    """
    result = None #Nacionalidad del artista. Se mantendra vacio si no lo encuentra
    if mp.contains(artists,artistid): #Revisa que si exista el id
        temp = onlyMapValue(artists,artistid) #Accede a los registros
        tempid = temp["ConstituentID"]
        if int(tempid) == int(artistid): #Compara los ID
            result = temp["Nationality"] #Toma la nacionalidad
    return result

def getTopNationality(nationalities,topNats,artists):
    topNat = lt.getElement(topNats,1)
    topNat = topNat["Nacionalidad"]
    topNum = 0
    lst = onlyMapValue(nationalities,topNat)
    for artwork in range(0,lt.size(lst)):
        artwork = lt.getElement(lst,artwork)
        unique = True
        artistsID = artwork["ConstituentID"]
        artistsID = artistsID.strip().strip('[').strip(']').replace(" ","")
        artistsID = artistsID.split(",")
        for artistID in artistsID:
            artistInfo = onlyMapValue(artists,artistID)
            if artistInfo["Nationality"] != topNat:
                unique = False
                break
        if unique:
            topNum += 1
    topLst = onlyMapValue(nationalities,topNat)
    return (topNat,topNum,topLst)
        

def getNationalityArtworksNumber(nationalities,nationality):
    """
    Obtiene la nacionalidad en str y el map de nacionalidades. Retorna el numero de obras en esa nacionalidad.
    """
    result = None
    if mp.contains(nationalities, nationality) == True:
        temp = mp.get(nationalities,nationality)
        result = lt.size(temp["value"])
    return result
    

def getArtworkByDep(catalog, department):
    artworks = onlyMapValue(catalog['department'], department)
    return artworks

def getCost(artworks, artists, department):
    list =  lt.newList('ARRAY_LIST', None)
    total = 0
    peso = 0
    for pos in range(1, lt.size(artworks)+1):
        temp = lt.getElement(artworks,pos)
        dimensions =  temp["Height (cm)"],temp["Width (cm)"], temp["Depth (cm)"], temp["Weight (kg)"]
        price = calCost(dimensions)
        total += price
        if temp["Weight (kg)"] != '':
            peso += float(temp["Weight (kg)"])

        temp['cost'] = price
        lt.addLast(list, temp)
    cont2 = 0 
    for pos in range(1, lt.size(list)+1):
        temp = lt.getElement(list, pos)
        cont2 += float(temp['cost'])
    ms.sort(list, sortCost)
    tabla = agregarTabla(list,artists)
    oldList = lt.newList('ARRAY_LIST')
    for pos in range(1,lt.size(list)+1):
        if lt.getElement(list,pos)['Date'] != '':
            lt.addLast(oldList,lt.getElement(list,pos))
    ms.sort(oldList, sortDate)
    tablaOld = agregarTabla(oldList, artists)
    str2 = 'El MoMa va a transportar %s artefactos de %s.\n RECUERDA!! No todos los datos del MoMa estan completos, esta es una aproximacion.\n Peso estimado: %s\n Costo total estimado: %s \n El top 5 de las obras mas caras.'%(str(lt.size(list)), department, str((peso)),str( total))
    
    return str2, tabla,'Las cinco obras mas viejas', tablaOld
  
def getArtistsByCode(temp, artists):
    #Saca los artistas segun su codigo
    str = ''
    temp =  temp.split(',')
    for item in temp:
        name = onlyMapValue(artists, item.strip().strip('[').strip(']'))['DisplayName']
        str += name + ', '

    return str


# Funciones utilizadas para comparar elementos dentro de una lista
def compareArtworks(artwork1, artwork2):
    """
    Compara los codigos de los Artworks
    """
    id1 = artwork1['ObjectID'] 
    id2 = artwork2['ObjectID']
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareArtists(artist1, artist2):
    """
    Compara los codigos de los artistas
    """
    id1 = artist1["ConstituentID"]
    id2 = artist2["ConstituentID"]
    if (id1==id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareMediumNames(name, medium):

    """
    Compara los nombres de los Mediums,
    devuelve 0 si son iguales, 
    1 si el primero es mayor y 
    -1 si es al reves
    """
    tagentry = me.getKey(medium)
    if (name == tagentry):
        return 0
    elif (name > tagentry):
        return 1
    else:
        return -1

def cmpArtworkByDate(artwork1,artwork2):
    
    """
    Si el primero es mayor, retorna True
    Si no, retorna False
    """

    date1 = artwork1['Date']
    date2 = artwork2['Date']
    if date1 == '':
        date1 =  0
    if date2 == '':
        date2 = 0
    if int(date1) < int(date2):
        return True
    else:
        return False

def sortDateAr(date1,date2):
    
    if date1['BeginDate'] < date2['BeginDate']:
        return True
    else:
        return False

def cmpArtworkByDateAdquired(artwork1,artwork2):
    # Compara el dia de adquisicion de una obra, devolviendo True si el primero es menor

    date1 = artwork1["DateAcquired"].split("-")
    date2 = artwork2["DateAcquired"].split("-")
    if len(date1)!= 3:
        return True
    if len(date2) != 3:
        return False

    if int(date1[0]) < int(date2[0]):
        return True
    elif int( date1[0]) == int(date2[0]):
        if date1[1] < date2[1]:
            return True
        elif int(date1[1]) == int(date2[1]):
            if int(date1[2]) < int(date2[2]):
                return True  
    else:
        return False

def sortCost(item1, item2):
    if item1['cost'] > item2['cost']:
        return True
    else:
        return False
def compareAlf(item1, item2):
    if item1[0] > item2[0]:
        return True
    else:
        return False

def compareCont(item1, item2):
    #Compara cual de los dos conteos es mayor (Se utiliza para ordenar las nacionalidades)
    if item1[1] > item2[1]:
        return True
    else:
        return False

def sortDate(item1,item2):
    if item1['Date'] < item2['Date']:
        return True
    else:
        return False

def cmpNationalitiesByArtworks(item1,item2):
    if int(item1["Numero"]) > int(item2["Numero"]):
        return True
    else:
        return False

# Funciones de ordenamiento

def sortArtworksByDate(lst, cmpfunction):
    """
    Ordena una lista, dada su cmpfuntion como str
    """
    if 'cmpArtworksByDate' == cmpfunction:
        ms.sort(lst, cmpArtworkByDate)

 