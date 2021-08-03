# Web Scrapping Vacunacion COVID-19 Chile
 Web Scrap de los datos del reporte visual del DEIS para la vacunación del COVID-19 en chile.
 
 Por alguna razon el MINSAL no se molesta en tener unos datos lo suficientemente actualizados **EXCEPTO** por un reporte visual en el sitio del DEIS https://deis.minsal.cl/ y además, la página del resumen comenzó a redondear los datos para celebrar antes de tiempo ciertos milestones de la campaña de vacunación. Todo esto me motivó a hacer este programa.
 
 El programa necesita Chrome (pero puede cambiarse el código para utilizar otros navegadores compatibles con Selenium https://www.selenium.dev/documentation/en/webdriver/driver_requirements/) y un chromedriver compatible con el navegador que se encuentra en https://chromedriver.chromium.org/.
 
 El output es un archivo de texto, que contiene el resumen del día en un formato legible.

# Ejemplo de Output
---VACUNACION MAYORES DE 18 AÑOS---

Numero de vacunas administradas: 24823976  
Numero de personas con primera dosis: 12656353  
Numero de personas con segunda dosis: 11660882  
Numero de personas con unica dosis 506741  
Poblacion Objetivo: 15200840  
Personas con primera y unica dosis: 86.59%;Con respecto al total de habitantes: 68.86%  
Personas con segunda y unica dosis: 80.05%;Con respecto al total de habitantes: 63.65%  
Datos Actualizados al martes, 3 de agosto de 2021 13:31:48  
---VACUNACION 12 A 17 AÑOS---  
Numero de vacunas administradas: 864857  
Numero de personas con primera dosis: 694831  
Numero de personas con segunda dosis: 170026  
Poblacion Objetivo: 1495162  
Personas con primera dosis: 46.47%  
Personas con primera dosis: 11.37%  
---TOTAL NACIONAL---  
 Datos con respecto a la poblacion total en Chile segun el Banco Mundial  
Primera y unica dosis: 13857925; 72.49%  
Segunda y unica dosis: 12337649; 64.54%  
Maximo posible porcentaje de vacunacion (considerando 100% de las poblacion objetivo): 87.34%  
