### Entrada
```Markdown
crie um app python que leia todos os arquivos csv de uma pasta, formate as colunas de datas que estiverem no formato yyyy/mm/dd para dd/mm/yyyy e salve todos os dados em um arquivo Meganium_sales_data.xlsx
- se houver mais de um arquivo na pasta a primeira linha dos próximos arquivos deve ser descartada, pois se trata de cabeçários das colunas
```
### Saída
```Python
import os
import pandas as pd
from datetime import datetime

def format_date_columns(df):
    for col in df.columns:
        if df[col].dtype == 'object':  # Verifica se a coluna é de texto
            try:
                df[col] = pd.to_datetime(df[col], format='%Y/%m/%d', errors='coerce').dt.strftime('%d/%m/%Y')
            except Exception:
                continue  # Se não for uma coluna de data, ignora
    return df

def merge_csv_files_to_excel(folder_path, output_file):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    combined_data = []
    
    for index, file in enumerate(all_files):
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
                
        df = format_date_columns(df)  # Formata as colunas de data
        combined_data.append(df)
    
    if combined_data:
        final_df = pd.concat(combined_data, ignore_index=True)
        final_df.to_excel(output_file, index=False)
        print(f'Dados combinados e salvos em {output_file}')
    else:
        print('Nenhum arquivo CSV encontrado.')

# Caminho da pasta com os arquivos CSV e nome do arquivo de saída
folder_path = 'caminho/para/a/pasta'
output_file = 'Meganium_sales_data.xlsx'

merge_csv_files_to_excel(folder_path, output_file)

```