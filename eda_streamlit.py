import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import missingno as msno 


def main():
    st.title('Análise Exploratória dos Dados')
    st.subheader('Por: Cairo Rocha (https://github.com/bractus)')
    file_ = st.file_uploader('Selecione seu arquivo CSV', type='csv')

    if file_:
        df = pd.read_csv(file_)

        st.write("Linhas", df.shape[0], "Colunas", df.shape[1])

        slider_st = st.slider('Quantidade de linhas', 0, df.shape[0], 5)
        st.dataframe(df.head(slider_st))

        st.subheader('Tipos de variável: ')
        st.write(df.dtypes.value_counts())

        st.subheader('Describe: ')
        st.write(df.describe().round(2).T)

        st.subheader('Skewness: ')
        st.write(df.skew())

        st.subheader('Kurtosis: ')
        st.write(df.kurtosis())

        st.subheader('Valores faltantes: ')
        heat = msno.matrix(df)
        st.write(heat)
        st.pyplot()

        st.subheader('Correlação: ')
        f, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(df.corr(), annot=True, square=True)
        st.pyplot()

        st.subheader('Gráficos de distribuição: ')
        var_select = st.selectbox('Selecione a variável: ', df.columns)
        if var_select:
            if df[var_select].dtype == 'object':
                df[var_select].value_counts().plot(kind='bar')
            else:
                sns.distplot(df[var_select])
            plt.title("Distribuição de " + var_select)
            st.pyplot()

        st.subheader('Outliers: ')
        out_select = st.selectbox('Selecione a variável que deseja ver os outliers: ', df.columns)
        if out_select:
            sns.boxplot(df[out_select])
            plt.title("Distribuição de " + out_select)
            st.pyplot()

if __name__ == '__main__':
    main()
