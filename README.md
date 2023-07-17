## 📝 Email Extractor App em Python 📧

Este é um aplicativo Python que utiliza o Streamlit para extrair emails válidos e únicos a partir dos resultados de busca do Google. O aplicativo oferece a possibilidade de escolher o tipo de mídia social (Facebook, Instagram, Telegram, Twitter, LinkedIn) a ser pesquisada, inserir uma palavra-chave após "CODIGO:" e selecionar a quantidade de páginas a serem pesquisadas.

## 🚀 Como Executar o Aplicativo

Para executar o aplicativo, você pode seguir os seguintes passos:

1. Certifique-se de ter o Python instalado em seu computador.

2. Instale as bibliotecas necessárias executando o seguinte comando no terminal ou prompt de comando:

```
pip install streamlit requests pandas
```

3. Salve o código do aplicativo em um arquivo Python (por exemplo, `app.py`).

4. Execute o aplicativo com o Streamlit usando o seguinte comando:

```
streamlit run app.py
```

5. O aplicativo será executado localmente e abrirá automaticamente no navegador padrão.

## 📝 Instruções de Uso

1. Ao acessar o aplicativo, você verá um seletor para escolher a mídia social desejada.

2. Digite a palavra-chave após "CODIGO:" no campo de texto.

3. Selecione a quantidade de páginas que deseja pesquisar.

4. Clique no botão "Buscar Emails" para iniciar a extração dos emails.

5. Os resultados serão exibidos na tela, mostrando a quantidade de páginas pesquisadas e o número total de emails únicos encontrados.

6. Para baixar os emails encontrados em um arquivo CSV, clique no botão "Baixar CSV".

## 📁 Estrutura do Projeto

```
/
├── app.py        # Código-fonte do aplicativo Streamlit
├── valid_emails.csv  # Arquivo CSV com os emails extraídos (será gerado após a execução)
└── requirements.txt  # Lista de bibliotecas necessárias para o projeto
```

## 📝 Notas Adicionais

- O aplicativo utiliza a biblioteca `requests` para fazer a busca no Google.
- Os emails são extraídos usando expressões regulares para encontrar padrões de emails válidos.
- É importante lembrar que a extração de informações de sites pode estar sujeita a restrições impostas pelo Google ou pelas mídias sociais escolhidas.

🚀 Divirta-se usando o aplicativo para extrair emails válidos a partir das suas pesquisas em mídias sociais! 😊📧
