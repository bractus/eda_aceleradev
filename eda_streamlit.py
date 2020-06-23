import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno 


def main():
    st.title('Análise Exploratória dos Dados')
    st.subheader('Por: Cairo Rocha (https://github.com/bractus)')

    separator = st.radio("Separador: ", (',', ';'))
    file_ = st.file_uploader('Selecione seu arquivo CSV', type='csv')

    if file_:

        df = pd.read_csv(file_, sep=separator)
        df_copy = df.copy()

        option = st.sidebar.selectbox(
            "Qual informação deseja ver?",
            ("Básicas", "Descrição (Describe)", "Valores faltantes", "Correlação", "Gráficos de distribuição", 
            "Valores atípicos (Outliers)")
        )

        if st.sidebar.button('Resetar alterações'):
            df = df_copy.copy()

        if option == 'Básicas':
            st.write("Linhas", df.shape[0], "Colunas", df.shape[1])
        
            slider_st = st.slider('Quantidade de linhas', 0, df.shape[0], 5)
            st.dataframe(df.head(slider_st))

            st.subheader('Tipos de variável: ')
            st.write(df.dtypes.value_counts())
        
        elif option == 'Descrição (Describe)':

            st.subheader('Describe: ')
            st.write(df.describe().round(2).T)

        elif option == 'Valores faltantes':

            opt = st.radio('Imputar valores faltantes :', ("Mediana", "Média", "Zero", "Moda"))
            options = st.multiselect('Quais colunas?', df.columns.tolist())

            if st.button("Imputar dados"):
                for i in options:
                    if df[i].dtype == 'object':
                        if opt == "Moda":
                            df.fillna({i: df[i].mode()[0]}, inplace=True)
                            st.success("Valores imputados com sucesso!")
                        else:
                            st.error("Erro! Variáveis categóricas só podem ser preenchidas com a moda")
                    else:
                        if opt == "Média":
                            df.fillna({i: df[i].mean()}, inplace=True)
                        elif opt == "Moda":
                            df.fillna({i: df[i].mode()[0]}, inplace=True)
                        elif opt == "Mediana":
                            df.fillna({i: df[i].median()}, inplace=True)
                        elif opt == "Zero":
                            df.fillna({i: 0}, inplace=True)
                        st.success("Valores imputados com sucesso!")

            st.subheader('Valores faltantes: ')
            heat = msno.matrix(df)
            st.write(heat)
            st.pyplot()
            
        elif option == "Correlação":
            st.subheader('Correlação: ')

            options = st.multiselect('Quais colunas?', df.columns.tolist(), default=list(df.columns))

            if len(df[options].columns) > 19:
                f, ax = plt.subplots(figsize=(15, 12))
            elif len(df[options].columns) > 10:
                f, ax = plt.subplots(figsize=(12, 10))
            else:
                f, ax = plt.subplots(figsize=(9, 7))

            sns.heatmap(df[options].corr(), annot=True, square=True)
            st.pyplot()

        elif option == 'Gráficos de distribuição':

            st.subheader('Gráficos de distribuição: ')
            var_select = st.selectbox('Selecione a variável: ', df.columns)
            if var_select:
                if df[var_select].dtype == 'object':
                    df[var_select].value_counts().plot(kind='bar')
                else:
                    sns.distplot(df[var_select])
                    st.write('Assimetria (Skewness): ', df[var_select].skew(), 'Achatamento (Kurtosis): ', df[var_select].kurtosis())

                plt.title("Distribuição de " + var_select)
                st.pyplot()
        
        elif option == 'Valores atípicos (Outliers)':

            st.subheader('Outliers: ')
            out_select = st.selectbox('Selecione a variável que deseja ver os outliers: ', df.columns)
            if out_select:
                sns.boxplot(df[out_select])
                plt.title("Distribuição de " + out_select)
                st.pyplot()

if __name__ == '__main__':
    main()
