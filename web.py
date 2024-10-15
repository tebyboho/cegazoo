from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        vendedora = request.form.get('vendedora')
        categoria = request.form.get('categoria')
    print(vendedora)
    print(start_date)
    return render_template(template_name_or_list="index.html")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)

