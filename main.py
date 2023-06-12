from flask import Flask, request, render_template, jsonify

app = Flask(__name__)
historial = []
contador = 0
rp1_data = []
rp2_data = []
rp3_data = []

@app.route('/')
def index():
    return render_template('index.html', historial=historial)

@app.route('/historial_ajax')
def mostrar_historial_ajax():
    return jsonify({
        'historial': historial,
        'rp1_data': rp1_data,
        'rp2_data': rp2_data,
        'rp3_data': rp3_data,
        'promedios': calcular_promedios()  # Agregar los promedios al JSON de respuesta
    })

@app.route('/historial', methods=['GET', 'POST'])
def mostrar_historial():
    global contador

    if request.method == 'GET':
        valor = float(request.args.get('valor'))
        contador += 1

        if contador > 15:
            historial.clear()
            rp1_data.clear()
            rp2_data.clear()
            rp3_data.clear()
            contador = 1

        historial.append((contador, valor))
        
        # Obtener el identificador de la Raspberry Pi Pico
        identificador = request.args.get('id')
        
        # Almacenar los datos en el historial correspondiente
        if identificador == 'rp1':
            rp1_data.append((contador, valor))
        elif identificador == 'rp2':
            rp2_data.append((contador, valor))
        elif identificador == 'rp3':
            rp3_data.append((contador, valor))

        # Devolver una respuesta en formato JSON con el historial actualizado y los promedios
        return jsonify({
            'historial': historial,
            'rp1_data': rp1_data,
            'rp2_data': rp2_data,
            'rp3_data': rp3_data,
            'promedios': calcular_promedios()
        })

def calcular_promedios():
    promedios = {}
    if rp1_data:
        rp1_promedio = sum([valor for _, valor in rp1_data]) / len(rp1_data)
        promedios['rp1'] = rp1_promedio
    if rp2_data:
        rp2_promedio = sum([valor for _, valor in rp2_data]) / len(rp2_data)
        promedios['rp2'] = rp2_promedio
    if rp3_data:
        rp3_promedio = sum([valor for _, valor in rp3_data]) / len(rp3_data)
        promedios['rp3'] = rp3_promedio
    return promedios

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
