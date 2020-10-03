import pymysql.cursors
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class MenuInicial():
    def __init__(self):
        self.menuinicial = Tk()
        self.menuinicial.title("Menu Inicial")
        Button(self.menuinicial, text='Contato', bg="blue1", width=10, command=self.destroiContato).grid(row=0, column=0, padx=5, pady=5)
        Button(self.menuinicial, text='Bot', bg="red", width=10, command=self.destroiBot).grid(row=0, column=1, padx=5, pady=5)
        self.menuinicial.mainloop()

    def destroiContato(self):
        self.menuinicial.destroy()
        Contato()

    def destroiBot(self):
        self.menuinicial.destroy()
        Bot()

class Contato():
    def __init__(self):
        self.contato = Tk()
        self.contato.title("Contatos")
        Button(self.contato, text='Adicionar', bg="blue1", width=10, command=self.adicionarContato).grid(row=4, column=0, padx=5, pady=5)
        self.adicionar = Entry(self.contato)
        self.adicionar.grid(row=4, column=1, padx=5, pady=5)
        Button(self.contato, text='Remover', bg="red", width=10, command=self.removerContato).grid(row=5, column=0, padx=5, pady=5)
        Button(self.contato, text='Voltar', bg="orange", width=10, command=self.voltar).grid(row=5, column=1,padx=5, pady=5)
        self.atualiza()
        self.contato.mainloop()

    def voltar(self):
        self.contato.destroy()
        MenuInicial()

    def atualiza(self):
        global conexao
        self.tree = ttk.Treeview(self.contato, selectmode='browse', column=('column1', 'column2'), show='headings')
        self.tree.column('column1', width=110, stretch=NO)
        self.tree.heading('#1', text='Id')
        self.tree.column('column2', width=110, stretch=NO)
        self.tree.heading('#2', text='Nome')
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='BotWhatsapp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo('Erro_1', 'Erro de Conexão')
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select * from Contatos')
                self.listaNomes = cursor.fetchall()
        except:
            messagebox.showinfo('Erro_2', 'Erro no Banco de Dados')

        for i in self.listaNomes:
            lisNomes = []
            lisNomes.append(i['id'])
            lisNomes.append(i['contatos'])
            self.tree.insert('', END, values=lisNomes, iid=i['id'], tag='1')
        self.tree.grid(row=0, column=0, padx=5, pady=5, rowspan=3, columnspan=2)

    def adicionarContato(self):
        if self.adicionar.get() != '':
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into contatos(contatos) values(%s)',(self.adicionar.get()))
                    conexao.commit()
                    self.adicionar.delete(0,END)
                    self.atualiza()


            except:
                messagebox.showinfo('Erro_4', 'Erro no Banco de Dados')
                self.adicionar.delete(0, END)

        else:
            messagebox.showinfo('Erro_3', 'Campo em Branco')

    def removerContato(self):
        idDeletar = int(self.tree.selection()[0])
        try:
            with conexao.cursor() as cursor:
                cursor.execute('delete from contatos where id = {}'.format(idDeletar))
                conexao.commit()
                self.atualiza()


        except:
                messagebox.showinfo('Erro_5', 'Erro no Banco de Dados')

class Bot():

    def __init__(self):
        self.bot = Tk()
        self.bot.title('Bot')
        Label(self.bot, text='Digite sua Mensagem').grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        self.mensagem = Entry(self.bot, width=60)
        self.mensagem.grid(row=1, column=0, padx=5, pady=5, columnspan=2)
        Button(self.bot, text='Voltar', bg='orange', command=self.voltar, width=30).grid(row=2, column=1, padx=5, pady=5)
        Button(self.bot, text='Enviar', bg='green3', command=self.verificaCampo,width=30).grid(row=2, column=0, padx=5, pady=5)
        self.bot.mainloop()

    def voltar(self):
        self.bot.destroy()
        MenuInicial()

    def verificaCampo(self):
        if self.mensagem.get() != '':
            self.conexao_Banco()
        else:
            messagebox.showinfo('Erro_6', 'Preencha todos os Campos')

    def conexao_Banco(self):
        try:
            conexao = pymysql.connect(
                host='localhost',
                user='root',
                password='',
                db='BotWhatsapp',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
        except:
            messagebox.showinfo('Erro_8', 'Erro de Conexão')
        try:
            with conexao.cursor() as cursor:
                cursor.execute('select contatos from Contatos')
                self.nomes = cursor.fetchall()



        except:
            messagebox.showinfo('Erro_7', 'Erro no Banco de Dados')

        self.pessoas = []
        for nome in self.nomes:
            self.pessoas.append(nome['contatos'])
        self.whatsappInicio()

    def whatsappInicio(self):
        self.texto = self.mensagem.get()
        opçoes = webdriver.ChromeOptions()
        opçoes.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(executable_path=r'C:\Users\Aldevair\.wdm\drivers\chromedriver\win32\85.0.4183.87\chromedriver')
        self.whatsappFim()

    def whatsappFim(self):
        self.driver.get('https://web.whatsapp.com')
        time.sleep(15)
        for nome in self.pessoas:
            pesquisa = self.driver.find_element_by_xpath('//div[contains(@class,"copyable-text selectable-text")]')
            time.sleep(3)
            pesquisa.click()
            pesquisa.send_keys(nome)
            pesquisa.send_keys(Keys.ENTER)
            texto = self.driver.find_element_by_class_name('_3uMse')
            time.sleep(3)
            texto.click()
            texto.send_keys(self.texto)
            enviar = self.driver.find_element_by_xpath("//span[@data-icon='send']")
            time.sleep(3)
            enviar.click()
        self.mensagem.delete(0, END)


MenuInicial()