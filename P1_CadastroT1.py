# -*- coding: latin-1 -*-
#----------------------- Imports--------------------------------------------------------------------
from tkinter import *
from tkinter import messagebox as mbox
import psycopg2 as pg
from unicodedata import normalize as norm
from tabulate import tabulate
import tkinter as tk
import docx
import json
from tkinter import Tk, Text, Scrollbar
#---------------------------------------------------------------------------------------------------

#-----------------------Importar JSON---------------------------------------------------------------
def exportar_JSON():
        try:
            con = pg.connect(
                database="adlpyumj",
                user="adlpyumj",
                password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                host="drona.db.elephantsql.com",
                port="5432"
            )
        except Exception as erro:
            mbox.showinfo("Erro", str(erro))
            return

        cur = con.cursor()
        sql = "SELECT * FROM tb_produtos"
        
        cur.execute(sql)
        linhas = cur.fetchall()

       # Converter as linhas para um formato JSON
        data = []
        for linha in linhas:
            produto = {
                "ID": linha[0],
                "Codigo": linha[1],
                "Nome": linha[2],
                "Valor Compra": str(linha[3]),
                "Valor Venda": str(linha[4]),
                "Quantidade": linha[5]
            }
            data.append(produto)

        # Exportar os dados para um arquivo JSON
        with open("output.json", "w") as file:
            json.dump(data, file, indent=4)

        # ...

        con.close()

        # Ler o arquivo JSON e exibir em uma janela
        with open("output.json", "r") as file:
            conteudo = json.load(file)

        texto = json.dumps(conteudo, indent=4)

        janela_sobre = Tk()
        janela_sobre.title("JSON")
        janela_sobre.iconbitmap("images/icon.ico")
        janela_sobre.geometry("400x300")

        # Criar a barra de rolagem vertical
        scrollbar = Scrollbar(janela_sobre)
        scrollbar.pack(side="right", fill="y")

        # Criar o widget Text
        texto_widget = Text(janela_sobre, wrap="none", yscrollcommand=scrollbar.set)
        texto_widget.insert("1.0", texto)
        texto_widget.pack(side="left", fill="both")

        # Configurar a barra de rolagem
        scrollbar.config(command=texto_widget.yview)

        janela_sobre.mainloop()
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Relatório Estoque Baixo---------------------------------------------
def abrir_janela_relatorio_estoque_baixo():
        try:
            con = pg.connect(
                database="adlpyumj",
                user="adlpyumj",
                password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                host="drona.db.elephantsql.com",
                port="5432"
            )
        except Exception as erro:
            mbox.showinfo("Erro", str(erro))
            return

        cur = con.cursor()
        sql = "SELECT * FROM tb_produtos WHERE qtd_estoque < 5"
        cur.execute(sql)
        linhas = cur.fetchall()

        tabela = tabulate(linhas, headers=["ID", "Codigo", "Nome", "Valor Compra", "Valor Venda", "Quantidade"], tablefmt="grid")

        janela_relatorio = Tk()
        janela_relatorio.title("Relatório de Produtos Estoque Baixo")
        janela_relatorio.iconbitmap("images/icon.ico")

        label_tabela = Label(janela_relatorio, text=tabela, justify="left", font="Courier")
        label_tabela.pack()

        janela_relatorio.mainloop()

        con.close()
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Relatório Estoque---------------------------------------------------
def abrir_janela_relatorio_estoque():
        try:
            con = pg.connect(
                database="adlpyumj",
                user="adlpyumj",
                password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                host="drona.db.elephantsql.com",
                port="5432"
            )
        except Exception as erro:
            mbox.showinfo("Erro", str(erro))
            return

        cur = con.cursor()
        sql = "SELECT * FROM tb_produtos"
        cur.execute(sql)
        linhas = cur.fetchall()

        tabela = tabulate(linhas, headers=["ID", "Codigo", "Nome", "Valor Compra", "Valor Venda", "Quantidade"], tablefmt="grid")

        janela_relatorio = Tk()
        janela_relatorio.title("Relatório de Produtos Estoque")
        janela_relatorio.iconbitmap("images/icon.ico")

        label_tabela = Label(janela_relatorio, text=tabela, justify="left", font="Courier")
        label_tabela.pack()

        janela_relatorio.mainloop()

        con.close()
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Excluir Cadastro Produto--------------------------------------------
def abrir_janela_excluir_cadastro_produto():
    janela_excluir = tk.Toplevel(root)
    janela_excluir.title("Editar")
    janela_excluir.iconbitmap("images/icon.ico")
    janela_excluir.geometry("400x370")  # tamanho da janela
    janela_excluir.resizable(False, False)


    def fechar_janela__excluir_produto():
        # Função para fechar a janela de cadastro e voltar para a janela principal
        janela_excluir.destroy()
        abrir_janela_menu()  # Exibe novamente a janela Menu

    def pesquisar_produto():
        try:
            codigo = excluir_frame2.entry1.get()

            try:
                con = pg.connect(
                    database="adlpyumj",
                    user="adlpyumj",
                    password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                    host="drona.db.elephantsql.com",
                    port="5432"
                )

                cur = con.cursor()
                cur.execute("SELECT * FROM tb_produtos WHERE codigo_produto = %s", (codigo,))
                produto = cur.fetchone()

                if produto:
                    excluir_frame5.entry2.delete(0, tk.END)
                    excluir_frame6.entry3.delete(0, tk.END)
                    excluir_frame7.entry4.delete(0, tk.END)
                    excluir_frame8.entry5.delete(0, tk.END)

                    excluir_frame5.entry2.insert(0, produto[1])  # Código do produto
                    excluir_frame6.entry3.insert(0, produto[2])  # Nome do produto
                    excluir_frame7.entry4.insert(0, produto[3])  # Valor do produto
                    excluir_frame8.entry5.insert(0, produto[5])  # Quantidade do produto
                else:
                    mbox.showinfo("Excluir", "Produto não encontrado!")

                con.close()

            except Exception as erro:
                mbox.showinfo("Erro", str(erro))
        except ValueError:
            mbox.showinfo("Excluir", "Produto não encontrado!")

    def excluir_produto():
        try:
            codigo = excluir_frame5.entry2.get()
            nome = excluir_frame6.entry3.get()
            valor = float(excluir_frame7.entry4.get())
            valor_venda = valor * 1.25
            quantidade = int(excluir_frame8.entry5.get())

            try:
                con = pg.connect(
                    database="adlpyumj",
                    user="adlpyumj",
                    password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                    host="drona.db.elephantsql.com",
                    port="5432"
                )

                cur = con.cursor()
                cur.execute("DELETE FROM tb_produtos WHERE codigo_produto = %s", (codigo,))
                con.commit()
                con.close()

                mbox.showinfo("Excluir", "Produto excluído com sucesso!")
                fechar_janela__excluir_produto()
            except Exception as erro:
                mbox.showinfo("Erro", str(erro))
        except ValueError:
            mbox.showinfo("Editar", str(erro))

#-------------------------Frame 1------------------------------------------------------------
    excluir_frame1 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame1.pack(fill=X)

    excluir_frame1.titulo = Label(excluir_frame1)
    excluir_frame1.titulo["text"] = "Pesquisar Produto"
    excluir_frame1.titulo["bg"] = "#3B5998"
    excluir_frame1.titulo["fg"] = "#FFFFFF"
    excluir_frame1.titulo["font"] = "Helvetica 16 bold"
    excluir_frame1.titulo.pack(side=TOP,fill=X)

#-------------------------Frame 2------------------------------------------------------------
    excluir_frame2 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame2.pack(fill=X)

    excluir_frame2.label1 = Label(excluir_frame2, text="Codigo Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    excluir_frame2.label1.pack(side=LEFT, pady=10)
    excluir_frame2.entry1 = Entry(excluir_frame2, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    excluir_frame2.entry1.pack(side=LEFT, pady=10)

#-------------------------Frame 3------------------------------------------------------------
    excluir_frame3 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame3.pack(fill=X)

    pesquisar_button = tk.Button(excluir_frame3, text="Pesquisar", width=20, bg="blue", fg="white", command=pesquisar_produto)
    pesquisar_button.pack(side=RIGHT, padx=12)


#-------------------------Frame 4------------------------------------------------------------
    excluir_frame4 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame4.pack(fill=X)

    excluir_frame4.titulo = Label(excluir_frame4)
    excluir_frame4.titulo["text"] = "Excluir Produto"
    excluir_frame4.titulo["bg"] = "#3B5998"
    excluir_frame4.titulo["fg"] = "#FFFFFF"
    excluir_frame4.titulo["font"] = "Helvetica 16 bold"
    excluir_frame4.titulo.pack(side=TOP,fill=X,pady=10)

#-------------------------Frame 5------------------------------------------------------------
    excluir_frame5 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame5.pack(fill=X)

    excluir_frame5.label2 = Label(excluir_frame5, text="Codigo Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    excluir_frame5.label2.pack(side=LEFT, pady=10)
    excluir_frame5.entry2 = Entry(excluir_frame5, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    excluir_frame5.entry2.pack(side=LEFT, pady=10)

#-------------------------Frame 6------------------------------------------------------------
    excluir_frame6 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame6.pack(fill=X)

    excluir_frame6.label3 = Label(excluir_frame6, text="Nome Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    excluir_frame6.label3.pack(side=LEFT, pady=10)
    excluir_frame6.entry3 = Entry(excluir_frame6, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    excluir_frame6.entry3.pack(side=LEFT, pady=10)

#-------------------------Frame 7------------------------------------------------------------
    excluir_frame7 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame7.pack(fill=X)

    excluir_frame7.label4 = Label(excluir_frame7, text="Valor Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    excluir_frame7.label4.pack(side=LEFT, pady=10)
    excluir_frame7.entry4 = Entry(excluir_frame7, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    excluir_frame7.entry4.pack(side=LEFT, pady=10)

#-------------------------Frame 8------------------------------------------------------------
    excluir_frame8 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame8.pack(fill=X)

    excluir_frame8.label5 = Label(excluir_frame8, text="Quantidade Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    excluir_frame8.label5.pack(side=LEFT, pady=10)
    excluir_frame8.entry5 = Entry(excluir_frame8, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    excluir_frame8.entry5.pack(side=LEFT, pady=10)

#-------------------------Frame 9-----------------------------------------------------------
    excluir_frame9 = Frame(janela_excluir, bg="#FFFFFF", height=20)
    excluir_frame9.pack(fill=X)
#----------------------------------------------------------------------------------------------

    # Criação dos botões na janela de cadastro
    excluir_button = tk.Button(excluir_frame9, text="Excluir", width=20, bg="blue", fg="white", command=excluir_produto)
    excluir_button.pack(side=RIGHT, padx=12)

    close_button = tk.Button(excluir_frame9, text="Fechar", width=20, bg="blue", fg="white", command=fechar_janela__excluir_produto)
    close_button.pack(side=RIGHT)
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Editar Cadastro Produto---------------------------------------------
def abrir_janela_editar_cadastro_produto():
    janela_editar = tk.Toplevel(root)
    janela_editar.title("Editar")
    janela_editar.iconbitmap("images/icon.ico")
    janela_editar.geometry("400x370")  # tamanho da janela
    janela_editar.resizable(False, False)


    def fechar_janela__editar_produto():
        # Função para fechar a janela de cadastro e voltar para a janela principal
        janela_editar.destroy()
        abrir_janela_menu()  # Exibe novamente a janela Menu

    def pesquisar_produto():
        try:
            codigo = editar_frame2.entry1.get()

            try:
                con = pg.connect(
                    database="adlpyumj",
                    user="adlpyumj",
                    password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                    host="drona.db.elephantsql.com",
                    port="5432"
                )

                cur = con.cursor()
                cur.execute("SELECT * FROM tb_produtos WHERE codigo_produto = %s", (codigo,))
                produto = cur.fetchone()

                if produto:
                    editar_frame5.entry2.delete(0, tk.END)
                    editar_frame6.entry3.delete(0, tk.END)
                    editar_frame7.entry4.delete(0, tk.END)
                    editar_frame8.entry5.delete(0, tk.END)

                    editar_frame5.entry2.insert(0, produto[1])  # Código do produto
                    editar_frame6.entry3.insert(0, produto[2])  # Nome do produto
                    editar_frame7.entry4.insert(0, produto[3])  # Valor do produto
                    editar_frame8.entry5.insert(0, produto[5])  # Quantidade do produto
                    janela_editar.deiconify()  # Exibe a janela editar cadastro produto
                else:
                    mbox.showinfo("Editar", "Produto não encontrado!")

                con.close()

            except Exception as erro:
                mbox.showinfo("Erro", str(erro))
        except ValueError:
            mbox.showinfo("Editar", "Produto não encontrado!")

    def editar_produto():
        try:
            codigo = editar_frame5.entry2.get()
            nome = editar_frame6.entry3.get()
            valor = float(editar_frame7.entry4.get())
            valor_venda = valor * 1.25
            quantidade = int(editar_frame8.entry5.get())

            try:
                con = pg.connect(
                    database="adlpyumj",
                    user="adlpyumj",
                    password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                    host="drona.db.elephantsql.com",
                    port="5432"
                )

                cur = con.cursor()
                cur.execute("UPDATE tb_produtos SET nome_produto = %s, valor_compra = %s, valor_venda = %s, qtd_estoque = %s WHERE codigo_produto = %s", (nome, valor, valor_venda, quantidade, codigo))
                con.commit()
                con.close()

                mbox.showinfo("Editar", "Produto alterado com sucesso!")
                fechar_janela__editar_produto()
            except Exception as erro:
                mbox.showinfo("Erro", str(erro))
        except ValueError:
            mbox.showinfo("Editar", "Preencha todos os campos com valores válidos!")

#-------------------------Frame 1------------------------------------------------------------
    editar_frame1 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame1.pack(fill=X)

    editar_frame1.titulo = Label(editar_frame1)
    editar_frame1.titulo["text"] = "Pesquisar Produto"
    editar_frame1.titulo["bg"] = "#3B5998"
    editar_frame1.titulo["fg"] = "#FFFFFF"
    editar_frame1.titulo["font"] = "Helvetica 16 bold"
    editar_frame1.titulo.pack(side=TOP,fill=X)

#-------------------------Frame 2------------------------------------------------------------
    editar_frame2 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame2.pack(fill=X)

    editar_frame2.label1 = Label(editar_frame2, text="Codigo Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    editar_frame2.label1.pack(side=LEFT, pady=10)
    editar_frame2.entry1 = Entry(editar_frame2, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    editar_frame2.entry1.pack(side=LEFT, pady=10)
    editar_frame2.entry1.focus_set()


#-------------------------Frame 3------------------------------------------------------------
    editar_frame3 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame3.pack(fill=X)

    pesquisar_button = tk.Button(editar_frame3, text="Pesquisar", width=20, bg="blue", fg="white", command=pesquisar_produto)
    pesquisar_button.pack(side=RIGHT, padx=12)


#-------------------------Frame 4------------------------------------------------------------
    editar_frame4 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame4.pack(fill=X)

    editar_frame4.titulo = Label(editar_frame4)
    editar_frame4.titulo["text"] = "Editar Produto"
    editar_frame4.titulo["bg"] = "#3B5998"
    editar_frame4.titulo["fg"] = "#FFFFFF"
    editar_frame4.titulo["font"] = "Helvetica 16 bold"
    editar_frame4.titulo.pack(side=TOP,fill=X,pady=10)

#-------------------------Frame 5------------------------------------------------------------
    editar_frame5 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame5.pack(fill=X)

    editar_frame5.label2 = Label(editar_frame5, text="Codigo Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    editar_frame5.label2.pack(side=LEFT, pady=10)
    editar_frame5.entry2 = Entry(editar_frame5, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    editar_frame5.entry2.pack(side=LEFT, pady=10)

#-------------------------Frame 6------------------------------------------------------------
    editar_frame6 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame6.pack(fill=X)

    editar_frame6.label3 = Label(editar_frame6, text="Nome Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    editar_frame6.label3.pack(side=LEFT, pady=10)
    editar_frame6.entry3 = Entry(editar_frame6, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    editar_frame6.entry3.pack(side=LEFT, pady=10)

#-------------------------Frame 7------------------------------------------------------------
    editar_frame7 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame7.pack(fill=X)

    editar_frame7.label4 = Label(editar_frame7, text="Valor Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    editar_frame7.label4.pack(side=LEFT, pady=10)
    editar_frame7.entry4 = Entry(editar_frame7, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    editar_frame7.entry4.pack(side=LEFT, pady=10)

#-------------------------Frame 8------------------------------------------------------------
    editar_frame8 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame8.pack(fill=X)

    editar_frame8.label5 = Label(editar_frame8, text="Quantidade Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    editar_frame8.label5.pack(side=LEFT, pady=10)
    editar_frame8.entry5 = Entry(editar_frame8, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    editar_frame8.entry5.pack(side=LEFT, pady=10)

#-------------------------Frame 9-----------------------------------------------------------
    editar_frame9 = Frame(janela_editar, bg="#FFFFFF", height=20)
    editar_frame9.pack(fill=X)
#----------------------------------------------------------------------------------------------

    # Criação dos botões na janela de cadastro
    editar_button = tk.Button(editar_frame9, text="Ok", width=20, bg="blue", fg="white", command=editar_produto)
    editar_button.pack(side=RIGHT, padx=12)

    close_button = tk.Button(editar_frame9, text="Fechar", width=20, bg="blue", fg="white", command=fechar_janela__editar_produto)
    close_button.pack(side=RIGHT)
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Cadastro Produto----------------------------------------------------
def abrir_janela_cadastro_produto():
    # Função para abrir a janela de cadastro
    janela_cadastro = tk.Toplevel(root)
    janela_cadastro.title("Cadastro")
    janela_cadastro.iconbitmap("images/icon.ico")
    janela_cadastro.geometry("400x250")  # tamanho da janela
    janela_cadastro.resizable(False, False)


    def fechar_janela_cadastro_produto():
        # Função para fechar a janela de cadastro e voltar para a janela principal
        janela_cadastro.destroy()
        abrir_janela_menu()  # Exibe novamente a janela Menu

#-------------------------Frame 1------------------------------------------------------------
    registration_frame1 = Frame(janela_cadastro, bg="#FFFFFF", height=20)
    registration_frame1.pack(fill=X)

    registration_frame1.titulo = Label(registration_frame1)
    registration_frame1.titulo["text"] = "Cadastrar Produtos"
    registration_frame1.titulo["bg"] = "#3B5998"
    registration_frame1.titulo["fg"] = "#FFFFFF"
    registration_frame1.titulo["font"] = "Helvetica 16 bold"
    registration_frame1.titulo.pack(side=TOP,fill=X)

#-------------------------Frame 2------------------------------------------------------------
    registration_frame2 = Frame(janela_cadastro, bg="#FFFFFF", height=20)
    registration_frame2.pack(fill=X)

    registration_frame2.label2 = Label(registration_frame2, text="Codigo Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    registration_frame2.label2.pack(side=LEFT, pady=10)
    registration_frame2.entry2 = Entry(registration_frame2, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    registration_frame2.entry2.pack(side=LEFT, pady=10)
    registration_frame2.entry2.focus_set()

#-------------------------Frame 3------------------------------------------------------------
    registration_frame3 = Frame(janela_cadastro, bg="#FFFFFF", height=20)
    registration_frame3.pack(fill=X)

    registration_frame3.label3 = Label(registration_frame3, text="Nome Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    registration_frame3.label3.pack(side=LEFT, pady=10)
    registration_frame3.entry3 = Entry(registration_frame3, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    registration_frame3.entry3.pack(side=LEFT, pady=10)

#-------------------------Frame 4------------------------------------------------------------
    registration_frame4 = Frame(janela_cadastro, bg="#FFFFFF", height=20)
    registration_frame4.pack(fill=X)

    registration_frame4.label4 = Label(registration_frame4, text="Valor Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    registration_frame4.label4.pack(side=LEFT, pady=10)
    registration_frame4.entry4 = Entry(registration_frame4, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    registration_frame4.entry4.pack(side=LEFT, pady=10)

#-------------------------Frame 5------------------------------------------------------------
    registration_frame5 = Frame(janela_cadastro, bg="#FFFFFF", height=20)
    registration_frame5.pack(fill=X)

    registration_frame5.label5 = Label(registration_frame5, text="Quantidade Produto:", bg="#FFFFFF", font=("Helvetica", 12))
    registration_frame5.label5.pack(side=LEFT, pady=10)
    registration_frame5.entry5 = Entry(registration_frame5, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    registration_frame5.entry5.pack(side=LEFT, pady=10)

#-------------------------Frame 6-----------------------------------------------------------
    registration_frame6 = Frame(janela_cadastro, bg="#FFFFFF", height=20)
    registration_frame6.pack(fill=X)
#----------------------------------------------------------------------------------------------

    def cadastrar_produto():
        try:
            codigo = registration_frame2.entry2.get()
            nome = registration_frame3.entry3.get()
            valor = float(registration_frame4.entry4.get())
            valor_venda = valor * 1.25
            quantidade = int(registration_frame5.entry5.get())

            try:
                con = pg.connect(
                database="adlpyumj",
                user="adlpyumj",
                password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                host="drona.db.elephantsql.com",
                port="5432"
                )

                sql = "INSERT INTO tb_produtos (codigo_produto, nome_produto, valor_compra, valor_venda, qtd_estoque) \
                                VALUES (%s, %s, %s, %s, %s)"
                cur = con.cursor()
                cur.execute(sql, (codigo, nome, valor, valor_venda, quantidade))
                con.commit()
                con.close()

                mbox.showinfo("Produtos", "Produto cadastrado com sucesso!")
                fechar_janela_cadastro_produto()

            except Exception as erro:
                mbox.showinfo("Erro", str(erro))
        except ValueError:
            mbox.showinfo("Produtos", "Preencha todos os campos com valores válidos!")

    
    # Criação dos botões na janela de cadastro
    registration_button = tk.Button(registration_frame6, text="Cadastrar", width=20, bg="blue", fg="white", command=cadastrar_produto)
    registration_button.pack(side=RIGHT, padx=12)

    close_button = tk.Button(registration_frame6, text="Fechar", width=20, bg="blue", fg="white", command=fechar_janela_cadastro_produto)
    close_button.pack(side=RIGHT)
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Menu----------------------------------------------------------------
def abrir_janela_menu():
    # Função para abrir a janela de menu
    menu_window = tk.Toplevel(root)
    menu_window.title("Menu")
    menu_window.iconbitmap("images/icon.ico")
    menu_window.geometry("450x590")  # tamanho da janela
    menu_window.resizable(False, False)
     

    def fechar_janela_menu():
        # Função para fechar a janela de cadastro e voltar para a janela principal
        menu_window.destroy()
        root.deiconify()  # Exibe novamente a janela principal

    def abrir_editar():
        menu_window.withdraw()
        abrir_janela_editar_cadastro_produto()

    def abrir_cadastrar():
        menu_window.withdraw()
        abrir_janela_cadastro_produto()

    def abrir_excluir():
        menu_window.withdraw()
        abrir_janela_excluir_cadastro_produto()

    def abrir_novo_usuario():
        menu_window.withdraw()
        abrir_janela_novo_usuario()

#-------------------------Frame 1------------------------------------------------------------
    menu_frame1 = Frame(menu_window, bg="#FFFFFF", height=20)
    menu_frame1.pack(fill=X, ipady=10)

    menu_frame1.titulo = Label(menu_frame1)
    menu_frame1.titulo["text"] = "OPÇÕES"
    menu_frame1.titulo["bg"] = "#3B5998"
    menu_frame1.titulo["fg"] = "#FFFFFF"
    menu_frame1.titulo["font"] = "Helvetica 16 bold"
    menu_frame1.titulo.pack(side=TOP,fill=X)

#-------------------------Frame 2------------------------------------------------------------
    menu_frame2 = Frame(menu_window, bg="#FFFFFF", height=20)
    menu_frame2.pack(fill=X, ipady=10)

    cadastro_button = tk.Button(menu_frame2, text="Cadastrar Produto", width=20, bg="blue", fg="white", font=("Helvetica", 12), command=abrir_cadastrar)
    cadastro_button.pack(side=TOP,fill=X, ipady=10)

#-------------------------Frame 3------------------------------------------------------------
    menu_frame3 = Frame(menu_window, bg="#FFFFFF", height=20)
    menu_frame3.pack(fill=X, ipady=10)

    relatorio_button = tk.Button(menu_frame3, text="Editar Produto Cadastrado", width=20, bg="blue", fg="white", font=("Helvetica", 12), command=abrir_editar)
    relatorio_button.pack(side=TOP,fill=X, ipady=10)

#-------------------------Frame 4------------------------------------------------------------
    menu_frame4= Frame(menu_window, bg="#FFFFFF", height=20)
    menu_frame4.pack(fill=X, ipady=10)

    relatorio_button = tk.Button(menu_frame4, text="Excluir Produto Cadastrado", width=20, bg="blue", fg="white", font=("Helvetica", 12), command=abrir_excluir)
    relatorio_button.pack(side=TOP,fill=X, ipady=10)

#-------------------------Frame 5------------------------------------------------------------
    menu_frame5 = Frame(menu_window, bg="#FFFFFF", height=20)
    menu_frame5.pack(fill=X, ipady=10)

    relatorio_button = tk.Button(menu_frame5, text="Relatório Estoque", width=20, bg="blue", fg="white", font=("Helvetica", 12), command=abrir_janela_relatorio_estoque)
    relatorio_button.pack(side=TOP,fill=X, ipady=10)

#-------------------------Frame 6------------------------------------------------------------
    menu_frame6 = Frame(menu_window, bg="#FFFFFF", height=20)
    menu_frame6.pack(fill=X, ipady=10)

    relatorio_button = tk.Button(menu_frame6, text="Relatório Estoque Baixo", width=20, bg="blue", fg="white", font=("Helvetica", 12), command=abrir_janela_relatorio_estoque_baixo)
    relatorio_button.pack(side=TOP,fill=X, ipady=10)

#-------------------------Frame 7------------------------------------------------------------
    menu_frame7 = Frame(menu_window, bg="#FFFFFF", height=20)
    menu_frame7.pack(fill=X, ipady=10)

    relatorio_button = tk.Button(menu_frame7, text="Cadastrar Novo Usuário", width=20, bg="blue", fg="white", font=("Helvetica", 12), command=abrir_novo_usuario)
    relatorio_button.pack(side=TOP,fill=X, ipady=10)

#-------------------------Frame 8------------------------------------------------------------
    menu_frame8 = Frame(menu_window, bg="#FFFFFF", height=20)
    menu_frame8.pack(fill=X, ipady=10)

    relatorio_button = tk.Button(menu_frame8, text="Exportar JSON", width=20, bg="blue", fg="white", font=("Helvetica", 12), command=exportar_JSON)
    relatorio_button.pack(side=TOP,fill=X, ipady=10)

#-------------------------Frame 9------------------------------------------------------------
    menu_frame9 = Frame(menu_window, bg="#FFFFFF", height=10)
    menu_frame9.pack(fill=X, ipady=5)

    close_button = tk.Button(menu_frame9, text="Logout", width=10, bg="#4682B4", fg="white", font=("Helvetica", 10), command=fechar_janela_menu)
    close_button.pack(side=RIGHT, pady=5, padx=12)
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Sobre---------------------------------------------------------------
def abrir_janela_sobre():
    janela_sobre = Tk()
    janela_sobre.title("Sobre Este Projeto")
    janela_sobre.iconbitmap("images/icon.ico")
    janela_sobre.geometry("600x300")

    # with open("Documentos/sobre.txt", "r") as file:
    #     texto = file.read()

    # label_tabela = Label(janela_sobre, text=texto, justify="left", font="Courier", wraplength=500)
    # label_tabela.pack()

    doc = docx.Document("Documentos/sobre.docx")
    texto = ""
    for paragraph in doc.paragraphs:
        texto += paragraph.text + "\n"

    label_tabela = Label(janela_sobre, text=texto, justify="left", font="Courier", wraplength=500)
    label_tabela.pack()

    janela_sobre.mainloop()
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Cadastro Novo Usuario-----------------------------------------------
def abrir_janela_novo_usuario():
    # Função para abrir a janela de cadastro
    janela_usuario = tk.Toplevel(root)
    janela_usuario.title("Cadastro Usuário")
    janela_usuario.iconbitmap("images/icon.ico")
    janela_usuario.geometry("400x250")  # tamanho da janela
    janela_usuario.resizable(False, False)


    def fechar_janela_novo_usuario():
        # Função para fechar a janela de cadastro e voltar para a janela principal
        janela_usuario.destroy()
        abrir_janela_menu()  # Exibe novamente a janela Menu

    def cadastrar_usuario():
        if usuario_frame3.entry3.get() == usuario_frame4.entry4.get():
            try:
                usuario = usuario_frame2.entry2.get()
                senha = usuario_frame3.entry3.get()
        
                try:
                    con = pg.connect(
                        database="adlpyumj",
                        user="adlpyumj",
                        password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                        host="drona.db.elephantsql.com",
                        port="5432"
                    )

                    sql = "INSERT INTO tb_usuarios (nome_usuario, senha_usuario) \
                                    VALUES (%s, %s)"
                    cur = con.cursor()
                    cur.execute(sql, (usuario, senha))
                    con.commit()
                    con.close()

                    mbox.showinfo("Cadastro Usuário", "Usuário cadastrado com sucesso!")
                    fechar_janela_novo_usuario()

                except Exception as erro:
                    mbox.showinfo("Erro", str(erro))
            except ValueError:
                mbox.showinfo("Cadastro usuário", str(erro))
        else:
            mbox.showinfo("Cadastro usuário", "As senhas não conferem!\nTente novamente!")
            janela_usuario.destroy()
            abrir_janela_novo_usuario()


#-------------------------Frame 1------------------------------------------------------------
    usuario_frame1 = Frame(janela_usuario, bg="#FFFFFF", height=20)
    usuario_frame1.pack(fill=X)

    usuario_frame1.titulo = Label(usuario_frame1)
    usuario_frame1.titulo["text"] = "Cadastrar Novo Usuário"
    usuario_frame1.titulo["bg"] = "#3B5998"
    usuario_frame1.titulo["fg"] = "#FFFFFF"
    usuario_frame1.titulo["font"] = "Helvetica 16 bold"
    usuario_frame1.titulo.pack(side=TOP,fill=X)

#-------------------------Frame 2------------------------------------------------------------
    usuario_frame2 = Frame(janela_usuario, bg="#FFFFFF", height=20)
    usuario_frame2.pack(fill=X)

    usuario_frame2.label2 = Label(usuario_frame2, text="Nome Usuario:", bg="#FFFFFF", font=("Helvetica", 12))
    usuario_frame2.label2.pack(side=LEFT, pady=10)
    usuario_frame2.entry2 = Entry(usuario_frame2, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    usuario_frame2.entry2.pack(side=LEFT, pady=10)
    usuario_frame2.entry2.focus_set()

#-------------------------Frame 3------------------------------------------------------------
    usuario_frame3 = Frame(janela_usuario, bg="#FFFFFF", height=20)
    usuario_frame3.pack(fill=X)

    usuario_frame3.label3 = Label(usuario_frame3, text="Senha Usuario:", bg="#FFFFFF", font=("Helvetica", 12))
    usuario_frame3.label3.pack(side=LEFT, pady=10)
    usuario_frame3.entry3 = Entry(usuario_frame3, width=22, bg="#DEDEDE", font=("Helvetica", 12), show="*")
    usuario_frame3.entry3.pack(side=LEFT, pady=10)

#-------------------------Frame 4------------------------------------------------------------
    usuario_frame4 = Frame(janela_usuario, bg="#FFFFFF", height=20)
    usuario_frame4.pack(fill=X)

    usuario_frame4.label4 = Label(usuario_frame4, text="Confirmar Senha:", bg="#FFFFFF", font=("Helvetica", 12))
    usuario_frame4.label4.pack(side=LEFT, pady=10)
    usuario_frame4.entry4 = Entry(usuario_frame4, width=22, bg="#DEDEDE", font=("Helvetica", 12), show="*")
    usuario_frame4.entry4.pack(side=LEFT, pady=10)

#-------------------------Frame 5------------------------------------------------------------
    usuario_frame5 = Frame(janela_usuario, bg="#FFFFFF", height=20)
    usuario_frame5.pack(fill=X)

    # Criação dos botões na janela de cadastro
    registration_button = tk.Button(usuario_frame5, text="Cadastrar", width=20, bg="blue", fg="white", command=cadastrar_usuario)
    registration_button.pack(side=RIGHT, padx=12)

    close_button = tk.Button(usuario_frame5, text="Fechar", width=20, bg="blue", fg="white", command=fechar_janela_novo_usuario)
    close_button.pack(side=RIGHT)
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Informativo Novo Usuario-----------------------------------------------
def abrir_janela_informacao_novo_usuario():
    root.withdraw()

    def login():
        janela_informacao.destroy()
        abrir_janela_login()

    def fechar():
        # Função para fechar a janela de cadastro e voltar para a janela principal
        janela_informacao.destroy()
        root.deiconify()  # Exibe novamente a janela principal

    
    # Função para abrir a janela de cadastro
    janela_informacao = tk.Toplevel(root)
    janela_informacao.title("Cadastro Usuário")
    janela_informacao.iconbitmap("images/icon.ico")
    janela_informacao.geometry("600x300")  # tamanho da janela
    janela_informacao.resizable(False, False)


    #-------------------------Frame 1-------------------------------------------------------------------
    frame1 = Frame(janela_informacao, bg="#3B5998", height=280)
    frame1.pack(fill=X)

    janela_informacao.titulo = Label(frame1)
    janela_informacao.titulo["text"] = "Somente um usuário já cadastrado\npode fazer o cadastro de um novo usuário.\n\nFAÇA LOGIN"
    janela_informacao.titulo["bg"] = "#3B5998"
    janela_informacao.titulo["fg"] = "#FFFFFF"
    janela_informacao.titulo["font"] = "Helvetica 16 bold"
    janela_informacao.titulo.pack(side=TOP, ipady=80)
    #---------------------------------------------------------------------------------------------------

    #-------------------------Frame 2-------------------------------------------------------------------
    frame2 = Frame(janela_informacao, bg="#FFFFFF", height=40)
    frame2.pack(fill=X)

    login_button = tk.Button(frame2, text="Login", width=15, bg="blue", fg="white", command=login)
    login_button.pack(side=RIGHT, padx=12)


    sobre_button = tk.Button(frame2, text="Fechar", width=15, bg="blue", fg="white", command=fechar)
    sobre_button.pack(side=RIGHT, padx=12)


#----------------------- Janela Login---------------------------------------------------------------
def abrir_janela_login():
    def fechar_janela_login():
        # Função para fechar a janela de cadastro e voltar para a janela principal
        janela_login.destroy()
        root.deiconify()  # Exibe novamente a janela principal
    
    def verifica_login():
        nome = login_frame2.entry2.get()
        senha = login_frame3.entry3.get()

        try:
            connection = pg.connect(
                database="adlpyumj",
                user="adlpyumj",
                password="m0iiqKBail9mWpcotg16HJtjrViN7TNa",
                host="drona.db.elephantsql.com",
                port="5432"
            )

            cursor = connection.cursor()

            # Consulta no banco de dados para obter a senha correspondente ao nome de usuário
            query = "SELECT senha_usuario FROM tb_usuarios WHERE nome_usuario = %s"
            cursor.execute(query, (nome,))
            result = cursor.fetchone()

            if result:
                stored_password = result[0]

                if senha == stored_password:
                    mbox.showinfo("Sucesso", "Login realizado com sucesso!")
                    janela_login.destroy()
                    abrir_janela_menu()
                    #root.deiconify()
                else:
                    mbox.showinfo("Erro", "Senha incorreta.")
            else:
                mbox.showinfo("Erro", "Usuário não encontrado.")

            connection.commit()
            cursor.close()
            connection.close()
        except (Exception, pg.Error) as error:
            print("Erro ao conectar ao banco de dados:", error)
            mbox.showinfo("Erro", "Ocorreu um erro ao conectar ao banco de dados.")
            
    root.withdraw()

    janela_login = tk.Toplevel(root)
    janela_login.title("Login")
    janela_login.iconbitmap("images/icon.ico")
    janela_login.geometry("350x150")  # tamanho da janela
    janela_login.resizable(False, False)
    
#-------------------------Frame 1------------------------------------------------------------
    login_frame1 = Frame(janela_login, bg="#FFFFFF", height=20)
    login_frame1.pack(fill=tk.X)

    login_frame1.titulo = Label(login_frame1)
    login_frame1.titulo["text"] = "LOGIN"
    login_frame1.titulo["bg"] = "#3B5998"
    login_frame1.titulo["fg"] = "#FFFFFF"
    login_frame1.titulo["font"] = "Helvetica 16 bold"
    login_frame1.titulo.pack(side=tk.TOP,fill=tk.X)

#-------------------------Frame 2------------------------------------------------------------
    login_frame2 = Frame(janela_login, bg="#FFFFFF", height=20)
    login_frame2.pack(fill=tk.X)

    login_frame2.label2 = Label(login_frame2, text="Nome Usuario:", bg="#FFFFFF", font=("Helvetica", 12))
    login_frame2.label2.pack(side=tk.LEFT, pady=10)
    login_frame2.entry2 = Entry(login_frame2, width=22, bg="#DEDEDE", font=("Helvetica", 12))
    login_frame2.entry2.pack(side=tk.LEFT, pady=10)
    login_frame2.entry2.focus_set()

#-------------------------Frame 3------------------------------------------------------------
    login_frame3 = Frame(janela_login, bg="#FFFFFF", height=20)
    login_frame3.pack(fill=tk.X)

    login_frame3.label3 = Label(login_frame3, text="Senha Usuario:", bg="#FFFFFF", font=("Helvetica", 12))
    login_frame3.label3.pack(side=tk.LEFT, pady=10)
    login_frame3.entry3 = Entry(login_frame3, width=22, bg="#DEDEDE", font=("Helvetica", 12), show="*")
    login_frame3.entry3.pack(side=tk.LEFT, pady=10)

#-------------------------Frame 4------------------------------------------------------------
    login_frame4 = Frame(janela_login, bg="#FFFFFF", height=20)
    login_frame4.pack(fill=tk.X)

    login_button = tk.Button(login_frame4, text="Entrar", width=10, bg="blue", fg="white", command=verifica_login)
    login_button.pack(side=tk.RIGHT, padx=12)

    login_close_button = tk.Button(login_frame4, text="Fechar", width=10, bg="blue", fg="white", command=fechar_janela_login)
    login_close_button.pack(side=tk.RIGHT)
#---------------------------------------------------------------------------------------------------

#----------------------- Janela Inicial-------------------------------------------------------------
root = tk.Tk()
root.iconbitmap("images/icon.ico")
root.geometry("600x300")  # tamanho da janela
root.title("Início")  # titulo
root.resizable(False, False)

#-------------------------Frame 1-------------------------------------------------------------------
frame1 = Frame(root, bg="#3B5998", height=300)
frame1.pack(fill=X)

titulo = Label(frame1)
titulo["text"] = "BEM-VINDO AO VAREJÃO DO JOÃO"
titulo["bg"] = "#3B5998"
titulo["fg"] = "#FFFFFF"
titulo["font"] = "Helvetica 16 bold"
titulo.pack(side=TOP, ipady=120)
#---------------------------------------------------------------------------------------------------

#-------------------------Frame 2-------------------------------------------------------------------
frame2 = Frame(root, bg="#FFFFFF", height=50)
frame2.pack(fill=X)

login_button = tk.Button(frame2, text="Login", width=15, bg="blue", fg="white", command=abrir_janela_login)
login_button.pack(side=RIGHT, padx=12)

usuario_button = tk.Button(frame2, text="Novo Usuario", width=15, bg="blue", fg="white", command=abrir_janela_informacao_novo_usuario)
usuario_button.pack(side=RIGHT, padx=12)

sobre_button = tk.Button(frame2, text="Sobre", width=15, bg="blue", fg="white", command=abrir_janela_sobre)
sobre_button.pack(side=RIGHT, padx=12)

root.mainloop()
#--------------------------------------------------------------------------------------------------------