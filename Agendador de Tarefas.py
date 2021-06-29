import tkinter as tk
from tkinter import ttk
import tkcalendar  as cal
from tkinter import messagebox
from tkinter import filedialog as fd
import json
import os
from datetime import date
from tkinter import messagebox as mb

font = "Arial"
tasks = []
newTask = {"titulo": "", "descricao": "", "inicial": None, "final": None}
currFile = None
changed = False
title = "TaskPlanner"

AboutDisplayed = False
HelpDisplayed = False


def get_desc():
    return desc.get("0.1", tk.END + '-1c')


def save(event=None):
    global changed
    if titre.get() == "":
        messagebox.showinfo("Alerta!", "Digite o título da sua tarefa")

    elif dated.get_date() > datef.get_date():
        messagebox.showinfo("Alerta!", "Data de término anterior à data de início!")

    elif get_desc() == "":
        messagebox.showinfo("Alerta!", "Insira a descrição da sua tarefa")
    else:
        sv.set("")
        task = {}
        task["titulo"] = titre.get()
        task["descricao"] = get_desc()
        task["inicial"] = str(dated.get_date())
        task["final"] = str(datef.get_date())
        act = listbox.get(listbox.curselection())
        # print(act)
        if act == "+":
            listbox.delete(len(tasks))
            listbox.insert(tk.END, str(len(tasks) + 1) + "- " + task["titulo"])
            tasks.append(task)
            listbox.insert(tk.END, "+")
            listbox.select_set(len(tasks) - 1)
        else:
            index = int(act.split("-")[0])
            listbox.delete(index - 1)
            listbox.insert(index - 1, str(index) + "- " + task["titulo"])
            tasks[index - 1] = task
            # listbox.insert(tk.END, "+")
            listbox.select_set(index - 1)
        prog.title("Agendador de Tarefa" + " - " + title + " *")
        changed = True
        B2["state"] = "normal"


def saveInFile(event=None):
    global currFile, tasks, title, changed
    if currFile == None:
        filename = fd.asksaveasfilename(initialdir="./DBASE", defaultextension=".json",
                                        filetypes=[("JSON Files", "*.json")])
        if filename == "" or len(filename) == 0: return
        with open(filename, "w") as f:
            json.dump(tasks, f)
            currFile = filename
            prog.title("Agendador de Tarefa" + " - " + os.path.basename(filename))
            title = os.path.basename(filename)
    else:
        with open(currFile, "w") as f:
            json.dump(tasks, f, indent=4)
            prog.title("Agendador de Tarefa" + " - " + title)
    filemenu.entryconfigure(3, state="normal")
    changed = False


def saveAs(event=None):
    global currFile, title, tasks, changed

    filename = fd.asksaveasfilename(initialdir="./DBASE", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename == "" or len(filename) == 0: return
    with open(filename, "w") as f:
        json.dump(tasks, f)
        currFile = filename
        prog.title("Agendador de Tarefa" + " - " + os.path.basename(filename))
        filemenu.entryconfigure(3, state="normal")
    title = os.path.basename(filename)
    changed = False


def openFile(event=None):
    global currFile, tasks, title, changed
    filename = fd.askopenfilename(initialdir="./DBASE", defaultextension=".json", filetypes=[("JSON Files", "*.json")])
    if filename == "" or len(filename) == 0: return
    closeFile()
    with open(filename, "r") as f:
        changed = False
        tasks = json.load(f)
        prog.title("Agendador de Tarefa" + " - " + os.path.basename(filename))
        title = os.path.basename(filename)
        currFile = filename
        listbox.delete(0, tk.END)
        for i, item in enumerate(tasks):
            listbox.insert(tk.END, str(i + 1) + "- " + item["titulo"])
        listbox.insert(tk.END, "+")
        listbox.select_set(0)
        if len(tasks) > 0:
            svt.set(tasks[0]["titulo"])
            desc.delete(1.0, "end")
            desc.insert(1.0, tasks[0]["descricao"])
            dated.set_date(date.fromisoformat(tasks[0]["inicial"]))
            datef.set_date(date.fromisoformat(tasks[0]["final"]))
            filemenu.entryconfigure(3, state="normal")
            B2["state"] = "normal"
        else:
            svt.set("")
            desc.delete(1.0, "end")
            dated.set_date(date.today())
            datef.set_date(date.today())
            filemenu.entryconfigure(3, state="normal")
            B2["state"] = "disabled"


def onselect(event=None):
    global newTask
    if listbox.curselection() == tuple():
        listbox.select_set(tk.ACTIVE)
        return
    curr = listbox.get(listbox.curselection())
    if curr == "+":
        svt.set(newTask["titulo"])
        desc.delete(1.0, "end")
        desc.insert(1.0, newTask["descricao"])
        dated.set_date(date.today())
        datef.set_date(date.today())
        B2["state"] = "disabled"
    else:
        index = int(curr.split("-")[0]) - 1
        B2["state"] = "normal"
        if index < len(tasks):
            svt.set(tasks[index]["titulo"])
            desc.delete(1.0, "end")
            desc.insert(1.0, tasks[index]["descricao"])
            dated.set_date(date.fromisoformat(tasks[index]["inicial"]))
            datef.set_date(date.fromisoformat(tasks[index]["final"]))


def up(event=None):
    c = listbox.curselection()[0]
    if c > 0:
        listbox.selection_clear(0, 'end')
        listbox.select_set(c - 1)
        onselect()


def down(event=None):
    global tasks
    c = listbox.curselection()[0]
    if c < len(tasks):
        listbox.selection_clear(0, 'end')
        listbox.select_set(c + 1)
        onselect()


def closeFile(event=None):
    global currFile, tasks, changed, title

    if changed:
        answer = mb.askyesnocancel(title="Agendador de Tarefa - " + title, message="Deseja salvar as alterações no arquivo?")
        if answer == None:
            changed = False
            return
        if answer:
            with open(currFile, "w") as f:
                json.dump(tasks, f, indent=4)

    filemenu.entryconfigure(3, state="disabled")
    svt.set("")
    tasks = []
    desc.delete(1.0, "end")
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "+")
    currFile = None
    title = "Sem título"
    prog.title("Agendador de Tarefa" + " - " + title)
    listbox.select_set(0)
    dated.set_date(date.today())
    datef.set_date(date.today())
    B2["state"] = "disabled"
    changed = False


def removeTask(event=None):
    global tasks, changed, title

    curr = listbox.get(listbox.curselection())
    if curr == "+":
        return
    changed = True
    prog.title("Agendador de Tarefa" + " - " + title + " *")
    index = int(curr.split("-")[0])
    del tasks[index - 1]
    listbox.delete(0, tk.END)
    for i, item in enumerate(tasks):
        listbox.insert(tk.END, str(i + 1) + "- " + item["titulo"])
    listbox.insert(tk.END, "+")
    listbox.select_set(index - 1)
    if index - 1 >= len(tasks):
        svt.set("")
        desc.delete(1.0, "end")
        dated.set_date(date.today())
        datef.set_date(date.today())
        B2["state"] = "disabled"
    else:
        svt.set(tasks[index - 1]["titulo"])
        desc.delete(1.0, "end")
        desc.insert(1.0, tasks[index - 1]["descricao"])
        dated.set_date(date.fromisoformat(tasks[index - 1]["inicial"]))
        datef.set_date(date.fromisoformat(tasks[index - 1]["final"]))


def about(event=None):
    global FrameAjuda, AboutDisplayed
    if not AboutDisplayed:
        FrameAjuda.grid(row=7, column=0, columnspan=4, sticky="EW")
        AboutDisplayed = True
    else:
        FrameAjuda.grid_forget()
        AboutDisplayed = False


def helpApp(event=None):
    global FrameAjuda, HelpDisplayed
    if not HelpDisplayed:
        FrameAjuda.grid(row=0, column=6, rowspan=6, sticky="NS")
        HelpDisplayed = True
    else:
        FrameAjuda.grid_forget()
        HelpDisplayed = False


def quitApp(event=None):
    global currFile, tasks, changed, title

    if changed:
        answer = mb.askyesnocancel(title="Agendador de Tarefa - " + title, message="Deseja salvar as alterações no arquivo?")
        if answer == None:
            return
        if answer:
            with open(currFile, "w") as f:
                json.dump(tasks, f, indent=4)
    prog.quit()


def printPDF(event=None):
    mb.showinfo(title="Agendador de Tarefa", message="Esta funcionalidade ainda não foi desenvolvida!")


prog = tk.Tk()
prog.title("Agendador de Tarefa" + " - " + title)

# Menu

menubar = tk.Menu(prog)
filemenu = tk.Menu(menubar, tearoff=0)
# filemenu.add_command(label="New", accelerator="Ctrl+N")
filemenu.add_command(label="Abrir", accelerator="Ctrl+O", command=openFile)
filemenu.add_command(label="Salvar", accelerator="Ctrl+S", command=saveInFile)
filemenu.add_command(label="Salvar como...", command=saveAs)
filemenu.add_command(label="Fechar", accelerator="Ctrl+W", command=closeFile, state="disabled")
filemenu.add_command(label="Imprimir", accelerator="Ctrl+P", command=printPDF)
filemenu.add_separator()
filemenu.add_command(label="Sair", accelerator="Ctrl+Q", command=quitApp)
menubar.add_cascade(label="Arquivo", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Ajuda", accelerator="F1", command=helpApp)
helpmenu.add_command(label="Sobre", accelerator="Alt+A", command=about)
menubar.add_cascade(label="Ajuda", menu=helpmenu)

prog.config(menu=menubar)

prog.bind("<Control-s>", saveInFile)
prog.bind("<Control-o>", openFile)
prog.bind("<Alt-v>", save)
prog.bind("<Control-q>", quitApp)
prog.bind("<Control-w>", closeFile)
# prog.bind("<Button-1>", lambda e: print(str(dated.get_date())))
prog.bind("<Alt-Up>", up)
prog.bind("<Alt-Down>", down)
prog.bind("<Alt-a>", about)
prog.bind("<Alt-d>", removeTask)
prog.bind("<Control-p>", printPDF)
prog.bind("<F1>", helpApp)
### Menu configurações

fen = ttk.Frame(prog, padding="10 10 10 10")
fen.pack()

cadre1 = ttk.Frame(fen, padding="5 5 5 5")
cadre1.grid(row=0, column=0, sticky="NWES")

listbox = tk.Listbox(cadre1, height=13, font="Arial", exportselection=0)
listbox.grid(row=0, column=0, sticky="NWES")

listbox.bind('<<ListboxSelect>>', onselect)
listbox.bind('<FocusIn>', lambda e: titre.focus_set())

for i, item in enumerate(tasks):
    listbox.insert(tk.END, str(i + 1) + "- " + item["titulo"])
listbox.insert(tk.END, "+")
listbox.select_set(0)

# Quadro 2
cadre2 = ttk.Frame(fen, padding="5 5 5 5")
cadre2.grid(row=0, column=1)

tk.Label(cadre2, text="Tarefa: ", font="Arial").grid(
    row=0, column=0, columnspan=4, sticky="W")

svt = tk.StringVar()
titre = tk.Entry(cadre2, textvariable=svt, width=50, font="Arial", highlightthickness=1)
titre.grid(row=1, column=0, columnspan=4)

tk.Label(cadre2, text="Data inicio: ", font="Arial").grid(row=2, column=0, sticky="W")
dated = cal.DateEntry(cadre2, date_pattern="dd/mm/Y", font="Arial", locale="en_US", borderwidth=1)
dated.grid(row=2, column=1)

tk.Label(cadre2, text="Data fim: ", font="Arial").grid(row=2, column=2, sticky="W")
datef = cal.DateEntry(cadre2, date_pattern="dd/mm/Y", font="Arial", locale="en_US", borderwidth=1)
datef.grid(row=2, column=3, sticky="E")

tk.Label(cadre2, text="Descrição: ", font="Arial").grid(row=3, column=0, columnspan=4, sticky="W")

desc = tk.Text(cadre2, width=22, height=6, font="Arial", highlightthickness=1)
scrollb = tk.Scrollbar(cadre2, command=desc.yview)
desc['yscrollcommand'] = scrollb.set
scrollb.grid(row=4, column=4, sticky='ns')
desc.grid(row=4, column=0, sticky="EW", columnspan=4)

sv = tk.StringVar()
sv.set("  ")
errLabel = tk.Label(cadre2, textvariable=sv, fg="red")
errLabel.grid(row=5, column=0, sticky="EW", columnspan=4)

B1 = tk.Button(cadre2, text="Salvar", command=lambda: save(), font="Arial")
B1.grid(row=6, column=2, sticky="E", columnspan=2)
B2 = tk.Button(cadre2, text="Excluir", command=lambda: removeTask(), font="Arial", state="disabled")
B2.grid(row=6, column=0, sticky="W", columnspan=2)

## Sobre
FrameSobre = tk.Frame(fen)

built = tk.Label(FrameSobre, text="(2021-06 v.0.1)")
copyRight = tk.Label(FrameSobre, text="Kelsen Lima")
ttk.Separator(FrameSobre, orient=tk.HORIZONTAL).pack()
built.pack()
copyRight.pack()
tk.Button(FrameSobre, text="Ocultar", anchor="w", command=about).pack(side="right")

## Ajuda
FrameAjuda = tk.Frame(fen)
tk.Label(FrameAjuda, text="Atalhos", font='Helvetica 18 bold').pack()

FrameAtalho = tk.Frame(FrameAjuda)

tk.Label(FrameAtalho, text="<Ctrl>-<O>:", font="bold").grid(row=0, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Abra um arquivo").grid(row=0, column=1, sticky="W")

tk.Label(FrameAtalho, text="<Ctrl>-<S>:", font="bold").grid(row=1, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Salve o arquivo atual").grid(row=1, column=1, sticky="W")

tk.Label(FrameAtalho, text="<Ctrl>-<W>:", font="bold").grid(row=2, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Fechar arquivo atual").grid(row=2, column=1, sticky="W")

tk.Label(FrameAtalho, text="<Ctrl>-<Q>:", font="bold").grid(row=3, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Sair").grid(row=3, column=1, sticky="W")

tk.Label(FrameAtalho, text="<Alt>-<Up>:", font="bold").grid(row=4, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Selecione as tarefas anteriores (vá para cima na lista)").grid(row=4, column=1, sticky="W")

tk.Label(FrameAtalho, text="<Alt>-<Down>:", font="bold").grid(row=5, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Selecione as próximas tarefas (vá para baixo na lista)").grid(row=5, column=1, sticky="W")

tk.Label(FrameAtalho, text="<Alt>-<D>:", font="bold").grid(row=6, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Excluir tarefa selecionada").grid(row=6, column=1, sticky="W")

tk.Label(FrameAtalho, text="<Atl>-<A>:", font="bold").grid(row=7, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Alternar quadro `Sobre`").grid(row=7, column=1, sticky="W")

tk.Label(FrameAtalho, text="<Atl>-<V>:", font="bold").grid(row=8, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Validar tarefa atual").grid(row=8, column=1, sticky="W")

tk.Label(FrameAtalho, text="<F1>:", font="bold").grid(row=9, column=0, sticky="E")
tk.Label(FrameAtalho, text=" Alternar quadro `Ajuda` ").grid(row=9, column=1, sticky="W")

FrameAtalho.pack()
prog.resizable(width=False, height=False)
x = (prog.winfo_screenwidth() - prog.winfo_reqwidth()) / 2
y = (prog.winfo_screenheight() - prog.winfo_reqheight()) / 2
prog.geometry("+%d+%d" % (x, y))
prog.mainloop()
