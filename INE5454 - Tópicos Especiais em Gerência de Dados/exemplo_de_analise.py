import matplotlib.pyplot as plt
import pandas as pd

# Carregar os dados do arquivo JSON
file_path = 'INE5454 - Tópicos Especiais em Gerência de Dados/metacritic_data.json'
df = pd.read_json(file_path)

# Imprimir as primeiras linhas do DataFrame para verificação
print(df.head())

# Verificar se a coluna 'SCORE' está presente e não está vazia
if 'SCORE' in df.columns:
    # Remover a string '/100' e converter 'SCORE' para numérico, ignorando erros
    df['SCORE'] = df['SCORE'].str.replace('/100', '').astype(float)
    
    # Verificar se há dados válidos na coluna 'SCORE'
    if df['SCORE'].isnull().all():
        print("Nenhum dado válido no campo 'SCORE'")
    else:
        # Plotando o histograma das pontuações dos filmes
        plt.figure(figsize=(10, 6))
        df['SCORE'].plot(kind='hist', bins=20, edgecolor='black')
        plt.title('Distribuição das Pontuações dos Filmes')
        plt.xlabel('Pontuação')
        plt.ylabel('Número de Filmes')
        plt.show()
else:
    print("Coluna 'SCORE' não encontrada no DataFrame")
