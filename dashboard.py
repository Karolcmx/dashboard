import pandas as pd
import streamlit as st 
import seaborn as sns
import matplotlib.pyplot as plt 


def definicao_parametros_graficos():

    # configurações gerais 
    sns.set_theme()

    plt.rcParams['figure.figsize']= (6,3) #tamanho da figura 
    plt.rcParams['axes.titlesize']=10      #tamanho do título 
    plt.rcParams ['axes.labelsize']= 8     #tamanho dos rótulos dos eixos
    plt.rcParams ['xtick.labelsize']=7     #tamanho dos ticks eixo x
    plt.rcParams ['ytick.labelsize']=7     #tamanho dos ticks eixo x
    plt.rcParams ['legend.fontsize']=8     #tamanho da legenda
    plt.rcParams ['lines.markersize']=4    #tamanho dos marcadores nas linhas
    
   
    
    st.set_page_config(page_title=' Análise vendas por estado', layout='wide')

    return None

def filtra_df(df):

    #Barra Lateral (side Bar)
    st.sidebar.header('Filtros')
    lista_estados= sorted(list(df['seller_state'].str.strip().unique()))
    #Dicionário de correções 
    correcao={
        'MAMÃ' : 'MA'
    }
    df['seller_state'] = df['seller_state'].replace(correcao)

    # Caixa de seleção dos estados
    estados_selecionados = st.sidebar.multiselect('Selecione um Estado', 
                                                options= lista_estados,
                                                default= lista_estados)

    customersDF_filtred= df[df['customer_state'].isin(estados_selecionados)]
    sellersDF_filtred= df[df['seller_state'].isin(estados_selecionados)]
    
    return customersDF_filtred, sellersDF_filtred 

def big_numbers(c_df, s_df):
    st.subheader('Indicadores Gerais')

    total_vendas= c_df ['total_price'].sum()
    total_customers= c_df ['customer_unique_id'].nunique()
    total_sellers= s_df['seller_id'].nunique()

    #Cria 3 colunas 
    col1, col2, col3 = st.columns(3)

    col1.metric ('Vendas Totais', f'R$ {total_vendas:,.2f}')
    col2.metric('Clientes Únicos',f'{total_customers:,.0f}')
    col3.metric('Vendedores Únicos',f'{total_sellers:,.0f}')

    return None 

def visoes_gerais (c_df, s_df):
    st.subheader('Visão Geral das Vendas por Estado')

    col1, col2, col3 = st.columns(3)

    vendas_estados = c_df[['customer_state', 'total_price']].groupby('customer_state').sum().reset_index()

    fig1, ax1 = plt.subplots()
    sns.barplot(data= vendas_estados, x='customer_state', y= 'total_price', palette="Set3", ax=ax1)
    ax1.set_title ('Vendas Totais por Estado')
    plt.xlabel('Estado')
    plt.ylabel('Vendas (R$)')
    col1.pyplot(fig1)

    clientes_estado = c_df[['customer_state', 'customer_unique_id']].groupby('customer_state').nunique().reset_index()
    fig2,ax2 = plt.subplots()
    sns.barplot(data= clientes_estado, x= 'customer_state', y= 'customer_unique_id',palette="Set3", ax= ax2)
    ax2.set_title('Clientes Únicos por Estado')
    plt.xlabel('Estados')
    plt.ylabel('Clientes Únicos')
    col2.pyplot(fig2)

    vendedores_estado = s_df[['seller_state', 'seller_id']].groupby('seller_state').nunique().reset_index()
    fig3,ax3 = plt.subplots()
    sns.barplot(data= vendedores_estado, x= 'seller_state', y= 'seller_id',palette="Set3", ax= ax3)
    ax3.set_title('Vendedores Únicos por Estado')
    plt.xlabel('Estados')
    plt.ylabel('Vendedores Únicos')
    col3.pyplot(fig3)

    return None 

def visoes_temporais (c_df,s_df):
    st.subheader('Visão Temporal por Estado')

    col1,col2,col3 = st.columns(3)

    vendas_temporal = c_df [['order_purchase_year_month', 'total_price']].groupby ('order_purchase_year_month').sum().reset_index()
    fig1,ax1 = plt.subplots()
    sns.lineplot(data= vendas_temporal, x= 'order_purchase_year_month', y= 'total_price',color='m',marker='o', ax= ax1)
    ax1.set_title(f'Vendas (R$)  por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Vendas (R$)')
    plt.xticks (rotation= 60)
    col1.pyplot(fig1)


    clientes_temporal = c_df[['order_purchase_year_month','customer_unique_id']].groupby('order_purchase_year_month').nunique().reset_index()
    fig2, ax2 = plt.subplots()
    sns.lineplot(data = clientes_temporal, x = 'order_purchase_year_month', y= 'customer_unique_id',color='m',marker='o', ax = ax2)
    ax2.set_title(f'Clientes Únicos por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Clientes Únicos')
    plt.xticks(rotation = 60)
    col2.pyplot(fig2)

    vendedores_temporal = s_df[['order_purchase_year_month','seller_id']].groupby('order_purchase_year_month').nunique().reset_index()
    fig3, ax3 = plt.subplots()
    sns.lineplot(data = vendedores_temporal, x = 'order_purchase_year_month', y= 'seller_id',color='m',marker='o', ax = ax3)
    ax3.set_title(f'Vendedores Únicos por mês')
    plt.xlabel('Ano-Mês')
    plt.ylabel('Vendedores Únicos')
    plt.xticks(rotation = 60)
    col3.pyplot(fig3)

    return None


def faturamento_por_categoria(df):
    
    st.subheader('Faturamento e Porcentagem dos produtos vendidos em cada Categoria')
    df2 = df[['product_category_name', 'total_price', 'product_id']].groupby('product_category_name').agg({
            'total_price': 'sum',
            'product_id': 'nunique' }).reset_index().sort_values('total_price', ascending=False).head(10)
        
    df2['product_perc'] = 100 * df2['product_id'] / df2['product_id'].sum()
    
    fig, ax1 = plt.subplots() # um grafico em cima do outro
    sns.barplot(data=df2, x='product_category_name', y = 'total_price',palette="Set3", ax=ax1)
    plt.title('Faturamento por categoria')
    plt.xlabel('Categoria')
    plt.ylabel('Faturamento (R$)')
    plt.xticks(rotation=80)

    ax2 = ax1.twinx() # um eixo em cima do outro
    sns.lineplot(data=df2, x='product_category_name', y='product_perc',color='m', marker='o', ax=ax2)
    plt.ylabel('Porcentagem da quantidade de produtos')
    st.pyplot(fig)
    
    return df2

def quantidade_clientes_por_estado(df):
    st.subheader('Visão de Clientes por Estado')
    col1,col2 = st.columns(2)
    # Agrupa por estado e conta o número de clientes únicos
    clientes_estado = df[['customer_unique_id', 'customer_state']].groupby('customer_state').count().reset_index().sort_values('customer_unique_id', ascending=False)

    # Cria o gráfico
    fig2, ax1 = plt.subplots(figsize=(15, 6))  # Ajuste o tamanho da figura aqui
    sns.barplot(data=clientes_estado, x='customer_state', y='customer_unique_id', palette="Set3", ax=ax1)
    ax1.set_title('Quantidade de Clientes por Estado')
    ax1.set_xlabel('Estado')
    ax1.set_ylabel('Quantidade de Clientes')
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=80)
    
    col1.pyplot(fig2)
    #st.pyplot(fig)


if __name__ == '__main__':
    definicao_parametros_graficos()

    orderDF= pd.read_csv('c:\\pos_graduacao\\programacao_em_python\\datasets\\order_items_cleaned.csv')

    #Título 
    st.title('Dashboard de Análise de Vendas ')

    #Side Bar (Filtros)
    customersDF_filtred, sellersDF_filtred = filtra_df(orderDF)
   
    #Big number (subtítulo)
    big_numbers(customersDF_filtred, sellersDF_filtred)

    #Visões Gerais 
    visoes_gerais (customersDF_filtred, sellersDF_filtred)

    #Visões temporais(mensal) para o estado selecionado 
    visoes_temporais (customersDF_filtred, sellersDF_filtred)

    faturamento_por_categoria(orderDF)

    quantidade_clientes_por_estado(orderDF)

