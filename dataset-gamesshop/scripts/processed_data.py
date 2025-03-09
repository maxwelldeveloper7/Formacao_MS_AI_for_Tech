import os
import pandas as pd

def format_date_columns(df):
    for col in df.columns:
        if df[col].dtype == 'object':
            temp_series = pd.to_datetime(df[col], format='%Y-%m-%d', errors='coerce')
            if temp_series.notna().any():
                df[col] = temp_series.dt.strftime('%d/%m/%Y')
    return df

def merge_csv_files_to_excel(folder_path, output_file):
    all_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    combined_data = []
    
    for file in all_files:
        file_path = os.path.join(folder_path, file)
        df = pd.read_csv(file_path)
        df = format_date_columns(df)
        combined_data.append(df)
    
    if combined_data:
        final_df = pd.concat(combined_data, ignore_index=True)
        
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            final_df.to_excel(writer, index=False, sheet_name='consolidate')
            
            workbook = writer.book
            worksheet = writer.sheets['consolidate']
            
            # Formato personalizado para FORÇAR o ponto como separador decimal
            # [$-409] = Código de localidade para inglês (Estados Unidos)
            number_format = workbook.add_format({'num_format': '[$-409]#,##0.00'})
            
            # Identificar colunas numéricas
            numeric_cols = final_df.select_dtypes(include=['float64', 'int64']).columns
            
            # Aplicar o formato às colunas
            for col_idx, col_name in enumerate(final_df.columns):
                if col_name in numeric_cols:
                    worksheet.set_column(col_idx, col_idx, 15, number_format)  # 15 = largura da coluna
        
        print(f'Arquivo Excel gerado: {output_file}')
    else:
        print('Nenhum arquivo CSV encontrado.')

# Exemplo de uso
folder_path = '../data/raw_data'
output_file = '../data/processed_data/Meganium_sales_data.xlsx'

merge_csv_files_to_excel(folder_path, output_file)
