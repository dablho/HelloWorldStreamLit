import streamlit as st
import pandas as pd
import pdfplumber as pp
from collections import Counter
import re
import nltk
import matplotlib.pyplot as plt
import wordcloud as wd

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
  st.write(f'As {num_palavras} palavras mais frequentes no PDF são:')
  st.write(mais_comuns)

  plt.figure(figsize=(15, 5))
  palavras, contagens = zip(*mais_comuns)
  plt.bar(palavras, contagens)
  plt.xlabel('Palavras')
  plt.ylabel('Frequência')
  plt.title('Palavras mais frequentes no texto inserido')
  plt.xticks(rotation=45)
  st.pyplot(plt.gcf())

  wordcloud = wd.WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies=frequencia)

# Exiba a nuvem de palavras na interface do Streamlit
  st.image(wordcloud.to_array(), caption='Nuvem de Palavras', use_column_width=True)


st.markdown('''
  ### Escreva um texto:
  '''
)

text = st.text_area('Escreva um texto:', max_chars=3200)

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
  st.write(mais_comuns)

  plt.figure(figsize=(15, 5))
  palavras, contagens = zip(*mais_comuns)
  plt.bar(palavras, contagens)
  plt.xlabel('Palavras')
  plt.ylabel('Frequência')
  plt.title('Palavras mais frequentes no texto inserido')
  plt.xticks(rotation=2)
  st.pyplot(plt.gcf())

  wordcloud = wd.WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(frequencies=frequencia)

  st.image(wordcloud.to_array(), caption='Nuvem de Palavras', use_column_width=True)

st.markdown('''
  ### Link de uma página:
  '''
)

