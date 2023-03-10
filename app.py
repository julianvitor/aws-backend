from flask import Flask, request
import boto3
import pandas as pd
import psycopg2

app = Flask(__name__)

# Configuração do S3
s3 = boto3.client('s3')
bucket_name = '<NOME_DO_BUCKET>'
s3_resource = boto3.resource('s3')
bucket = s3_resource.Bucket(bucket_name)

# Configuração do banco de dados
db_host = '<ENDEREÇO>'
db_port = '<PORTA DO BANCO DE DADOS>'
db_name = '<NOME>'
db_user = '<USUARIO>'
db_pass = '<SENHA DO BANCO DE DADOS>'

# Função para tratar as informações do arquivo CSV
def trata_csv(df):
    df['cpf'] = df['cpf'].str.replace('[^0-9]', '')  # remove caracteres não numéricos
    df['cnpj'] = df['cnpj'].str.replace('[^0-9]', '')
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')  # converte a coluna data para o formato yyyy-MM-dd
    return df

# Rota para receber os parâmetros e processar o arquivo CSV
@app.route('/processar-csv', methods=['POST'])
def processar_csv():
    object_key = request.form['object_key']  # obtém o nome do arquivo no S3
    obj = s3.get_object(Bucket=bucket_name, Key=object_key)  # obtém o objeto do S3
    df = pd.read_csv(obj['Body'])  # CSV para dataframe
    df = trata_csv(df)  # trata as informações do dataframe
    
    # Conexão com o banco de dados
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_pass)
    cursor = conn.cursor()
    
    # Insere as informações no banco de dados
    for index, row in df.iterrows():
        cursor.execute("INSERT INTO tabela (cpf, cnpj, data) VALUES (%s, %s, %s)", (row['cpf'], row['cnpj'], row['data']))
    conn.commit()
    cursor.close()
    conn.close()
    return 'Arquivo CSV processado!'

if __name__ == '__main__':
    app.run(debug=True)