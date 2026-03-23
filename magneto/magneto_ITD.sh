#************************************************************************************************************************
#Bash que ejecuta el script magneto_ITD.py tomando en consideracion el año, mes, nombre de la estacion y el tipo de dato
#Autor: Isaac Tupac
#************************************************************************************************************************

#!/bin/bash

# 1. Definir los arreglos de valores
TIPOS=("huam" "icam" "ancm" "jica" "piur" "huan" "areq" "leon" "saol" "tara") # Agrega aquí todos los que necesites
#TIPOS=("jica")
FRECUENCIAS=("minute" "second" "minutefigure")

# 2. Capturar fecha actual
YEAR=$(date +%Y)
MES=$(date +%m)

# 3. Bucle anidado para recorrer todas las combinaciones
for TIPO in "${TIPOS[@]}"; do
    for FREC in "${FRECUENCIAS[@]}"; do
        
        # EXCEPCIÓN: Si la ciudad es 'saol' y la frecuencia es 'day' (o el parámetro que quieras omitir), saltar.
        if [[ "$TIPO" == "saol" && "$FREC" == "second" ]]; then
            echo "Saltando $TIPO para la frecuencia $FREC..."
            continue
        fi
        
        LOG_FILE="/var/log/magneto_${TIPO}_${FREC}.log"
        
        echo "Ejecutando para TIPO: $TIPO y FRECUENCIA: $FREC...($(date))"
        
        # Ejecución del comando de Docker
        docker exec ckan-python-cielo python3 magneto_ITD.py \
            $YEAR $YEAR $MES $MES $TIPO $FREC > "$LOG_FILE" 2>&1
            
    done
done
