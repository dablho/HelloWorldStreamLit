import streamlit as st
import pandas as pd
import pdfplumber as pp
from collections import Counter
import re
import nltk
import matplotlib.pyplot as plt
import wordcloud as wd
import requests

st.markdown('''
  # *Olá, seja bem-vindo à Análise Estatística de um texto*.
  
  ### Importe um arquivo de texto:
  '''
)

arquivo = st.file_uploader(
  'Importar arquivo PDF',
  type=['pdf']
)

num_palavras = st.sidebar.selectbox(
  'Selecione a quantia de palavras mais frequentes:',
  [10, 20, 30]
)

if arquivo:
  pdf = pp.open(arquivo)
  st.write(f'O arquivo tem {len(pdf.pages)} páginas.')

  texto = ''
  for pagina in pdf.pages:
    texto += pagina.extract_text()

  expander = st.expander('Palavras do PDF:')
  expander.write(texto)

  nltk.download('stopwords')
  stopwords = nltk.corpus.stopwords.words('portuguese')

  texto_limpo = re.sub(r'\W+', ' ', texto.lower())
  palavras = texto_limpo.split()

  palavra_sem_stopword = [palavra for palavra in palavras if palavra not in stopwords and len(palavra) > 2]

  frequencia = Counter(palavra_sem_stopword)

  mais_comuns = frequencia.most_common(num_palavras)
  st.write(f'As {num_palavras} palavras mais frequentes no texto pdf são:')
  col1, col2 = st.columns(2)

  for i, (palavra, contagem) in enumerate(mais_comuns):
    if i < num_palavras // 2:
        col1.write(f"{i+1}: {palavra} - {contagem}")
    else:
        col2.write(f"{i+1}: {palavra} - {contagem}")

  plt.figure(figsize=(15, 5))
  palavras, contagens = zip(*mais_comuns)
  plt.bar(palavras, contagens)
  plt.xlabel('Palavras')
  plt.ylabel('Frequência')
  plt.title('Palavras mais frequentes no texto inserido')
  plt.xticks(rotation=45)
  st.pyplot(plt.gcf())

  wordcloud = wd.WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies=frequencia)

  st.image(wordcloud.to_array(), caption='Nuvem de Palavras', use_column_width=True)


st.markdown('''
  ### Escreva um texto:
  '''
)

text = st.text_area('Escreva um texto:', max_chars=7000)

if text:
  text_limpo = re.sub(r'\W+', ' ', text.lower())
  palavras_text = text_limpo.split()

  nltk.download('stopwords')
  stopwords = nltk.corpus.stopwords.words('portuguese')

  palavras_text_sem_stopwords = [palavra for palavra in palavras_text if palavra not in stopwords and len(palavra) > 2]

  frequencia = Counter(palavras_text_sem_stopwords)

  total_palavras_text = len(palavras_text)

  if total_palavras_text == 1:
    st.write(f'{total_palavras_text} palavra')
  elif total_palavras_text > 1:
    st.write(f'{total_palavras_text} palavras')

  mais_comuns = frequencia.most_common(num_palavras)
  st.write(f'As {num_palavras} palavras mais frequentes no texto inserido são:')
  col1, col2 = st.columns(2)

  for i, (palavra, contagem) in enumerate(mais_comuns):
    if i < num_palavras // 2:
        col1.write(f"{i+1}: {palavra} - {contagem}")
    else:
        col2.write(f"{i+1}: {palavra} - {contagem}")




  if mais_comuns:
    palavras, contagens = zip(*mais_comuns)
    plt.figure(figsize=(15, 5))
    plt.bar(palavras, contagens)
    plt.xlabel('Palavras')
    plt.ylabel('Frequência')
    plt.title('Palavras mais frequentes no texto inserido')
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
  else:
    st.warning('Esta palavra é uma stopword.')

  if frequencia:
    wordcloud = wd.WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies=frequencia)
    st.image(wordcloud.to_array(), caption='Nuvem de Palavras', use_column_width=True)
  else:
    pass

st.markdown('''
  ### Link de uma página:
  '''
)

link_pagina = st.text_input('Insira o link da página:', '')

def baixar_conteudo_pagina(link):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            return response.text
        else:
            st.error(f"Não foi possível baixar o conteúdo da página. Código de status: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao tentar baixar o conteúdo da página: {e}")
        return None
    
if link_pagina:
    texto_pagina = baixar_conteudo_pagina(link_pagina)
    
    if texto_pagina:
        texto_limpo_pagina = re.sub(r'\W+', ' ', texto_pagina.lower())
        palavras_pagina = texto_limpo_pagina.split()

        nltk.download('stopwords')
        stopwords = nltk.corpus.stopwords.words('portuguese')

        palavras_pagina_sem_stopwords = [palavra for palavra in palavras_pagina if palavra not in stopwords and len(palavra) > 2]

        frequencia_pagina = Counter(palavras_pagina_sem_stopwords)

        total_palavras_pagina = len(palavras_pagina_sem_stopwords)

        if total_palavras_pagina == 1:
            st.write(f'{total_palavras_pagina} palavra encontrada na página')
        elif total_palavras_pagina > 1:
            st.write(f'{total_palavras_pagina} palavras encontradas na página')

        mais_comuns_pagina = frequencia_pagina.most_common(num_palavras)
        st.write(f'As {num_palavras} palavras mais frequentes no texto inserido são:')
        col1, col2 = st.columns(2)

        for i, (palavra, contagem) in enumerate(mais_comuns_pagina):
          if i < num_palavras // 2:
            col1.write(f"{i+1}: {palavra} - {contagem}")
          else:
            col2.write(f"{i+1}: {palavra} - {contagem}")

        plt.figure(figsize=(15, 5))
        palavras_pagina, contagens_pagina = zip(*mais_comuns_pagina)
        plt.bar(palavras_pagina, contagens_pagina)
        plt.xlabel('Palavras')
        plt.ylabel('Frequência')
        plt.title('Palavras mais frequentes na página')
        plt.xticks(rotation=45)
        st.pyplot(plt.gcf())

        wordcloud_pagina = wd.WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies=frequencia_pagina)

        st.image(wordcloud_pagina.to_array(), caption='Nuvem de Palavras na Página', use_column_width=True)

st.markdown('''
  ###
  ###### Projeto feito por William Mattede
  '''
)
