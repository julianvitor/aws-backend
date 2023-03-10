# -*- coding: utf-8 -*-
from flask import Flask, request
import boto3 #biblioteca AWS S3 
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do S3
s3 = boto3.client('s3')
bucket_name = '<NOME_DO_BUCKET>'
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(bucket_name)

# Configuração do banco de dados (ORM)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<USUARIO_DO_BANCO>:<SENHA_DO_BANCO>@<HOST_DO_BANCO>:<PORTA_DO_BANCO>/<NOME_DO_BANCO>'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo da tabela do banco de dados
class Tabela(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), nullable=False)
    cnpj = db.Column(db.String(14), nullable=False)
    data = db.Column(db.Date, nullable=False)


# Função para tratar as informações do arquivo CSV
def trata_csv(df):
    df['cpf'] = df['cpf'].str.replace('[^0-9]', '')  # remove caracteres não numéricos
    df['cnpj'] = df['cnpj'].str.replace('[^0-9]', '')
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y').dt.date  # converte a coluna para o formato yyyy-MM-dd
    return df

# Rota para receber os parâmetros e processar o CSV
@app.route('/processar-csv', methods=['POST'])
def processar_csv():
    object_key = request.form['object_key']  # obtém o nome do arquivo no S3
    obj = s3.get_object(Bucket=bucket_name, Key=object_key)  # obtém o objeto do S3
    df = pd.read_csv(obj['Body'])  # CSV para dataframe
    df = trata_csv(df)  # trata as informações do dataframe
    
    # Insere as informações no banco de dados
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO tabela (cpf, cnpj, data) VALUES (%s, %s, %s)", (row['cpf'], row['cnpj'], row['data']))
    conn.commit()
    cursor.close()
    conn.close()
    return 'Arquivo CSV processado!'

if __name__ == '__main__':
    app.run(debug=True)