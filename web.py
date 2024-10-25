from flask import Flask, render_template, request
from main import filtrar_ventas
app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        # formulario = {
        #     'start_date': request.form.get('start_date'),
        #     'end_date': request.form.get('end_date'),
        #     'vendedora': request.form.get('vendedora'),
        #     'categoria': request.form.get('categoria')
        # }
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        vendedora = request.form.get('vendedora')
        categoria = request.form.get('categoria')
        
        # total_ventas = filtrar_ventas(**formulario)
        total_ventas = filtrar_ventas(start_date, end_date, vendedora, categoria)
        
        return render_template(template_name_or_list='index.html',  context=total_ventas)
    return render_template(template_name_or_list='index.html')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)

