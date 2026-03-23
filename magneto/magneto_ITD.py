import re
import os
import sys
from jrodb import Api

"""
****************************************************************************************************************************************
Codigo para magnetometros LISN, IGP, MAGDAS, que reconoce: year,mes,estacion,tipo de dato
<script.py year_inferior year_superior mes_inferior mes_superior estacion datatype>
Sube a la web de LISN la data almacenada en el servidor: crea el dataset y sube los recursos especificados por el usuario (parametros)
17Febr2026-V1.0-ITD
Autor: Isaac Tupac
****************************************************************************************************************************************
"""
meses = {1: 'JANUARY',2: 'FEBRUARY',3: 'MARCH',4: 'APRIL',5: 'MAY',6: 'JUNE',7: 'JULY',8: 'AUGUST',9: 'SEPTEMBER',10: 'OCTOBER',11: 'NOVEMBER',12: 'DECEMBER'}
stations = ['huam','icam','ancm','tmam','piur','jica','huan','anco','areq','nazc','leon','cuib','puer','leti','saol','tara','tucu','alta']
data_types = ['minute','second','minutefigure']
fechas = []

if len(sys.argv)>1:
    nombre_script=sys.argv[0]
    print("Ejecutando el script",nombre_script,"\n")
    #print(len(sys.argv))

    year0 = sys.argv[1]
    if int(year0)<1991 or int(year0)>2027:
        print("Error en el año - elegir 2025, 2026 o 2027")
        sys.exit()

    year = sys.argv[2]
    if int(year)<1991 or int(year)>2027:
        print("Error en el año - elegir 2025, 2026 o 2027")
        sys.exit()

    mes0 = sys.argv[3]
    if int(mes0)<1 or int(mes0)>12:
        print("Error en el mes0 - elegir entre 1 y 12")
        sys.exit()

    mes = sys.argv[4]
    if int(mes)<1 or int(mes)>12:
        print("Error en el mes - elegir entre 1 y 12")
        sys.exit()

    station = sys.argv[5]
    c=0
    for i in stations:
        if i==station:
            c=c+1
    if c!=1:
        print("Error en la estacion - elegir 'huam','icam','ancm','tmam','piur','jica','huan','anco','areq','nazc','leon','cuib','puer','leti','saol','tara','tucu','alta'")
        sys.exit()

    if station == 'huam':
        name_station='HUANCAYO MAGDAS'
        voc_name='Huancayo Magdas'
        red='MAGDAS'
    if station == 'icam':
        name_station='ICA MAGDAS'
        voc_name='Ica Magdas'
        red='MAGDAS'
    if station == 'ancm':
        name_station='ANCON MAGDAS'
        voc_name='Ancon Magdas'
        red='MAGDAS'
    if station == 'tmam':
        name_station='TINGO MARIA MAGDAS'
        voc_name='TingoMaria Magdas'
        red='MAGDAS' 
    if station == 'piur':
        name_station='PIURA'
        voc_name='Piura'
        red='IGP' 
    if station == 'jica':
        name_station='JICAMARCA'
        voc_name='Jicamarca'
        red='IGP'
    if station == 'huan':
        name_station='HUANCAYO'
        voc_name='Huancayo'
        red='IGP'
    if station == 'anco':
        name_station='ANCON'
        voc_name='Ancon'
        red='IGP'
    if station == 'areq':
        name_station='AREQUIPA'
        voc_name='Arequipa'
        red='IGP'
    if station == 'nazc':
        name_station='NAZCA'
        voc_name='Nazca'
        red='IGP'
    if station == 'leon':
        name_station='CASLEO'
        voc_name='Casleo'
        red='LISN'
    if station == 'cuib':
        name_station='CUIABA'
        voc_name='Cuiaba'
        red='LISN'
    if station == 'puer':
        name_station='PUERTO MALDONADO'
        voc_name='Puerto Maldonado'
        red='LISN'
    if station == 'leti':
        name_station='LETICIA'
        voc_name='Leticia'
        red='LISN'
    if station == 'saol':
        name_station='SAO LUIZ'
        voc_name='Sao Luiz'
        red='LISN'
    if station == 'tara':
        name_station='TARAPOTO'
        voc_name='Tarapoto'
        red='IGP'
    if station == 'tucu':
        name_station='TUCUMAN'
        voc_name='Tucuman'
        red='LISN'
    if station == 'alta':
        name_station='ALTA FLORESTA'
        voc_name='Alta Floresta'
        red='LISN'

    data_type = sys.argv[6]
    d=0
    for j in data_types:
        if j==data_type:
            d=d+1
            if data_type == "minutefigure":
                data_type="minute_figure"
    if d!=1:
        print("Error en el tipo de dato - elegir 'minute','second','minutefigure'")
        sys.exit()

    print("El año inferior es:"+year0+", el año superior es:"+year+", el rango de meses:"+mes0+"-"+mes+", estacion:"+station+" "+", tipo de dato:"+data_type+" "+", voc_name:"+voc_name+" "+" y la red:"+red)
    print("")

    rangey0 = int(year0)
    rangey = int(year)+1
    range0 = int(mes0)
    rangef = int(mes)+1

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmb0ZhbDFfRVdlSWg0cmJwNTVnV1V0Y0JaMDlvQzgxTDEyX3B4Y21yd0dVaW9LNlpTVkpjNGt1N3hhVm1pdlNwdUpZM1B1QUYzOVZ5Z2p1MyIsImlhdCI6MTcxNzc5MjcyOX0.Q8hOUutNk6xeHS0J77FSMqpzv5DQUwzWFBln5Vo8YOA'

    for year in range (rangey0,rangey):
        for xmonth in range(range0,rangef):
            try:
                name_dataset = str(year)+'_'+meses[xmonth].lower()+'_'+data_type+'_'+station
                print("El dataset es:",name_dataset)
                
                if data_type == "minute_figure":
                    with Api('http://10.10.120.145:8091/database', Authorization=token) as access:
                        SKY = access.create(
                        type_option='dataset',
                        name=name_dataset,
                        owner_org='magnetometer',
                        voc_instrument_type='Magnetometer',
                        data_type=data_type+"s",
                        title=f'{year} {meses[xmonth]} {name_station} {(data_type[:6]+" "+data_type[7:]).upper()} {"REPORTED"}',  # Utiliza el nombre del mesueier¡
                        voc_station_name=voc_name,
                        notes='Magnetometer Data - Magnetogram',
                    )
                    print("El valor del mes es:\n",xmonth)
                    print("El valor creado para el data set es:\n",SKY)
                    #print(f'{year} {meses[xmonth]} {name_station} {(data_type[:6]+" "+data_type[7:]).upper()} {"REPORTED"}')

                    day_dir = f'/srv/app/src/data1/magnetometer/{red}/{station}/{year}/{xmonth:02d}/{data_type}s'
                    filenames = sorted(os.listdir(day_dir))
                    print("Los archivos alamacenados son: \n",filenames)

                    day_dir = day_dir.replace(f'/srv/app/src/data1', 'https://lisn.igp.gob.pe/database/base')
                    file_paths = [f'{day_dir}/{filename}' for filename in filenames]
                    #print("Las direcciones son:\n",file_paths)
                    print("Se crearon las direcciones de la data almacenada\n")

                    for nombre_de_datos in filenames:
                        #match = re.match(r"lpiu_(\d{2})(\d{2})(\d{2})\.nvd\.gz", nombre_de_datos)
                        match = re.match(rf"{station}_(\d{{2}})(\d{{2}})(\d{{2}})\.min\.png", nombre_de_datos)
                        if match:
                            if 90 < int(match.group(1)) < 100:
                                año = "19" + match.group(1)
                            else:    
                                año = "20" + match.group(1)
                            mes = match.group(2)
                            dia = match.group(3)
                            fecha = f"{año}-{mes}-{dia}"
                            fechas.append(fecha)
                        else:
                            print(f"El formato del nombre del archivo '{nombre_de_datos}' no es válido.")

                    print("Las fechas por almacenar son:\n",fechas)

                    with Api('http://10.10.120.145:8091/database', Authorization=token) as access:
                        create_resources = access.create(
                            type_option='resource',
                            url=file_paths,
                            ignore_repetition=True,
                            package_id = name_dataset,
                            name=filenames,
                            file_date=fechas,
                            file_type=data_type[0].upper()+data_type[1:]+'s',
                            format='png',
                            max_size=100,
                            max_count=100,
                        )
                    fechas = []
                    #print(data_type[0].upper()+data_type[1:]+'s')
                    print("El valor del recurso creado es:\n", create_resources)

                    with Api('http://10.10.120.145:8091/database', Authorization=token) as access:

                        metadata_dataset = access.show(type_option='dataset' , id = name_dataset)
                        k=access.create(type_option='views',select='dataset',package= metadata_dataset)
                        print(k)
              
                else:

                    with Api('http://10.10.120.145:8091/database', Authorization=token) as access:
                        SKY = access.create(
                        type_option='dataset',
                        name=name_dataset,
                        owner_org='magnetometer',
                        voc_instrument_type='Magnetometer',
                        data_type=data_type,
                        title=f'{year} {meses[xmonth]} {name_station} {data_type.upper()}',  # Utiliza el nombre del mesueier¡
                        voc_station_name=voc_name,
                        notes='Magnetometer Data - Magnetogram',
                    )
                    print("El valor del mes es:\n",xmonth)
                    print("El valor creado para el data set es:\n",SKY)

                    day_dir = f'/srv/app/src/data1/magnetometer/{red}/{station}/{year}/{xmonth:02d}/{data_type}'
                    filenames = sorted(os.listdir(day_dir))
                    print("Los archivos alamacenados son: \n",filenames)

                    day_dir = day_dir.replace(f'/srv/app/src/data1', 'https://lisn.igp.gob.pe/database/base')
                    file_paths = [f'{day_dir}/{filename}' for filename in filenames]
                    #print("Las direcciones son:\n",file_paths)
                    print("Se crearon las direcciones de la data almacenada\n")

                    if data_type == 'minute':
                        val='min'
                    if data_type == 'second':
                        val='sec'

                    for nombre_de_datos in filenames:
                        #match = re.match(r"lpiu_(\d{2})(\d{2})(\d{2})\.nvd\.gz", nombre_de_datos)
                        match = re.match(rf"{station}_(\d{{2}})(\d{{2}})(\d{{2}})\."+val+r"\.gz", nombre_de_datos)
                        if match:
                            if 90 < int(match.group(1)) < 100:
                                año = "19" + match.group(1)
                            else:    
                                año = "20" + match.group(1)
                            mes = match.group(2)
                            dia = match.group(3)
                            fecha = f"{año}-{mes}-{dia}"
                            fechas.append(fecha)
                        else:
                            print(f"El formato del nombre del archivo '{nombre_de_datos}' no es válido.")

                    print("Las fechas por almacenar son:\n",fechas)

                    with Api('http://10.10.120.145:8091/database', Authorization=token) as access:
                        create_resources = access.create(
                            type_option='resource',
                            url=file_paths,
                            ignore_repetition=True,
                            package_id=name_dataset,
                            name=filenames,
                            file_date=fechas,
                            file_type=data_type,
                            format='txt',
                            max_size=100,
                            max_count=100,
                        )
                    fechas = []

                    print("El valor del recurso creado es:\n", create_resources)                    

            except Exception as e:
                print("Estoy en exception\n")
                print(e)

else:
    print("Debe de agregar parametros al momento de correr el script - script.py year_inferior year_superior mes_inferior mes_superior estacion datatype")
