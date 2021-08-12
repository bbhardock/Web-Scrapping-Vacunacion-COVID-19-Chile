# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(executable_path=r'chromedriver.exe')

#Link al informe visual del MINSAL
#lo que me hace preguntar "where api"
driver.get('https://informesdeis.minsal.cl/SASVisualAnalytics/?reportUri=%2Freports%2Freports%2F9037e283-1278-422c-84c4-16e42a7026c8&sectionIndex=0&sso_guest=true&reportViewOnly=true&sas-welcome=false')

content = ""
#Un delay para esperar que la pagina cargue
delay = 10 #segundos
try:
    #Cuando la pagina está cargada, el titulo es el que está aca
    tituloEsperado = "VACUNACIÓN SARS-CoV-2 - SAS® Visual Analytics"
    #Digo que espere hasta que el titulo de la pagina sea el que esta arriba, expected condition se usa aca
    myElem = WebDriverWait(driver, delay).until(EC.title_is(tituloEsperado))
    #Que duerma un poco, tiene sueño
    #es para que los datos se carguen bien, sin esto a veces la ejecucion da errores de "sin datos"
    time.sleep(3)
    #Lo importante esta dentro de un iframe, asi que hay que buscar el iframe (solo uno para la pagina base)
    seq= driver.find_elements_by_tag_name('iframe')
    #hacerle el switch a ese iframe para que tome los datos importantes
    driver.switch_to.frame(seq[0])
    #se mueve hacia la posicion de la pestaña de vacunacion de menores y le hace click
    pestania = driver.find_element(By.ID, '__filter0-appSplitView-reportPanelView-0-sectionTabBar--header-7-text')
    webdriver.ActionChains(driver).move_to_element(pestania).click().perform()
    #espera 3 segundos para que cargue la segunda pagina
    time.sleep(3)
    #ahora con todo en el codigo de la pagina se guarda en una variable
    content= driver.page_source
    print("¡TREMENDO, SE CARGO LA PAGINA! AHORA VIENE LO BUENOOOOO")
except Exception as e:
    print("Para emocion, paso esto: ", e)

#cierra el navegadores
driver.quit()
#y hacemos el soup para navegar mas facilmente en los contenidos de la pagina
soup = BeautifulSoup(content,"lxml")



#como referencia, este titulo deberia ser diferente al tituloEsperado, porque el titulo de iframe es otro
#print(soup.title.string)

#DATO FREAK: los numeros importantes son de la clase sasdynamictext, asi que ese es el filtro LEL
datosBrutos = []
datosImportantes = soup.find_all('span','sasdynamictext')

for x in datosImportantes:
    #Si es string, pasalo a string, si no, dejalo asi nomas
    dato = x.string.replace('.','')
    try:
       datosBrutos.append(int(dato))
    #Un poco hack y a lo bruto pero funciona eh
    except Exception:
        datosBrutos.append(dato)


numeroDeVacunasAdministradas = datosBrutos[0]
personasPrimeraDosis = datosBrutos[1]
personasSegundaDosis = datosBrutos[2]
personasUnicaDosis = datosBrutos[3]
personasTerceraDosis = datosBrutos[4]
poblacionObj = datosBrutos[5]
actualizacionTabla = datosBrutos[-1] # siempre sera el ultimo, este dato esta al final de la pag
poblacionTotalChile = 19116209


dosisMenores = datosBrutos[14]
primeraDosisMenores = datosBrutos[15]
segundaDosisMenores = datosBrutos[16]
poblacionObjMenores = datosBrutos[17]


porcentajePrimera = ((personasPrimeraDosis+personasUnicaDosis)/poblacionObj)*100
porcentajeSegunda = ((personasSegundaDosis+personasUnicaDosis)/poblacionObj)*100
porcentajeObjetivoConTotal = poblacionObj/poblacionTotalChile


nombreArchivo = actualizacionTabla.replace(" ","_").replace(":","-")+".txt"
#ya empezamos a hacer el output
file = open(nombreArchivo,"w")
file.write('---VACUNACION MAYORES DE 18 AÑOS---')
file.close()

#y agregamos los datillos, haciendo los calculos a medida que los necesito
file = open(nombreArchivo,"a")

file.write("\nNumero de vacunas administradas: " + str(numeroDeVacunasAdministradas))
file.write("\nNumero de personas con primera dosis: "+str(personasPrimeraDosis))
file.write("\nNumero de personas con segunda dosis: "+str(personasSegundaDosis))
file.write("\nNumero de personas con unica dosis "+str( personasUnicaDosis))
file.write("\nPoblacion Objetivo: "+str(poblacionObj))

file.write("\nPersonas con primera y unica dosis: "+ str(round(porcentajePrimera,2))+"%"+";Con respecto al total de habitantes: "+ str(round(porcentajePrimera*porcentajeObjetivoConTotal,2))+"%")
file.write("\nPersonas con segunda y unica dosis: "+ str(round(porcentajeSegunda,2))+"%"+ ";Con respecto al total de habitantes: "+ str(round(porcentajeSegunda*porcentajeObjetivoConTotal,2))+"%")

file.write("\nDatos Actualizados al " + actualizacionTabla)


porcentajePrimeraMenores = primeraDosisMenores/poblacionObjMenores
porcentajeSegundaMenores = segundaDosisMenores/poblacionObjMenores


file.write("\n---VACUNACION 12 A 17 AÑOS---")
file.write("\nNumero de vacunas administradas: " + str(dosisMenores))
file.write("\nNumero de personas con primera dosis: "+str(primeraDosisMenores))
file.write("\nNumero de personas con segunda dosis: "+str(segundaDosisMenores))
file.write("\nPoblacion Objetivo: "+str(poblacionObjMenores))

file.write("\nPersonas con primera dosis: "+str(round(porcentajePrimeraMenores*100,2))+"%")
file.write("\nPersonas con segunda dosis: "+str(round(porcentajeSegundaMenores*100,2))+"%")

totalPrimeraDosis = personasPrimeraDosis + personasUnicaDosis + primeraDosisMenores
totalSegundaDosis = personasSegundaDosis + personasUnicaDosis + segundaDosisMenores
porcentajeTotalPrimeraDosis = totalPrimeraDosis/poblacionTotalChile
porcentajeTotalSegundaDosis = totalSegundaDosis/poblacionTotalChile
maximoPosiblePorcentaje = (poblacionObj+poblacionObjMenores)/poblacionTotalChile

file.write("\n---TOTAL NACIONAL---")
file.write("\n Datos con respecto a la poblacion total en Chile segun el Banco Mundial")
file.write("\nPrimera y unica dosis: "+str(totalPrimeraDosis)+"; "+str(round(porcentajeTotalPrimeraDosis*100,2))+"%")
file.write("\nSegunda y unica dosis: "+str(totalSegundaDosis)+"; "+str(round(porcentajeTotalSegundaDosis*100,2))+"%")
file.write("\nMaximo posible porcentaje de vacunacion (considerando 100% de las poblacion objetivo): "+str(round(maximoPosiblePorcentaje*100,2))+"%")

file.close()