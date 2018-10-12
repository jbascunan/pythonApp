from flask import Flask, render_template, request
import json, urllib.request, sys, datetime


app = Flask(__name__)

@app.route('/datos', methods=["GET","POST"])

def obtenerUF():
    fechaInicio = request.form.get("fechaInicio")
    fechaFin = request.form.get("fechaFin")

    strError=''
    if fechaInicio is None or fechaFin is None:
        return render_template("datos.html", datos='', strError='Debe ingresar fechas')
    elif datetime.datetime.strptime(str(fechaInicio), '%Y-%m-%d') > datetime.datetime.strptime(str(fechaFin), '%Y-%m-%d'):
        return render_template("datos.html", datos='', strError='Fecha Fin no puede ser menor a la fecha de inicio')


    # ***** OBTENER UF ******
    try:
        output_uf = getDatosApi(fechaInicio, fechaFin, 'uf')

        arrayValorUf = []
        arrayFechaUf = []

        for page_entry in output_uf:
            arrayValorUf.append(float(page_entry['Valor'].replace('.', '').replace(',', '.')))
            arrayFechaUf.append(page_entry['Fecha'])

        legendUf = 'Valor UF'
        labelsUf = arrayFechaUf
        valuesUf = arrayValorUf


    except:
        strError = "Se ha producido error al obtener valores de uf"

    #****DOLAR ****
    try:
        output_dolar = getDatosApi(fechaInicio, fechaFin, 'dolar')

        arrayValorDolar = []
        arrayFechaDolar = []

        for page_entry in output_dolar:
            arrayValorDolar.append(float(page_entry['Valor'].replace('.', '').replace(',', '.')))
            arrayFechaDolar.append(page_entry['Fecha'])

        legendDolar = 'Valor Dolar'
        labelsDolar = arrayFechaDolar
        valuesDolar = arrayValorDolar

    except:
        strError = "Se ha producido error al obtener valores de DOLAR"


    return render_template("datos.html", datosUf=output_uf, valuesUf=valuesUf, labelsUf=labelsUf, legendUf=legendUf,promedioUf=promedio(arrayValorUf),promedioDolar=promedio(arrayValorDolar),maxUf=max(arrayValorUf),minUf=min(arrayValorUf), maxDolar=max(arrayValorDolar),minDolar=min(arrayValorDolar), datosDolar=output_dolar, valuesDolar=valuesDolar, labelsDolar=labelsDolar, legendDolar=legendDolar, fechaIni=fechaInicio, fechaFin=fechaFin, strError=strError)

def getDatosApi(fechaInicio, fechaFin, operacion):
    fechaIniRango = datetime.datetime.strptime(str(fechaInicio), '%Y-%m-%d')
    fechaFinRango = datetime.datetime.strptime(str(fechaFin), '%Y-%m-%d')

    rangoFecha = str(fechaIniRango.year) + "/" + str(fechaIniRango.month) + "/" + str(fechaFinRango.year) + "/" + str(
        fechaFinRango.month)

    url = ''
    root_json = ''

    if operacion == 'uf':
        url = "https://api.sbif.cl/api-sbifv3/recursos_api/uf/periodo/"
        root_json = 'UFs'
    else:
        url = "https://api.sbif.cl/api-sbifv3/recursos_api/dolar/periodo/"
        root_json = 'Dolares'

    url = url + rangoFecha + "?apikey=d0f45d4e841570f973493048c91ff888ff478482&formato=json"

    url_req = urllib.request.urlopen(url)
    json_obj = json.load(url_req)

    # Filtramos fechas
    output = [x for x in json_obj[root_json] if
                    (datetime.datetime.strptime(x['Fecha'], '%Y-%m-%d') >= fechaIniRango) and (
                            datetime.datetime.strptime(x['Fecha'], '%Y-%m-%d') <= fechaFinRango)]

    return output

def promedio(valores):
	sumaParcial=0
	for valor in valores:
		sumaParcial+=valor

	cantidadValores = len(valores)
	return sumaParcial/float(cantidadValores)

@app.route('/')
def index():
    return render_template("datos.html")

if __name__ == '__main__':
    app.run(debug=True)