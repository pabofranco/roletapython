from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
import time
import winsound
import random
import pymysql

#####Funções#####
def Jogar():
    jogatemp = cmra.get()
    s = 0
    i = imglst[s]
    imglst.remove(i)
    imglst.append(i)
    s += 1
    mycanvas.delete(img1)
    mycanvas.create_image(40, 40, anchor=CENTER, image=i)
    Roleta(jogatemp)
    root.update_idletasks()

def toca(som):
   winsound.PlaySound('%s.wav' %som, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_NOWAIT)

def Desistir():
    g = nvnom.get()
    vlr = nvscore.get()
    vlr = int(vlr)
    if vlr <= 250:
        toca('mybeep')
        escrevelog("Você não pode desistir.\n")
        ttk.btncrg['state'] = 'disabled'
        ttk.btnjg['state'] = 'normal'
        ttk.btndst['state'] = 'disabled'
    else:
        nvscore.set((vlr-250))
        escrevelog("%s: perdeu 250 pontos." %g)
        ttk.btnjg['state'] = 'disabled'
        ttk.btndst['state'] = 'disabled'
        ttk.btncrg['state'] = 'normal'

def Carregar():
    toca('spin')
    time.sleep(0.3)
    v = 0
    cmra.set(0)
    while v <= 15:
        s = 0
        i = imglst[s]
        imglst.remove(i)
        imglst.append(i)
        s += 1
        mycanvas.create_image(40, 40, anchor=CENTER, image=i)
        root.update_idletasks()
        v += 1
        time.sleep(0.1)
    cmratmp = random.randint(0,5)
    Tmbr[cmratmp] = 1
    random.shuffle(Tmbr)
    random.shuffle(Tmbr)
    random.shuffle(Tmbr)
    escrevelog("Arma carregada.\n")
    ttk.btnjg['state'] = 'normal'
    ttk.btndst['state'] = 'normal'
    ttk.btncrg['state'] = 'disabled'

def Sair():
    root.destroy()

def Sobre():
    messagebox.showinfo("Sobre", " Roleta Russa por:\n Pedro Augusto Franco\n pedro_o_pirata@hotmail.com\n \n Efeitos Sonoros: BlinkFarm")

def ComoJogar():
    messagebox.showinfo("Como Jogar", u" Você Começa com 1.000 pontos\n Pode escolher Jogar ou Desistir\n Se desistir, perde 250 pontos\n O jogo acaba quando você morre")

def Versao():
    messagebox.showinfo("Versão", "Roleta Russa : V1.2")

def defnome():
    g = NM.get()
    if len(g) > 8:
        mytop.destroy()
        messagebox.showerror("Erro", "O nome deve possuir no máximo 8 caracteres!")
        NovoJogo()
    elif g == '':
        mytop.destroy()
        messagebox.showerror("Erro", "Nome de jogador não inserido!")
        NovoJogo()
    else:
        mytmp = NM.get()
        nvnom.set(mytmp)
        mytop.destroy()
        escrevelog("Jogo iniciado.\n \nCarregue a arma")
        cmra.set(0)
        ttk.btncrg['state'] = 'normal'
        toca('load')

def hitesc(event):
    mytop.destroy()

def hitenter(event):
    defnome()

def hitf2(event):
    NovoJogo()

def hitup(event):
    if ttk.btncrg['state'] == 'disabled':
        pass
    else:
        Carregar()

def hitright(event):
    if ttk.btndst['state'] == 'disabled':
        pass
    else:
        Desistir()

def hitleft(event):
    if ttk.btnjg['state'] == 'disabled':
        pass
    else:
        Jogar()

def NovoJogo():
    imprimerank()
    global NM
    NM = StringVar()
    global mytop
    mytop = Toplevel(ttk.principal, width=100, height=100, bg="gray")
    mytop.resizable(0, 0)
    mytoplbl = Label(mytop, bg="gray", text="Insira seu nome:")
    mytoplbl.pack()
    myEntry = Entry(mytop, textvariable=NM, width=8)
    myEntry.pack()
    mytopbtn = Button(mytop, bg="gray", text="OK", width=10, command=defnome).pack(pady=5)
    myEntry.focus_set()
    mytop.bind("<Return>", hitenter)
    mytop.bind("<Escape>", hitesc)

def Mutar():
    pass

def Desmutar():
    pass

def GameOver():
    g = nvnom.get()
    escrevelog("%s: encontrou a bala." %g)
    mycanvas.delete(img1)
    mycanvas.create_image(40, 40, anchor=CENTER, image=myimg1)
    resposta = messagebox.askquestion("Classificação", "Você morreu!\nAcrescentar sua pontuação à tabela?", icon='question')
    if resposta == 'yes':
        w = nvnom.get()
        w = str(w)
        z = nvscore.get()
        z = str(z)
        insererank(w, z)
        reinicio()
    else:
        reinicio()
    mylog['state'] = 'normal'
    mylog.delete(1.0, END)
    mylog['state'] = 'disabled'
    NovoJogo()

def escrevelog(msg):
    numlines = mylog.index('end -1 line').split('.')[0]
    mylog['state'] = 'normal'
    if numlines == 10:
        mylog.delete(1.0, 2.0)
    if mylog.index('end -1c') != '1.0':
        mylog.insert('end', '\n')
    mylog.insert('end', msg)
    mylog.see('end')
    mylog['state'] = 'disabled'

def insererank(nome, score):
    connection = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7111326', password='vJrsH2vDZB', db='sql7111326',
                             charset='utf8mb4')
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO ´Rank´(Nome, Pont) VALUES (%s, %s)"
            cursor.execute(sql,(nome, score))
        connection.commit()
    except:
        messagebox.showerror("Classificação", "Erro ao conectar com o servidor")
    finally:
        connection.close()
    messagebox.showinfo("Classificação", "Pontuação enviada com sucesso!")

def imprimerank():
    myrank['state'] = 'normal'
    myrank.delete(1.0, END)

    connection = pymysql.connect(host='sql7.freesqldatabase.com', user='sql7111326', password='vJrsH2vDZB', db='sql7111326',
                             charset='utf8mb4')
    mylist = []
    myintlist = []
    mystrlist = []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM ´Rank´")
            data = cursor.fetchall()

            c = 0
            while c < (len(data)):
                mytemp = (data[c][0], data[c][1])
                mylist.append(mytemp)
                c += 1

        for i in mylist:
            myintlist.append(int(i[0]))
        myintlist.sort(reverse=True)
        for i in myintlist:
            mystrlist.append(str(i))

        cnt = 0
        p = 0
        q = 0
        while cnt <= 9:
            if q == len(mylist):
                q = 0
            if p > len(mystrlist):
                break
            if mystrlist[p] in mylist[q][0]:
                line = (mylist[q][0] + " \t" + mylist[q][1] + "\n")
                myrank.insert('end', line)
                mylist.remove(mylist[q])
                p += 1
                cnt += 1
            else:
                q += 1
    except:
        messagebox.showerror("Classificação", "Erro ao conectar com o servidor")
    finally:
        connection.close()

    myrank['state'] = 'disabled'
    root.update_idletasks()

def Roleta(numero):
    g = nvnom.get()
    if Tmbr[numero] == 0:
        toca('nobullet')
        time.sleep(0.3)
        escrevelog("%s: câmara vazia." %g)
        numero += 1
        cmra.set(numero)
        if Tmbr[numero] == 1:
            escrevelog("BOT: encontrou a bala.\n%s é o vencedor." %g)
            scoretmp = nvscore.get()
            scoretmp += 1000
            nvscore.set(scoretmp)
            escrevelog("\nCarregue a arma.")
            ttk.btnjg['state'] = 'disabled'
            ttk.btndst['state'] = 'disabled'
            ttk.btncrg['state'] = 'normal'
        else:
            escrevelog("BOT: câmara vazia.\n")
            numero += 1
            cmra.set(numero)
    else:
        toca('bullet')
        cmra.set(0)
        GameOver()

def reinicio():
    nvscore.set(1000)
    nvnom.set('Player 1')
    ttk.btnjg['state'] = 'disabled'
    ttk.btndst['state'] = 'disabled'
    ttk.btncrg['state'] = 'disabled'

#####ROOT#####
root = Tk()
root.title("Roleta Russa")
root.configure(background="gray", width=400, height=500)
root.resizable(0, 0)
root.bind("<F2>", hitf2)

global cmra
global Tmbr
cmra = IntVar()
cmra.set(0)
Tmbr = [0, 0, 0, 0, 0, 0]


#####Cria frame principal#####
ttk.principal = Frame(root, width=500, height=500)
ttk.principal.configure(background="gray")
ttk.principal.grid(column=0, row=0, sticky=(N, S, W, E))
ttk.principal.columnconfigure(0, weight=0)
ttk.principal.rowconfigure(0, weight=0)



#####Cria titulo#####
titulo = PhotoImage(file='titulo.png')
ttk.titulo = Label(ttk.principal, image=titulo, width=400, height=60)
ttk.titulo.configure(background="gray")
ttk.titulo.grid(column=0, row=1, columnspan=3, sticky=(E, W))



#####Cria o MENU / AJUDA#####
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Novo Jogo (F2)", command=NovoJogo)
#filemenu.add_command(label="Resetar Rank", command=limparank)
filemenu.add_separator()
filemenu.add_command(label="Sair", command=Sair)
menubar.add_cascade(label="Menu", menu=filemenu)

ajudamenu = Menu(menubar, tearoff=0)
ajudamenu.add_command(label="Como Jogar", command=ComoJogar)
ajudamenu.add_command(label="Sobre", command=Sobre)
ajudamenu.add_command(label="Versao", command=Versao)
menubar.add_cascade(label="Ajuda", menu=ajudamenu)

root.config(menu=menubar)



#####Cria espaço para o nome do jogador, o display da camara e o display de score#####
nvnom = StringVar()
nvnom.set('Jogador 1')
scorejgd = 1000
nvscore = IntVar()
nvscore.set(scorejgd)

ttk.framejogador = LabelFrame(ttk.principal, width=100, height=30)
ttk.framejogador.configure(background="gray")
ttk.framejogador.grid(column=0, row=2, sticky=W)

ttk.framescore = LabelFrame(ttk.principal, width=100, height=30)
ttk.framescore.configure(background="gray")
ttk.framescore.grid(column=2, row=2, sticky=E)

#ttk.framecmra = LabelFrame(ttk.principal, width=50, height=30)
#ttk.framecmra.configure(background="gray")
#ttk.framecmra.grid(column=1, row=2)



#####Insere nome do jogador, a camara e o score#####
ttk.jgd = Label(ttk.framejogador, bg="gray", textvariable=nvnom, width=20).pack()
ttk.score = Label(ttk.framescore, bg="gray", textvariable=nvscore, width=20).pack()
#ttk.numcmra = Label(ttk.framecmra, bg="gray", textvariable=cmra, width=2, font=("Impact", 20)).pack()



#####Cria LogBox#####
ttk.pnd = PanedWindow(ttk.principal, orient=VERTICAL)
ttk.pnd.configure(background="gray")
ttk.logbox = LabelFrame(ttk.pnd, text="REGISTRO", labelanchor=N, width=150, height=200)
ttk.logbox.configure(background="gray")
mylog = Text(ttk.logbox, state='disabled', wrap='word', bg="gray", fg="blue", border=0, font=("Sim Sun", 11))
mylog.place(in_=ttk.logbox, width=146, height=181)
ttk.pnd.add(ttk.logbox)
ttk.pnd.grid(column=0, row=3, sticky=W)



#####Cria RankBox#####
ttk.Rank = LabelFrame(ttk.principal, text="CLASSIFICAÇÃO", labelanchor=N, width=150, height=200)
ttk.Rank.configure(background="gray")
ttk.Rank.grid(column=2, row=3, sticky=E)
myrank = Text(ttk.Rank, state='disabled', wrap='word', width=18, height=11, bg="gray", fg="#990000", border=0)
myrank.pack()
imprimerank()

"""
#####Cria Modo Mute#####
v = IntVar()
v = 2
muteimg = PhotoImage(file='mute.png', width=20, height=15)
unmuteimg = PhotoImage(file='unmute.png', width=20, height=15)
ttk.btnmute = Radiobutton(ttk.principal, command=Mutar, image=muteimg, bg="gray", activebackground="gray", variable=v, value=1, state='disabled')
ttk.btnmute.grid(column=0, row=5, sticky=W)
ttk.btnunmute = Radiobutton(ttk.principal, command=Desmutar, image=unmuteimg, bg="gray", activebackground="gray", variable=v, value=2, state='disabled')
ttk.btnunmute.grid(column=0, row=5)
"""

#####Cria Botoes JOGAR, DESISTIR e CARREGAR#####
ttk.btnjg = Button(ttk.principal, bg="gray", width=10, text="← JOGAR", command=Jogar, state='disabled')
ttk.btnjg.grid(column=0, row=5, sticky=E)
ttk.btndst = Button(ttk.principal, bg="gray", width=10, text="DESISTIR →", command=Desistir, state='disabled')
ttk.btndst.grid(column=2, row=5, sticky=W)
ttk.btncrg = Button(ttk.principal, bg="gray", width=10, text="CARREGAR ↑", command=Carregar, state='disabled')
ttk.btncrg.grid(column=1, row=4, sticky=(W, E))
root.bind('<Up>', hitup)
root.bind('<Right>', hitright)
root.bind('<Left>', hitleft)


#Insere imagem do tambor
ttk.pndimg = PanedWindow(ttk.principal, orient=VERTICAL)
ttk.pndimg.configure(background="gray")
mycanvas = Canvas(ttk.principal, width=81, height=81, bg="gray", bd=0, highlightthickness=0)

myimg1 = ImageTk.PhotoImage(Image.open('tambor_a.png'))
myimg2 = ImageTk.PhotoImage(Image.open('tambor_b.png'))
myimg3 = ImageTk.PhotoImage(Image.open('tambor_c.png'))
myimg4 = ImageTk.PhotoImage(Image.open('tambor_d.png'))
imglst = [myimg2, myimg3, myimg4, myimg1]

myimg = imglst[3]

img1 = mycanvas.create_image(40, 40, anchor=CENTER, image=myimg)
Seta = PhotoImage(file='seta.png', width=9, height=6)
ttk.seta = Label(ttk.principal, background="gray", image=Seta)
Tambor = PhotoImage(file='tambor_a.png', width=81, height=81)
ttk.tambor = Label(ttk.principal, background="gray", image=Tambor)
ttk.pndimg.add(ttk.seta)
ttk.pndimg.add(mycanvas)
ttk.pndimg.grid(column=1, row=3, sticky=W)


#####Mainloop#####
root.mainloop()