from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
import pandas as pd
# import json

scope = ['https://spreadsheets.google.com/feeds']
k="456"
creds = ServiceAccountCredentials.from_json_keyfile_name("controle.json", scope)

cliente = gspread.authorize(creds)

#sheet = cliente.open("Ciente Rurais").sheet1 # Open the spreadhseet
sheet=cliente.open_by_key('1Ofc7gL5ftXjbDjxXPhDknTpfImsR3iOjJN7yosq9VjQ').get_worksheet(0)
dados = sheet.get_all_records()  # Get a list of all records
df=pd.DataFrame(dados)

todos = ['','Procedente','Agendada','Realizado','Não Procedente','Pendente']
#inicial = ['Agendada','Não Procedente','Procedente']
datando=[]
n_solicitacao=[]
nome=[]
telefone=[]
predio=[]
status_atual=[]
data=[]
observacao=[]
tipo=[]

#padroes
padrao = '<p style="font-family:Courier; color:Blue; font-size: 15px;">'
infor = '<p style="font-family:Courier; color:Green; font-size: 15px;">'
alerta = '<p style="font-family:Courier; color:Red; font-size: 15px;">'
titulo = '<p style="font-family:Courier; color:Blue; font-size: 20px;">'
cabecalho='<div id="logo" class="span8 small"><a title="Universidade Federal do Tocantins"><img src="https://ww2.uft.edu.br/images/template/brasao.png" alt="Universidade Federal do Tocantins"><span class="portal-title-1"></span><h1 class="portal-title corto">Universidade Federal do Tocantins</h1><span class="portal-description">COINFRA - RURAIS</span></a></div>'

st.sidebar.title('Gestão Rurais')
a=k
#pg=st.sidebar.selectbox('Selecione a Página',['Solicitações em Aberto','Solicitações a Finalizar','Consulta'])
pg=st.sidebar.radio('',['Solicitações em Aberto','Solicitações a Finalizar','Agendamentos'])


if (pg=='Solicitações em Aberto'):
    contador = 0

    st.markdown(cabecalho,unsafe_allow_html=True)
    st.subheader(pg)
    filtro = st.selectbox('Filtrar',['Sem Status','Procedente'],index=1)

    for dic in dados:
        if (dic['Status'] == filtro or (filtro == 'Sem Status' and dic['Status'] == '')) and dic['Região aproximada']!='' and dic['Data de Solicitação'] != '': #'Registro de Reclamação',
            print(dic['Código UFT'])
            n_solicitacao.append(str(dic['Código UFT']))
            tipo.append(dic['Serviços'])
            nome.append(dic['Nome'])
            telefone.append(dic['Telefone'])
            predio.append(dic['Região aproximada'])
            data.append(dic['Data de Solicitação'])
            observacao.append(dic['Descrição'])
            status_atual.append(dic['Status'])
            contador += 1

    st.markdown(padrao + '<b>Solicitações conforme filtro selecionado</b>: ' + str(contador) + '</p>', unsafe_allow_html=True)
    selecionado = str(st.selectbox('Nº da solicitação:',n_solicitacao))
    #print(nome[n_solicitacao.index(selecionado)])
    if (len(n_solicitacao)>0):
        n=n_solicitacao.index(selecionado)

        #apresentar dados da solicitação
        st.markdown(titulo+'<b>Dados da Solicitação</b></p>',unsafe_allow_html=True)
        #st.text('<p style="font-family:Courier; color:Blue; font-size: 20px;">Nome: '+ nome[n]+'</p>',unsafe_allow_html=True)
        st.markdown(padrao + '<b>Serviços</b>: ' + str(tipo[n]) + '</p>', unsafe_allow_html=True)
        st.markdown(padrao+'<b>Nome</b>: '+ str(nome[n])+'</p>',unsafe_allow_html=True)
        st.markdown(padrao+'<b>Telefone</b>: '+ str(telefone[n])+'</p>',unsafe_allow_html=True)
        st.markdown(padrao+'<b>Região Aproximada</b>: '+ str(predio[n])+'</p>',unsafe_allow_html=True)
        st.markdown(padrao+'<b>Data da Solicitação</b>: '+ str(data[n])+'</p>',unsafe_allow_html=True)
        st.markdown(padrao+'<b>Descrição</b>: '+ observacao[n]+'</p>',unsafe_allow_html=True)

        #status=st.selectbox('Selecione o Status',['Selecionar','Ciente','Não é possível atender'])
        #print(status)

        #Data
        d = '01/01/2021'
        # print('Data Agendamento registrada: ' + d_agend[n])
        if (data[n] != ''):
            d = data[n]
        else:
            # st.text('OS sem agendamento registrado ou com data de agendamento anterior a hoje!')
            print('Sem data registrada')
        d = d.replace('/', '-')

        data_ag = datetime.strptime(d, '%d-%m-%Y')

        if (data_ag == ''):
            data_ag = datetime.strptime("01-01-2023", '%d-%m-%Y')

        data_agendamento = st.date_input('Data de Agendamento (ANO/MÊS/DIA)', value=data_ag)
        data = data_agendamento
        data_formatada = str(data.day) + '/' + str(data.month) + '/' + str(data.year)

        cont = 0
        for dic in dados:
            # print(dic['Status'])
            if dic['Status'] == 'Agendada' and data_formatada == dic['Data Programada']:
                #print('Atendeu a condição')
                cont += 1
        st.markdown(padrao + 'Agendamentos existentes na data: '+str(cont)+'</p>', unsafe_allow_html=True)
        #st.markdown('<p id="datepicker--screenreader--message--input" placeholder="DD/MM/YYYY"></p>',unsafe_allow_html=True)
        #data_agendamento.strftime('%d/%m/%Y')
        celula = sheet.find(n_solicitacao[n])
        status=st.selectbox('Status',todos,index = todos.index(status_atual[n]))
        texto = st.text_area('Observação: ')
        s=st.text_input("Senha:",value="", type="password")
        st.markdown(alerta + '<b>Em caso de agendamento, lembrar de alterar o status para Agendada e selecionar a data antes de registrar.</p>', unsafe_allow_html=True)
        botao=st.button('Registrar')
        if (botao==True and s==a):

            st.markdown(infor+'<b>Registro efetuado!</b></p>',unsafe_allow_html=True)

            sheet.update_acell('H'+str(celula.row),status)
            sheet.update_acell('K' + str(celula.row), texto) #observação
            data = data_agendamento
            data_formatada = str(data.day) + '/' + str(data.month) + '/' + str(data.year)
            sheet.update_acell('O' + str(celula.row), data_formatada)

        elif (botao==True and s!=a):
            st.markdown(alerta + '<b>Senha incorreta!</b></p>', unsafe_allow_html=True)
    else:
        st.markdown(infor + '<b>Não há itens na condição '+ pg +'</b></p>', unsafe_allow_html=True)
elif pg=='Solicitações a Finalizar':
    contador = 0
    for dic in dados:
        if dic['Status'] == 'Agendada' and dic['Região aproximada']!='' and dic['Data de Solicitação'] != '': #'Registro de Reclamação',
            print(dic['Código UFT'])
            n_solicitacao.append(str(dic['Código UFT']))
            tipo.append(dic['Serviços'])
            nome.append(dic['Nome'])
            telefone.append(dic['Telefone'])
            predio.append(dic['Região aproximada'])
            data.append(dic['Data de Solicitação'])
            observacao.append(dic['Descrição'])
            status_atual.append(dic['Status'])
            contador += 1

    st.markdown(cabecalho,unsafe_allow_html=True)
    st.subheader(pg)
    st.markdown(padrao + '<b>Solicitações a finalizar</b>: ' + str(contador) + '</p>', unsafe_allow_html=True)
    selecionado = st.selectbox('Nº da solicitação:',n_solicitacao)
    #print(nome[n_solicitacao.index(selecionado)])
    if (len(n_solicitacao) > 0):
        n = n_solicitacao.index(selecionado)

        # apresentar dados da solicitação
        st.markdown(titulo + '<b>Dados da Solicitação</b></p>', unsafe_allow_html=True)
        # st.text('<p style="font-family:Courier; color:Blue; font-size: 20px;">Nome: '+ nome[n]+'</p>',unsafe_allow_html=True)
        st.markdown(padrao + '<b>Serviços</b>: ' + str(tipo[n]) + '</p>', unsafe_allow_html=True)
        st.markdown(padrao+'<b>Nome</b>: '+ str(nome[n])+'</p>',unsafe_allow_html=True)
        st.markdown(padrao+'<b>Telefone</b>: '+ str(telefone[n])+'</p>',unsafe_allow_html=True)
        st.markdown(padrao+'<b>Região Aproximada</b>: '+ str(predio[n])+'</p>',unsafe_allow_html=True)
        st.markdown(padrao+'<b>Data da Solicitação</b>: '+ str(data[n])+'</p>',unsafe_allow_html=True)
        st.markdown(padrao+'<b>Descrição</b>: '+ observacao[n]+'</p>',unsafe_allow_html=True)

        # status=st.selectbox('Selecione o Status',['Selecionar','Ciente','Não é possível atender'])
        # print(status)
        celula = sheet.find(n_solicitacao[n])
        status=st.selectbox('Status',todos,index = todos.index(status_atual[n]))
        texto = st.text_area('Observação: ')
        s=st.text_input("Senha:",value="", type="password")
        botao=st.button('Registrar')
        if (botao==True and s==a):
            st.markdown(infor+'<b>Registro efetuado!</b></p>',unsafe_allow_html=True)

            sheet.update_acell('H'+str(celula.row),status)
            sheet.update_acell('K' + str(celula.row), texto) #observação

        elif (botao==True and s!=a):
            st.markdown(alerta + '<b>Senha incorreta!</b></p>', unsafe_allow_html=True)
    else:
        st.markdown(infor + '<b>Não há itens na condição ' + pg + '</b></p>', unsafe_allow_html=True)
elif pg=='Agendamentos':
    contador = 0
    st.markdown(cabecalho, unsafe_allow_html=True)
    st.subheader(pg)
    st.markdown(padrao + '<b>' + 'Codigo' + ' -  ' + 'Nome' + ' - ' + 'Telefone' + ' - ' + 'Região aproximada' + ' - ' + 'Data Programada' +  '</b></p>',
                unsafe_allow_html=True)
    st.markdown(padrao + '</p>', unsafe_allow_html=True)
    for dic in dados:
        #print(dic['Status'])
        if dic['Status'] == 'Agendada':
            print('Atendeu a condição')
            contador += 1
            st.markdown(padrao + '<b>'+str(dic['Código UFT'])+' - ' + str(dic['Nome']) + ' - ' + str(dic['Telefone'])+ ' - ' + dic['Região aproximada']+  ' - ' + str(dic['Data Programada'])+'</b></p>', unsafe_allow_html=True)
            st.markdown(padrao + '</p>', unsafe_allow_html=True)


