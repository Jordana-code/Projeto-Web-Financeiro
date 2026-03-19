from flask import Flask, request, render_template, jsonify
import matplotlib.pyplot as plt
import sqlite3

app = Flask(__name__)

def grafico(renda, gastos, investimento, lazer, dividas, sobra):
    
    labels = ['Gastos', 'Investimento', 'Lazer', 'Divídas', 'Sobras']
    valores = [gastos, investimento, lazer, dividas, sobra]

    plt.figure(figsize=(10,10), facecolor='#0f172a')
    plt.pie(valores, labels=labels, autopct='%1.1f%%', textprops={'color': 'white'})

    plt.title("Organização Financeira atual:", color="white")

    plt.savefig("static/grafico.png", facecolor='#0f172a', bbox_inches='tight')
    plt.close()

def grafico2(gastos, investimento, lazer, dividas, sobra):
    gastos2 = gastos + dividas
    investimento2 = investimento + sobra/2
    lazer2 = lazer + sobra/2

    labels = ['Gastos + Divídas', 'Investimento', 'Lazer']
    valores = [gastos2, investimento2, lazer2]

    plt.figure(figsize=(10,10), facecolor='#0f172a')
    plt.pie(valores, labels=labels, autopct='%1.1f%%', textprops={'color': 'white'})

    plt.title("Organização Financeira recomendada:", color="white")

    plt.savefig("static/grafico2.png", facecolor='#0f172a', bbox_inches='tight')
    plt.close()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/resultado', methods=['POST'])
def resultado():
 
    try:
        renda = float(request.form['renda'])
        gastos = float(request.form['gastos'])
        investimento = float(request.form['investimento'])
        lazer = float(request.form['lazer'])
        dividas = float(request.form['dividas'])

        sobra_calculada = renda - (gastos + investimento + lazer + dividas)
        
        grafico(renda, gastos, investimento, lazer, dividas, sobra_calculada)
        grafico2(gastos, investimento, lazer, dividas, sobra_calculada)

        if sobra_calculada < 0:
            return render_template("index.html", erro="Seus gastos ultrapassam sua renda")
        try:
            conn = sqlite3.connect('financas.db')
            cursor = conn.cursor()

            id_user = 1  # depois a gente melhora isso

            cursor.execute(
                "INSERT INTO info_financeira (id_usuario, salario) VALUES (?, ?)",
                (id_user, renda)
            )

            dados_para_salvar = [
                (id_user, 'Essencial', gastos),
                (id_user, 'Investimento', investimento),
                (id_user, 'Lazer', lazer),
                (id_user, 'Dividas', dividas)
            ]

            cursor.executemany("""
                INSERT INTO gastos (id_usuario, tipo, valor, data)
                VALUES (?, ?, ?, date('now'))
            """, dados_para_salvar)

            conn.commit()
            conn.close()

        except Exception as e:
            print("Erro no banco:", e)
        return jsonify({
            "grafico" : "grafico.png",
            "grafico2" : "grafico2.png"
        })
        
    except Exception as e:
        print(f"Erro no console: {e}") 
        return render_template("index.html", grafico=False, grafico2=False, erro="Rapaz... Como que você ta gastando mais do que você ganha?")

if __name__ == "__main__":
    app.run(debug=True)