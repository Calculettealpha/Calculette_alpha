from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from math import radians, sqrt, pi, e, fabs, factorial, log, log10, degrees, comb
from math import sin as nsin
from math import cos as ncos
from math import tan as ntan
from math import sinh as nsinh
from math import cosh as ncosh
from math import tanh as ntanh
from math import acos as nacos
from math import asin as nasin
from math import atan as natan
from math import asinh as nasinh
from math import acosh as nacosh
from math import atanh as natanh
import numpy as np
from fractions import Fraction
import sys
from numpy import *
from scipy import integrate
import tkinter.tix, tkinter.colorchooser
import tkinter.font
from sympy import*
from sympy import limit, oo, acos, acosh, acot, acoth, asin, asinh, atan, atanh, cos, cosh, cot, coth, exp, ln, log, pi, sin, tan, tanh, sinh
from sympy.abc import x
import sympy.core.numbers

lp = []
with open('primes.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        lp.append(int(line))
      
# ==============================================================


class Repere(Canvas):
    """Cette class permet de gérer l'affichage d'un repère orthonormal, et d'effectuer le traçage de courbes mathématiques"""

    def __init__(self, root, width=600, height=400, color="#FFFFFF"):
        Canvas.__init__(self, root)  # Construction du widget parent
        # Width et height -> impaire car pixel du "milieu" est un pixel impaire (ex: 401 -> pixel milieu = 201) :
        if width % 2 == 0: width += 1
        if height % 2 == 0: height += 1
        self.configure(width=width, height=height, bg=color)  # Configuration du widget selon les options
        self.width, self.height = width, height  # Enregistrement des valeurs width et height
        self.courbe = []  # Variable contenant les infos propres à chaque courbe (équation, couleur, option , ...)

    def trace_axe(self, xmax=10, xmin=-10, ymax=10, ymin=-10, grad=2):
        """ Méthode permettant de tracer les axes selon des valeurs maximales et minimales en x et y..
        L'option grad est une option d'affichage de graduations sur les axes :
            grad == -1 -> Rien
            grad == 0 -> simplement deux axes sans rien d'autre
            grad == 1 -> deux axes + flèches en début et fin de chaque axe
            grad == 2 -> petites graduations seulement sur les axes, selon valeurs minimum et maximum de ces axes
            grad == 3 -> graduations traversant tout le canvas, selon valeurs minimum et maximum des axes """

        self.delete("axe", "grad")  # On efface les anciens axes (+ graduations) si anciens axes il y a

        # Gestion des erreurs d'attributs :
        if xmax <= 0:
            xmax = 10
            messagebox.showwarning("Attention !!!", "Valeur de \"xmax\" rectifiée à 10 car inférieur ou égal à 0")
        if xmin >= 0:
            xmin = -10
            messagebox.showwarning("Attention !!!", "Valeur de \"xmin\" rectifiée à -10 car supérieur ou égal à 0")
        if ymax <= 0:
            ymax = 10
            messagebox.showwarning("Attention !!!", "Valeur de \"ymax\" rectifiée à 10 car inférieur ou égal à 0")
        if ymin >= 0:
            ymin = -10
            messagebox.showwarning("Attention !!!", "Valeur de \"ymin\" rectifiée à -10 car supérieur ou égal à 0")
        if grad < -1 or grad > 3:
            grad = 2
            messagebox.showwarning("Attention !!!", "Mode de graduation fixé à 2, car la valeur soumise est incorrect")

        npix_x = int(float(self.width) / (-xmin + xmax) * (-xmin))  # Calcul nbr pixel de la partie gauche des abscisses
        npix_y = int(float(self.height) / (-ymin + ymax) * ymax)  # Calcul nbr pixel de la partie haute des ordonnées
        self.val_xy = [[xmax, xmin], [ymax, ymin]]  # Enregistrement des valeurs min et max en x et en y

        # Création des graduations selon l'option choisie :
        if grad == 0: arrow = NONE
        if grad == 1: arrow = BOTH
        if grad == 2:  # Graduation partielle
            arrow = NONE
            # Graduations sur l'axe x -> partie négative puis positive :
            for x in range(npix_x + 1, 0, int(npix_x / xmin)): self.create_line(x, npix_y - 2, x, npix_y + 5,
                                                                                tag="grad")
            for x in range(npix_x + 1, self.width + 1, int(npix_x / (-xmin))): self.create_line(x, npix_y - 2, x,
                                                                                                npix_y + 5, tag="grad")
            # Graduations sur l'axe x -> partie positive puis négative :
            for y in range(npix_y + 1, 0, int(-npix_y / ymax)): self.create_line(npix_x - 2, y, npix_x + 5, y,
                                                                                 tag="grad")
            for y in range(npix_y + 1, self.height + 1, int(npix_y / ymax)): self.create_line(npix_x - 2, y, npix_x + 5,
                                                                                              y, tag="grad")
        if grad == 3:  # Graduation complète
            arrow = NONE
            # Graduations sur l'axe x -> partie négative puis positive :
            for x in range(npix_x + 1, 0, int(-npix_x / (-xmin))): self.create_line(x, 1, x, self.height,
                                                                                    fill="#dbd8d8", tag="grad")
            for x in range(npix_x + 1, self.width + 1, int(npix_x / (-xmin))): self.create_line(x, 1, x, self.height,
                                                                                                fill="#dbd8d8",
                                                                                                tag="grad")
            # Graduations sur l'axe x -> partie positive puis négative :
            for y in range(npix_y + 1, 0, int(-npix_y / ymax)): self.create_line(1, y, self.width, y, fill="#dbd8d8",
                                                                                 tag="grad")
            for y in range(npix_y + 1, self.height + 1, int(npix_y / ymax)): self.create_line(1, y, self.width, y,
                                                                                              fill="#dbd8d8",
                                                                                              tag="grad")

        if grad != -1:
            self.create_line(0, npix_y + 1, self.width, npix_y + 1, arrow=arrow,
                             tag="axe")  # Création de l'axe x (des abscisses)
            self.create_line(npix_x + 1, 0, npix_x + 1, self.height, arrow=arrow,
                             tag="axe")  # Création de l'axe y (des ordonnées)

    def check_value(self, f, x):

        try:
            eval(f)
        except ValueError:
            return (x, None)
        except SyntaxError:
            pass

        else:
            if -30 < eval(f) < 30:
                return (x, eval(f))
            else:
                return (x, None)

    def trace_courbe(self, equa, color="#000000", mod="normal", step=10):
        """ Méthode permettant de tracer une courbe d'équation définie par l'attribut "equa".
        De plus, celle-ci accepte un attribut, mod, qui permet d'afficher la courbe de différentes manières :
        mod == "normal" -> affiche la courbe de façon linéaire
        mod == "point" -> affiche certains points seulement de la courbe
        mod == "both" -> affiche des deux manières précédentes
        step est utilisé uniquement quand mod == "point" ou "both". Cela affiche les points tout les step pixel """

        for i in range(len(self.courbe)):  # Cas s'il y a des doublons :
            if equa == self.courbe[i][0]:  # Si l'équation existe déjà :
                if messagebox.askquestion("Fonction déjà existante",
                                          "Cette fonction existe déjà.\nVoulez-vous écraser la précédente ?") == "no":
                    return None
                else:
                    self.delete("courbe_" + equa, "point_" + equa)  # On efface la courbe (+ les points s'ils existent)
                    del self.courbe[i]  # On enlève la courbe de self.courbe
                    break
        kury = np.arange(-10, 10, 0.01)
        first_board = []
        for x in np.arange(-10, 10, 0.005):
            try:
                self.check_value(equa, x)
            except(SyntaxError, NameError, TypeError):
                messagebox.showerror(str(sys.exc_info()[0]),
                                     "L'équation \"" + equa + "\" semble erronée")  # On affiche un message d'erreur

            first_board.append(self.check_value(equa, x))
        self.val_non_perms = [round(x, 2) for (x, y) in first_board if y is None]
        self.courbe.append([equa, color, mod, step])  # On enregistre les infos de la courbe
        res = []  # Liste contenant les coordonnées de chaque pixel affichable
        tr = []
        for i in range(1, self.width + 1):

            x = self.convert_pix_to_unit("x", i)
            x_round = round(x, 2)

            if x_round not in self.val_non_perms:
                y_pix = self.convert_unit_to_pix("y", eval(equa))

                try:
                    y_pix = self.convert_unit_to_pix("y", eval(equa))
                except ValueError:
                    pass
                except (SyntaxError, NameError, TypeError):
                    messagebox.showerror(str(sys.exc_info()[0]),
                                         "L'équation \"" + equa + "\" semble erronée")  # On affiche un message d'erreur
                    self.courbe.pop()  # On supprime la dernière entrée de la liste self.courbe, car elle est erronée
                    break  # On sort de la boucle for

                if (-(self.height ** 2) < y_pix < (self.height ** 2)):
                    tr.append((i, y_pix))  # On n'enregistre que les résultats servant à l'affichage
                if round(self.convert_pix_to_unit("x", i + 1), 2) in self.val_non_perms:
                    res.append(tr)
                    tr = []
            else:
                pass

        try:
            if (mod == "normal") or (mod == "both"):
                for c in res:
                    self.create_line(c, fill=color, tag="courbe_" + equa)
                self.create_line(tr, fill=color, tag="courbe_" + equa)
            if (mod == "point") or (mod == "both"):
                for i in range(0, len(res) - 1):
                    if not res[i][0] % step:
                        self.create_oval(res[i + 1][0] - 2, res[i + 1][1] - 2, res[i + 1][0] + 2, res[i + 1][1] + 2,
                                         fill=color, tag="point_" + equa)
            return 1  # Retourne 1 si tout s'est bien passé sinon on retourne rien (None)
        except:
            return None

    def convert_pix_to_unit(self, axe, val):
        """ Convertit les pixels (par raport à un des axes) en unités """
        if axe == "x":
            pix = (self.val_xy[0][0] - self.val_xy[0][1]) / float(self.width)
            return self.val_xy[0][1] + pix * val
        elif axe == "y":
            pix = (self.val_xy[1][0] - self.val_xy[1][1]) / float(self.height)
            return self.val_xy[1][0] - pix * val
        else:
            return None

    def convert_unit_to_pix(self, axe, val):
        """ Convertit une unité en pixel (par rapport à un des axes) """
        if axe == "x":
            unit = float(self.width) / (self.val_xy[0][0] - self.val_xy[0][1])
            return unit * (-self.val_xy[0][1]) + unit * val + 1
        elif axe == "y":
            unit = float(self.height) / (self.val_xy[1][0] - self.val_xy[1][1])
            return unit * self.val_xy[1][0] - unit * val + 1
        else:
            return None


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


# ++++++++++++++++++++++++++++++++++++++++++++ Début du programme +++++++++++++++++++++++++++++++++++++++++
def draw_function():
    # On importe le module Tix pour des widgets Tkinter préfabriqués et le module de choix de couleur (ds une boite de dialogue) :

    # ++++++++++++++++++++++++++ Variables globales ########################
    global color
    color = "#999999"  # Couleur de la courbe en cours        ##

    ######################################################################

    # ------------------------------ Partie traçage d'une nouvelle courbes ---------------------------#
    # Fonction lançant le traçage de la courbe :
    def tracer():
        try:
            if (int(pas_en.get()) > 50) and (
                    mod.get() != "normal"):  # Si le pas est trop gros, on demande à l'utilisateur si il veut qd même tracer la courbe
                if messagebox.askquestion("Conseil :",
                                          "Vous avez rentré une valeur de pas très élevée. Il se peut que la courbe ne s'affiche pas.\n Voulez-vous continuez ?") == "no":
                    return None
            if not rep.trace_courbe(equa=equa_en.get(), color=color, mod=mod.get(), step=int(pas_en.get())):
                equa_en.configure(bg="#999999")
            else:  # On réinitialise tout si la courbe a bien été tracé
                inisialis_trace_part()

        except ValueError:
            messagebox.showerror("Attention !!!", "La valeur du pas \"" + pas_en.get() + "\" semble erronée.")

    def inisialis_trace_part():  # Pour initialiser ts les éléments de lbfr_tracer
        global color
        color = "#999999"
        equa_en.configure(bg=color)
        equa_en.delete(0, END)
        pas_en.delete(0, END)
        pas_en.insert(0, "10")
        color_bt.configure(bg=color)
        normal_rbt_mod.select()

    # Fonction permettant le choix de la couleur de la fonction :
    def choix_color():
        global color
        colch = tkinter.colorchooser.askcolor(title="Choisir la couleur de la fonction", master=rep, color="#999999")
        # colch.grab_set()
        color = str(colch[1])
        color_bt.configure(bg=color)

    # ------------------------------------------------------------------------------------------------#

    # -------------------------------- Partie configuration du fenetrage -----------------------------#
    # Fonction lançant le traçage de la courbe :
    def config_window():
        try:
            xmax, xmin = float(lben_xmax.entry.get()), float(lben_xmin.entry.get()),
            ymax, ymin = float(lben_ymax.entry.get()), float(lben_ymin.entry.get())

            rep.delete(ALL)  # On supprime ts les éléments du canvas
            lb_coords.configure(text="x= -- et y= --")
            tmp_courbe = rep.courbe[0:]
            rep.courbe = []  # On supprime ttes les entrées de rep.courbe

            # Gestion des erreurs d'attributs :
            # Ce même bou de code apparaît déjà ds la class Repere, mais c'est normal
            # puisqu'elle est conçue pour être indépendante (pour être réutilisable) du reste du code (donc gestion des erreurs indépendantes)
            if xmax <= 0:
                xmax = 10
                lben_xmax.entry.delete(0, END)
                lben_xmax.entry.insert(0, "10")
                messagebox.showwarning("Attention !!!", "Valeur de \"xmax\" rectifiée à 10 car inférieur ou égal à 0")
            if xmin >= 0:
                xmin = -10
                lben_xmin.entry.delete(0, END)
                lben_xmin.entry.insert(0, "-10")
                messagebox.showwarning("Attention !!!", "Valeur de \"xmin\" rectifiée à -10 car supérieur ou égal à 0")
            if ymax <= 0:
                ymax = 10
                lben_ymax.entry.delete(0, END)
                lben_ymax.entry.insert(0, "10")
                messagebox.showwarning("Attention !!!", "Valeur de \"ymax\" rectifiée à 10 car inférieur ou égal à 0")
            if ymin >= 0:
                ymin = -10
                lben_ymin.entry.delete(0, END)
                lben_ymin.entry.insert(0, "-10")
                messagebox.showwarning("Attention !!!", "Valeur de \"ymin\" rectifiée à -10 car supérieur ou égal à 0")

            rep.trace_axe(xmax=xmax, xmin=xmin, ymax=ymax, ymin=ymin, grad=grad.get())  # On trace les nvo axes
            for crb in tmp_courbe:  # Et on retrace les courbes
                rep.trace_courbe(equa=crb[0], color=crb[1], mod=crb[2], step=crb[3])

        except:
            messagebox.showerror("Erreur !!!",
                                 "Une ou plusieurs données pour le fenètrage, ne sont pas des données numériques.\nVeuillez rectifier.")

    def reinitialisation():
        lben_xmax.entry.delete(0, END)
        lben_xmin.entry.delete(0, END)
        lben_ymax.entry.delete(0, END)
        lben_ymin.entry.delete(0, END)

        lben_xmax.entry.insert(0, "10")
        lben_xmin.entry.insert(0, "-10")
        lben_ymax.entry.insert(0, "10")
        lben_ymin.entry.insert(0, "-10")

        rep.courbe = []
        normal_rbt_grad.select()
        config_window()

    # ------------------------------------------------------------------------------------------------#

    # ---------------------------------------- Autres fonctions --------------------------------------#

    def coords_write(event):
        lb_coords.configure(text="x= %4.2f et y= %4.2f" % (
            rep.convert_pix_to_unit("x", event.x), rep.convert_pix_to_unit("y", event.y)))
        rep.delete("croix")
        rep.create_text(event.x, event.y, text="+", font=font_big, tag="croix")

    def del_croix(event):
        rep.delete("croix")  # Enlève le chtite croix si le bouton drt de la sourie est préssé
        lb_coords.configure(text="x= -- et y= --")

    # ------------------------------------------------------------------------------------------------#

    # Création du widget maître :
    root = tkinter.tix.Tk()
    root.iconbitmap("alpha.ico")
    root.title("Traceur de fonctions mathématiques")
    root.config(bg="#20212E")

    # Création des widgets esclaves #
    # Label ac les coordonnées :
    font_big = tkinter.font.Font(size=15, weight="bold")
    lb_coords = Label(root, text="x= -- et y= --", font=font_big)
    lb_coords.grid(columnspan=3, padx=5, pady=5)
    # Repère -> 600*400, avec grad==2, sur fond blanc :
    rep = Repere(root)
    rep.trace_axe()
    rep.configure(borderwidth=0)
    rep.bind("<Button-1>",
             coords_write)  # Si on presse le bouton gch de la souris sur le canvas, ça nous donne les coords au pts cliqué
    rep.bind("<Button-3>", del_croix)  # Enlève la chtite croix
    rep.grid(row=1, columnspan=3, padx=10, pady=10, sticky="n")
    # LabelFrame_Tracer -> frame contenant les éléments pour tracer une courbe :
    lbfr_tracer = tkinter.tix.LabelFrame(root, label="Tracer une courbe", bg="#20212E")
    lbfr_tracer.frame.configure(width=rep.width / 2, height=100)
    lbfr_tracer.grid(row=2, sticky=NW)
    # Eléments de lbfr_tracer :
    Label(lbfr_tracer, text="Equation :").place(y=23, x=10)
    equa_en = Entry(lbfr_tracer, width=20, bg="#999999", justify="right")
    equa_en.place(y=20, x=70)
    Label(lbfr_tracer, text="Pas :").place(y=90, x=10)
    pas_en = Entry(lbfr_tracer, width=5, bg="#999999", justify="right")
    pas_en.insert(0, "10")
    pas_en.place(y=88, x=40)
    color_bt = Button(lbfr_tracer, text="Couleur équation", relief=SOLID, border=1, command=choix_color)
    color_bt.place(x=130, y=88)
    Button(lbfr_tracer, text="Tracer", command=tracer, bg="#0A98C3").place(x=248, y=88)
    # Les RadioButton & co
    mod = StringVar()  # Variable Tkinter contenant la valeur de la case cochée
    mod.set("normal")
    Label(lbfr_tracer, text="Mod -->").place(x=10, y=53)
    normal_rbt_mod = Radiobutton(lbfr_tracer, text="Normal", value="normal", variable=mod)
    normal_rbt_mod.place(x=50, y=50)
    Radiobutton(lbfr_tracer, text="Point", value="point", variable=mod).place(x=115, y=50)
    Radiobutton(lbfr_tracer, text="Both", value="both", variable=mod).place(x=172, y=50)
    # LabelFrame_Repere_Option -> frame contenant les éléments pour configurer le repère
    lbfr_rep = tkinter.tix.LabelFrame(root, label="Configuration du repère", bg="#20212E")
    lbfr_rep.frame.configure(width=rep.width, height=100)
    lbfr_rep.grid(row=2, column=1, columnspan=2, sticky=NW)
    # Eléments de lbfr_rep :
    Label(lbfr_rep, text="Fenètrage :").place(x=10, y=20)
    lben_xmin = tkinter.tix.LabelEntry(lbfr_rep, label="xmin ->  ")
    lben_xmin.entry.insert(0, "-10")
    lben_xmin.entry.configure(width=5, justify="right")
    lben_xmin.place(x=30, y=35)
    lben_xmax = tkinter.tix.LabelEntry(lbfr_rep, label="xmax -> ")
    lben_xmax.entry.insert(0, "10")
    lben_xmax.entry.configure(width=5, justify="right")
    lben_xmax.place(x=30, y=55)
    lben_ymin = tkinter.tix.LabelEntry(lbfr_rep, label="ymin ->  ")
    lben_ymin.entry.insert(0, "-10")
    lben_ymin.entry.configure(width=5, justify="right")
    lben_ymin.place(x=31, y=75)
    lben_ymax = tkinter.tix.LabelEntry(lbfr_rep, label="ymax -> ")
    lben_ymax.entry.insert(0, "10")
    lben_ymax.entry.configure(width=5, justify="right")
    lben_ymax.place(x=31, y=95)
    Button(lbfr_rep, text="Mettre à jour", command=config_window, bg="#FA0524").place(x=430, y=88)
    Button(lbfr_rep, text="Réinitialiser", command=reinitialisation, bg="#10DB26").place(x=525, y=88)
    # Les RadioButtons & co
    grad = IntVar()
    grad.set(2)
    Label(lbfr_rep, text="Type de graduation -> ").place(x=190, y=20)
    Radiobutton(lbfr_rep, text="Sans axes        ", value=-1, variable=grad).place(x=300, y=20)
    Radiobutton(lbfr_rep, text="Axes simples    ", value=0, variable=grad).place(x=300, y=45)
    Radiobutton(lbfr_rep, text="Axes + flèches ", value=1, variable=grad).place(x=300, y=70)
    normal_rbt_grad = Radiobutton(lbfr_rep, text="Axes + graduations simples    ", value=2, variable=grad)
    normal_rbt_grad.place(x=400, y=20)
    Radiobutton(lbfr_rep, text="Axes + graduations complètes", value=3, variable=grad).place(x=400, y=45)
    # Différents Buttons en bas à droite pour quitter+aide+apropos
    fr_but_br = Frame(root, bg="#20212E")
    fr_but_br.grid(row=3, column=2, sticky=NE)
    # Button(fr_but_br, text="À propos", command=apropos, bg="#EDCF1B").pack(side=LEFT, padx=5, pady=5)
    Button(fr_but_br, text="Quitter", command=root.destroy, bg="#FA0524").pack(side=LEFT, padx=5, pady=5)
    root.mainloop()


# ===========================================Fonctions générales=======================
def destroy_element(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def int_or_float(nbre):
    if int(nbre) == nbre:
        return int(nbre)
    else:
        return nbre

# ======================  Simulation de chargement  ======================================


racinezero = Tk()
racinezero.title("Calculette Alpha")
racinezero.geometry("500x400+470+60")
racinezero.iconbitmap("alpha.ico")
racinezero.resizable(width=False, height=False)
racinezero.config(background="#0C283D")

canv1 = Canvas(racinezero, bg='black', width=350, height=350)
canv1.grid(padx=70, pady=20)
canv1.create_rectangle(4, 4, 350, 350, fill="black", outline="red", width=2)

canv2 = Canvas(canv1, width=250, height=250, bg='black')
canv2.place(x=50, y=50)
textz = Frame(canv2, width=244, height=244, bg='#0C283D')
textz.place(x=6, y=6)
canv2.create_rectangle(4, 4, 250, 250, fill="#0C283D", outline="red", width=2)

niv = 0
sx = 0
xw = ['175+niv', '352', '352-niv', '0', 'niv']
yw = ['0', 'niv', '352', '352-niv', '0']
lmt = [180, 350, 350, 350, 180]
cnt = 0
img1 = PhotoImage(master=racinezero, file="alpha.png")


def progress_sys():
    global niv, sx, cnt
    if sx <= 4:
        cnt += 1
        canv1.create_line(175, 175, eval(xw[sx]), eval(yw[sx]), fill="deep sky blue", width=15)
        if niv == lmt[sx]:
            niv = -10
        niv += 10
        if niv == 0:
            sx += 1

        # Actualisation de la zone de texte
        destroy_element(textz)
        txto = str(int(cnt / 1.46)) + '%'
        Label(textz, text=txto, font=('Vivaldi', 42, 'bold'), bg='#0C283D', fg='deep sky blue').place(x=70, y=15)
        Label(textz, image=img1, text='CALCULETTE\nALPHA', compound=TOP,  font=('Freestyle Script', 28, 'bold'),
              bg='#0C283D', fg='deep sky blue').place(x=30, y=90)
        # Label(textz, text='CALCULETTE', font=('Gabriola', 32, 'bold'), bg='gray22', fg='white').place(x=10, y=100)
        # Label(textz, text='ALPHA', font=('Freestyle Script', 28, 'bold'), bg='gray22', fg='orange').place(x=65, y=155)

        canv1.after(25, progress_sys)

    else:
        racinezero.destroy()


progress_sys()
racinezero.mainloop()

# ============================  Code principal  ==================================
racine = Tk()
racine.title("Calculette Alpha")
racine.geometry("1020x710+170+60")
racine.iconbitmap("alpha.ico")
racine.resizable(width=False, height=False)
racine.config(background="#0C283D")

style = ttk.Style(racine)
style.configure("lefttab.TNotebook", tabposition="wn")

notebook = ttk.Notebook(racine, style="lefttab.TNotebook")
f1 = Frame(notebook, bg="#0C283D", width=970, height=710)
f2 = Frame(notebook, bg="#0C283D", width=970, height=710)
f3 = Frame(notebook, bg="#0C283D", width=970, height=710)
f4 = Frame(notebook, bg="#0C283D", width=970, height=710)
f5 = Frame(notebook, bg="#0C283D", width=970, height=710)
f6 = Frame(notebook, bg="#0C283D", width=970, height=710)
f7 = Frame(notebook, bg="#0C283D", width=970, height=710)

notebook.add(f1, text="     Calculatrices          ")
notebook.add(f2, text="      Matrices             ")
notebook.add(f3, text="        Facteurs premiers      ")
notebook.add(f4, text="Système de numérotation")
notebook.add(f5, text="     Fonctions            ")
notebook.add(f6, text="          Vecteurs             ")
notebook.add(f7, text="         \u24D8 A PROPOS          ")

# =========================================================Onglet_Calculatrices_ou_f1=========================================================================


class Calculus(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.onglets_calc = ttk.Notebook(root)

        self.f1_o1 = Frame(self.onglets_calc, bg="#0C283D", width=900, height=685)
        self.f1_o2 = Frame(self.onglets_calc, bg="#0C283D", width=900, height=685)

        self.onglets_calc.add(self.f1_o1, text="   STANDARD  ")
        self.onglets_calc.add(self.f1_o2, text="   SCIENTIFIQUE  ")

        self.aff1_o1 = Entry(self.f1_o1, width=35, font=("Times New Roman", 22), bd=10, bg="white", fg="black")
        self.aff1_o1.place(x=60, y=10)
        self.aff2_o1 = Entry(self.f1_o1, width=35, font=("Baskerville Old Face", 22), justify=RIGHT, bd=10, bg="white",
                             fg="black")
        self.aff2_o1.place(x=60, y=66)
        self.aff1_o1.insert(0, '0')

        self.dic_ans = {'Ans1': 'broh'}

        btns1 = [' ( ', ' ) ', ' x² ', ' 10^ ', ' √ ',
                 ' 7 ', ' 8 ', ' 9 ', ' C ', ' ⌫ ',
                 ' 4 ', ' 5 ', ' 6 ', ' x ', ' ÷ ',
                 ' 1 ', ' 2 ', ' 3 ', ' + ', ' - ',
                 ' (-) ', ' 0 ', ' . ', ' = ', ' Ans ']

        acts1 = ['(', ')', '²', '10^(', '√(',
                 '7', '8', '9', '', '',
                 '4', '5', '6', '*', '/',
                 '1', '2', '3', '+', '-',
                 '-', '0', '.', '', 'Ans']

        ifc = 0
        yd = 200
        xd = 120
        for w in range(len(btns1)):
            if btns1[w] == ' C ':
                Button(self.f1_o1, text=btns1[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='red',
                       command=lambda: self.del_all(self.aff1_o1, self.aff2_o1)).place(x=xd, y=yd)
            elif btns1[w] == ' \u232B ':
                Button(self.f1_o1, text=btns1[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='red',
                       command=lambda: self.clear(self.aff1_o1, self.aff2_o1)).place(x=xd, y=yd)
            elif btns1[w] == ' = ':
                Button(self.f1_o1, text=btns1[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='green',
                       command=self.calcul1).place(x=xd, y=yd)
            elif btns1[w] in [' 7 ', ' 8 ', ' 9 ', ' 4 ', ' 5 ', ' 6 ', ' 1 ', ' 2 ', ' 3 ', ' 0 ']:
                Button(self.f1_o1, text=btns1[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='#857384',
                       command=lambda w=w: self.insertment(acts1[w], self.aff1_o1, self.aff2_o1, self.dic_ans['Ans1'])).place(x=xd,
                                                                                                                   y=yd)
            else:
                Button(self.f1_o1, text=btns1[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='#5D7B85',
                       command=lambda w=w: self.insertment(acts1[w], self.aff1_o1, self.aff2_o1, self.dic_ans['Ans1'])).place(x=xd,
                                                                                                                   y=yd)

            xd += 75
            ifc += 1
            if ifc % 5 == 0:
                xd = 120
                yd += 70

        self.aff1_o2 = Entry(self.f1_o2, width=46, font=("Times New Roman", 22), bd=10, bg="white", fg="black")
        self.aff1_o2.place(x=30, y=10)
        self.aff2_o2 = Entry(self.f1_o2, width=46, font=("Baskerville Old Face", 22), justify=RIGHT, bd=10, bg="white",
                             fg="black")
        self.aff2_o2.place(x=30, y=66)
        self.aff1_o2.insert(0, '0')

        self.dic_ans["Ans2"] = 'bruh'

        btns2 = [' sin ', ' cos ', ' tan ', ' cotan ', ' sinh ', ' cosh ', ' tanh ', ' cotanh ',
                 ' arcsin ', ' arccos ', ' arctan ', ' arccot ', ' argsh ', ' argch ', ' argth ', ' C(n, k) ',
                 ' 7 ', ' 8 ', ' 9 ', ' C ', ' ⌫ ', ' abs ', ' e ', ' π ',
                 ' 4 ', ' 5 ', ' 6 ', ' x ', ' ÷ ', ' x² ', ' xʸ ', ' 10^ ',
                 ' 1 ', ' 2 ', ' 3 ', ' + ', ' - ', ' (n)! ', ' ( ', ' ) ',
                 ' (-) ', ' 0 ', ' . ', ' = ', ' Ans ', ' √ ', ' ln ', ' log₁₀ ']

        acts2 = ['sin(', 'cos(', 'tan(', 'cotan(', 'sinh(', 'cosh(', 'tanh(', 'cotanh(', 'asin(', 'acos(', 'atan(',
                 'arccot(', 'asinh(', 'acosh(', 'atanh(', 'comb(', '7', '8', '9', '', '', 'abs(', 'e', 'π', '4', '5',
                 '6', '*',
                 '/',
                 '²', '^(', '10^(', '1', '2', '3', '+', '-', 'fact(', '(', ')', '-', '0', '.', '', 'Ans', '√(', 'ln(',
                 'log₁₀(']

        ifc = 0
        yd = 210
        xd = 55
        for w in range(len(btns2)):
            if btns2[w] == ' C ':
                Button(self.f1_o2, text=btns2[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='red',
                       command=lambda: self.del_all(self.aff1_o2, self.aff2_o2)).place(x=xd, y=yd)
            elif btns2[w] == ' \u232B ':
                Button(self.f1_o2, text=btns2[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='red',
                       command=lambda: self.clear(self.aff1_o2, self.aff2_o2)).place(x=xd, y=yd)
            elif btns2[w] == ' = ':
                Button(self.f1_o2, text=btns2[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='green',
                       command=self.calcul2).place(x=xd, y=yd)
            elif btns2[w] in [' 7 ', ' 8 ', ' 9 ', ' 4 ', ' 5 ', ' 6 ', ' 1 ', ' 2 ', ' 3 ', ' 0 ']:
                Button(self.f1_o2, text=btns2[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='#857384',
                       command=lambda w=w: self.insertment(acts2[w], self.aff1_o2, self.aff2_o2, self.dic_ans["Ans2"])).place(x=xd,
                                                                                                                   y=yd)
            else:
                Button(self.f1_o2, text=btns2[w], width=5, height=2, font=("Baskerville Old Face", 16), fg='white',
                       bg='#5D7B85',
                       command=lambda w=w: self.insertment(acts2[w], self.aff1_o2, self.aff2_o2, self.dic_ans["Ans2"])).place(x=xd,
                                                                                                                   y=yd)

            xd += 75
            ifc += 1
            if ifc % 8 == 0:
                xd = 55
                yd += 70
        self.deg_rad = Button(self.f1_o2, text='DEG', font=("Baskerville Old Face", 14), relief=FLAT,
                              command=self.conv_degrad)
        self.deg_rad.place(x=70, y=140)

        self.onglets_calc.grid(row=0, column=0)

    def del_all(self, aff1, aff2):
        aff1.delete(0, END)
        aff2.delete(0, END)

    def clear(self, aff1, aff2):
        if len(aff2.get()) != 0:
            aff2.delete(0, END)
        pos = len(aff1.get())
        aff1.delete(pos - 1)

    def calcul1(self):
        nb = self.aff1_o1.get()
        posi = len(self.aff1_o1.get())
        # print(f'old{nb=}')
        pil = {'²': '**(2)', '^': '**', '√': 'sqrt', 'abs': 'fabs', 'Ans': 'self.dic_ans["Ans1"]'}
        for v in pil:
            if v in nb:
                nb = nb.replace(v, pil[v])
        # print(f'new{nb=}')

        try:
            rep = eval(nb)
            check = True
        except:
            messagebox.showerror("Erreur", "Revérifiez les valeurs entrées !")
            check = False

        if check:
            if posi != 0: self.aff1_o1.insert(posi, '=')
            self.aff2_o1.delete(0, END)
            rep1 = int_or_float(round(rep, 10))
            if len(str(rep1)) > 8:
                self.aff2_o1.insert(0, str(np.format_float_scientific(rep1)))
            else:
                self.aff2_o1.insert(0, str(rep1))

            self.dic_ans['Ans1'] = int_or_float(float(self.aff2_o1.get()))
            # print(Ans1)

    def calcul2(self):
        def acos(nb):
            if self.deg_rad['text'] == 'DEG':
                return degrees(nacos(nb))
            else:
                return nacos(nb)

        def acosh(nb):
            if self.deg_rad['text'] == 'DEG':
                return degrees(nacosh(nb))
            else:
                return nacosh(nb)

        def asin(nb):
            if self.deg_rad['text'] == 'DEG':
                return degrees(nasin(nb))
            else:
                return nasin(nb)

        def asinh(nb):
            if self.deg_rad['text'] == 'DEG':
                return degrees(nasinh(nb))
            else:
                return nasinh(nb)

        def atan(nb):
            if self.deg_rad['text'] == 'DEG':
                return degrees(natan(nb))
            else:
                return natan(nb)

        def atanh(nb):
            if self.deg_rad['text'] == 'DEG':
                return degrees(natanh(degrees(nb)))
            else:
                return natanh(nb)

        def cotanh(nb):
            if self.deg_rad['text'] == 'DEG':
                return 1 / tanh(radians(nb))
            else:
                return 1 / tanh(nb)

        def arccot(nb):
            if self.deg_rad['text'] == 'DEG':
                return degrees(atan(degrees(pi / 2) - nb))
            else:
                return atan((pi / 2) - nb)

        def cotan(nb):
            if self.deg_rad['text'] == 'DEG':
                return 1 / ntan(radians(nb))
            else:
                return 1 / ntan(nb)

        def sin(nb):
            if self.deg_rad['text'] == 'DEG':
                return nsin(radians(nb))
            else:
                return nsin(nb)

        def cos(nb):
            if self.deg_rad['text'] == 'DEG':
                return ncos(radians(nb))
            else:
                return ncos(nb)

        def tan(nb):
            if self.deg_rad['text'] == 'DEG':
                return ntan(radians(nb))
            else:
                return ntan(nb)

        def sinh(nb):
            if self.deg_rad['text'] == 'DEG':
                return nsinh(radians(nb))
            else:
                return nsinh(nb)

        def cosh(nb):
            if self.deg_rad['text'] == 'DEG':
                return ncosh(radians(nb))
            else:
                return ncosh(nb)

        def tanh(nb):
            if self.deg_rad['text'] == 'DEG':
                return ntanh(radians(nb))
            else:
                return ntanh(nb)

        nb = self.aff1_o2.get()
        posi = len(self.aff1_o2.get())
        # print(f'old{nb=}')
        pil = {'²': '**(2)', '^': '**', 'fact': 'factorial', '√': 'sqrt', 'ln': 'log', 'log₁₀': 'log10', 'abs': 'fabs',
               'π': 'pi', 'Ans': "self.dic_ans['Ans2']"}
        for v in pil:  # remplacement des crcts spéciaux par leur équivalents dans 'math' pour le calcul
            if v in nb:
                nb = nb.replace(v, pil[v])
        # print(f'new{nb=}')

        try:
            rep = eval(nb)
            check = True
        except:
            messagebox.showerror("Erreur", "Revérifiez les valeurs entrées !")
            check = False

        if check:
            if posi != 0: self.aff1_o2.insert(posi, '=')
            self.aff2_o2.delete(0, END)
            rep1 = int_or_float(round(rep, 10))
            if len(str(rep1)) > 8:
                self.aff2_o2.insert(0, str(np.format_float_scientific(rep1)))
            else:
                self.aff2_o2.insert(0, str(rep1))

            self.dic_ans["Ans2"] = int_or_float(float(self.aff2_o2.get()))
            # print(Ans2)

    def insertment(self, ch, aff1, aff2, Ans):
        if len(aff2.get()) != 0:
            aff2.delete(0, END)
            aff1.delete(0, END)
            if ch in ['+', '-', '*', '/', '²']:
                aff1.insert(0, 'Ans')

        if aff1.get() == '0' and ch != 'Ans':
            aff1.delete(0, END)

        if (ch != 'Ans') or (ch == 'Ans' and not f'{Ans}'.isalpha()):
            pos = len(aff1.get())
            aff1.insert(pos, ch)

    def conv_degrad(self):
        if self.deg_rad['text'] == 'DEG':
            self.deg_rad.config(text='RAD')
        else:
            self.deg_rad.config(text='DEG')


app_calculus = Calculus(f1)
app_calculus.grid()


# =========================================================Onglet_Matrices_ou_f2=========================================================================

class Matrix(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(width=970, height=710)
        self.config(bg="#0C283D")

        self.onglets_matrice = ttk.Notebook(root, width=970, height=710)

        self.f2_o1 = Frame(self.onglets_matrice, bg="#0C283D", width=900, height=685)
        self.f2_o2 = Frame(self.onglets_matrice, bg="#0C283D", width=900, height=685)

        self.onglets_matrice.add(self.f2_o1, text="   TRANSFORMATIONS  ")
        self.onglets_matrice.add(self.f2_o2, text="   CALCUL MATRICIEL  ")

        Button(self.f2_o2, text="   Dimensions   ", font=("Times New Roman", 16), command=self.entrer_dim1).place(x=270,
                                                                                                                  y=10)
        liste_ope1 = ["+", "-", "*"]
        self.operations = ttk.Combobox(self.f2_o2, width=2, values=liste_ope1, font=("Mongolian Baiti", 20))
        self.operations.current(0)

        self.frame_mat1 = Frame(self.f2_o2, width=385, height=300, bg="#0C283D")  # relief=SUNKEN, bd=2,
        self.frame_mat1.place(x=0, y=70)

        self.frame_mat2 = Frame(self.f2_o2, width=400, height=300, bg="#0C283D")  # relief=SUNKEN, bd=2
        self.frame_mat2.place(x=470, y=70)

        self.frame_mat3 = Frame(self.f2_o2, width=390, height=300, bg="#0C283D")  # relief=SUNKEN, bd=2
        self.frame_mat3.place(x=0, y=375)

        self.reinit_btn = Button(self.f2_o2, text="Réinitialiser", font=("Times New Roman", 16), bg="#335733",
                                 command=None)

        self.onglets_matrice.grid(row=0, column=0)

        Button(self.f2_o1, text="   Dimensions   ", font=("Times New Roman", 16), command=self.entrer_dim2).place(x=170,
                                                                                                                  y=10)
        Label(self.f2_o1, text="Opération: ", font=("Times New Roman", 22), bg="#0C283D", fg="#3834A6").place(x=360,
                                                                                                              y=10)
        self.frame1_o1 = Frame(self.f2_o1, width=350, height=400, bg="#0C283D")  # , relief=SUNKEN, bd=2
        self.frame1_o1.place(x=0, y=170)

        self.frame2_o1 = Frame(self.f2_o1, width=450, height=400, bg="#0C283D")  # , relief=SUNKEN, bd=2
        self.frame2_o1.place(x=440, y=170)

        liste_ope2 = ["Inversion", "Déterminant", "Comatrice"]
        self.operations1 = ttk.Combobox(self.f2_o1, width=12, values=liste_ope2, font=("Mongolian Baiti", 16))
        self.operations1.current(0)
        self.operations1.place(x=490, y=16)
        self.valeurs_copie = []
        self.dic_nc = {}

    def destroy_element(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def copy_mat(self, frame, nc, co_entryx=None):
        self.valeurs_copie.clear()
        mu = []
        for widget in frame.winfo_children():
            if widget.winfo_class() == "Entry":
                if co_entryx and widget.winfo_x() == 7:
                    continue
                mu.append(widget.get())
                if len(mu) == nc:
                    self.valeurs_copie.append([x for x in mu])
                    mu.clear()

    def paste_mat(self, frame, ydep, xdep, co_entryx=None):
        if len(self.valeurs_copie) != 0:
            for widget in frame.winfo_children():
                if widget.winfo_class() == "Entry":
                    if co_entryx and widget.winfo_x() in [5, 7]:
                        continue
                    widget.destroy()

            pcv = [self.frame_mat1, self.frame_mat2, self.frame1_o1]
            ncs = ['nc1', 'nc2', 'nc']
            for j in range(3):
                if frame == pcv[j]:
                    self.dic_nc[ncs[j]] = len(self.valeurs_copie[0])

            ydepart = ydep
            for x in range(len(self.valeurs_copie)):
                xdepart = xdep
                for u in range(len(self.valeurs_copie[0])):
                    abc = Entry(frame, width=4, font=("Times New Roman", 12))
                    abc.insert(0, self.valeurs_copie[x][u])
                    abc.place(x=xdepart, y=ydepart)
                    xdepart += 40
                ydepart += 30

    def fraction_element(self, tab):
        vij = []
        for y in tab:
            poi = []
            for w in y:
                poi.append(str(Fraction(w).limit_denominator()))
            vij.append([g for g in poi])
            poi.clear()
        return vij

    def entrer_dim2(self):

        def get_dim():

            def affiche_solution(matrice_s, texte_s):
                self.destroy_element(self.frame2_o1)
                Label(self.frame2_o1, text=texte_s, font=("Times New Roman", 26), bg="#0C283D", fg="sky blue").place(
                    x=0, y=20)
                Button(self.frame2_o1, text="copier", font=("Fixedsys", 12), bg="#33AB0F",
                       command=lambda: self.copy_mat(self.frame2_o1, len(matrice_s[0]))).place(x=260, y=30)
                ydepart = 70
                for x in range(len(matrice_s)):
                    xdepart = 0
                    for u in range(len(matrice_s[0])):
                        abc = Entry(self.frame2_o1, width=5, font=("Times New Roman", 12,))
                        abc.insert(0, matrice_s[x][u])
                        abc.place(x=xdepart, y=ydepart)
                        xdepart += 49
                    ydepart += 30

            def transform():
                valeurs_m = []
                mu = []
                check = True
                for widget in self.frame1_o1.winfo_children():
                    if widget.winfo_class() == "Entry":
                        try:
                            mu.append(float(eval(widget.get())))
                        except:
                            messagebox.showerror("ERREUR",
                                                 "UNE ERREUR S'EST PRODUITE !\nREVERIFIEZ LES VALEURS ENTREES")
                            check = False
                            break
                        if check:
                            if len(mu) == self.dic_nc['nc']:
                                valeurs_m.append([x for x in mu])
                                mu.clear()
                if check:
                    M = np.array(valeurs_m)
                    M_det = str(Fraction(np.linalg.det(M)).limit_denominator())
                    if self.operations1.get().capitalize() == "Inversion":
                        if M_det != "0":
                            M_inv = np.linalg.inv(M)
                            # print(M_inv)
                            pufu = self.fraction_element(M_inv)
                            affiche_solution(pufu, "Matrice Inverse")

                        else:
                            self.destroy_element(self.frame2_o1)
                            messagebox.showwarning("ERREUR",
                                                   "CETTE MATRICE N'EST PAS INVERSIBLE !\nCAUSE: DETERMINANT NUL")

                    elif self.operations1.get().capitalize() == "Comatrice":
                        try:
                            def matrice_min(matri, line_i, column_j):
                                matri.pop(line_i)
                                for elm in matri:
                                    elm.pop(column_j)
                                return matri

                            comat = []
                            for i in range(self.dic_nc['nc']):
                                butok = []
                                for j in range(self.dic_nc['nc']):
                                    matri = eval(str(valeurs_m))
                                    butok.append(pow(-1, i + j) * linalg.det(array(matrice_min(matri, i, j))))
                                comat.append(butok)
                            M_com = self.fraction_element(comat)
                            affiche_solution(M_com, "Comatrice")

                        except:
                            messagebox.showerror("ERREUR",
                                                 "UNE ERREUR S'EST PRODUITE !\nREVERIFIEZ LES VALEURS ENTREES")

                    elif self.operations1.get().capitalize() == "Déterminant":
                        try:
                            M_det = str(Fraction(np.linalg.det(M)).limit_denominator())
                        except:
                            messagebox.showerror("ERREUR",
                                                 "UNE ERREUR S'EST PRODUITE !\nREVERIFIEZ LES VALEURS ENTREES")
                        # M_det = np.linalg.det(M)
                        self.destroy_element(self.frame2_o1)  # Réinitialisation de la zone d'affichage de la solution
                        Label(self.frame2_o1, text=f"Det(M) = {M_det}", font=("Felixtitling", 26), bg="#0C283D",
                              fg="sky blue").place(x=60, y=80)

            nl = int(entr_l.get())
            nc = nl
            self.destroy_element(self.frame1_o1)
            self.destroy_element(self.frame2_o1)
            self.dic_nc['nc'] = nc
            Label(self.frame1_o1, text="Matrice", font=("Times New Roman", 26), bg="#0C283D", fg="#B4B852").place(x=10,
                                                                                                                  y=0)
            Button(self.frame1_o1, text="copier", font=("Fixedsys", 12), bg="#33AB0F",
                   command=lambda: self.copy_mat(self.frame1_o1, self.dic_nc['nc'])).place(x=140, y=15)
            Button(self.frame1_o1, text="coller", font=("Fixedsys", 12), bg="#33AB0F",
                   command=lambda: self.paste_mat(self.frame1_o1, 50, 10)).place(x=205, y=15)
            Button(self.f2_o1, text="Valider", font=("Times New Roman", 18), bg="green", command=transform).place(x=290,
                                                                                                                  y=70)
            ydepart = 50
            for x in range(nl):
                xdepart = 10
                for u in range(nc):
                    abc = Entry(self.frame1_o1, width=4, font=("Times New Roman", 12))
                    abc.insert(0, "0")
                    abc.place(x=xdepart, y=ydepart)
                    xdepart += 40
                ydepart += 30
            top2.destroy()

        top2 = Toplevel()
        top2.title("Dimension de la matrice")
        top2.iconbitmap("alpha.ico")
        top2.grab_set()
        top2.geometry("480x150+800+100")
        top2.config(background="#0C283D")

        m1 = Label(top2, text="Matrice", font=("Times New Roman", 26), bg="#0C283D", fg="white")
        m1.place(x=10, y=10)

        Label(top2, text="Lignes/Colonnes:", font=("Constantia", 20), bg="#0C283D", fg="white").place(x=10, y=50)
        entr_l = Spinbox(top2, from_=2, to=8, width=7)
        entr_l.place(x=230, y=63)
        Button(top2, text="VALIDER", font=("Constantia", 16), bg="green", command=get_dim).pack(side=BOTTOM)

    def entrer_dim1(self):
        def getvaleursdim():

            def affiche_matrices(nc1, nl1, nc2, nl2):

                def calculer():
                    valeurs_m1 = []
                    valeurs_m2 = []

                    mu = []
                    try:
                        for widget in self.frame_mat1.winfo_children():
                            recup_valeurs(widget, valeurs_m1, self.dic_nc['nc1'], mu)

                        for widget in self.frame_mat2.winfo_children():
                            recup_valeurs(widget, valeurs_m2, self.dic_nc['nc2'], mu)

                    except:
                        messagebox.showerror("ERREUR",
                                             "UNE ERREUR S'EST PRODUITE !\nREVERIFIEZ LES VALEURS ENTREES")

                    else:
                        A = eval(coeff_mat1.get()) * np.array(valeurs_m1)
                        B = eval(coeff_mat2.get()) * np.array(valeurs_m2)
                        # print(f"{A=}\n{B=}")
                        if self.operations.get().split()[0] == "*":
                            if A.shape[1] != B.shape[0]:
                                messagebox.showwarning("ATTENTION",
                                                       "LE NOMBRE DE COLONNES DE M1 DOIT ÊTRE EGAL AU NOMBRE DE LIGNES DE M2!")
                            else:
                                C = np.dot(A, B)
                                # print(f"{C=}")
                                affiche_solution(self.fraction_element(C), "Matrice1 * Matrice2")

                        elif self.operations.get().split()[0] == "+":
                            a_shape = A.shape
                            b_shape = B.shape
                            # print(f"{a_shape=}, {b_shape=}")
                            if a_shape[0] != b_shape[0] or a_shape[1] != b_shape[1]:
                                messagebox.showwarning("ATTENTION", "LES MATRICES DOIVENT AVOIR LA MEME DIMENSION !")
                            else:
                                C = A + B
                                affiche_solution(self.fraction_element(C), "Matrice1 + Matrice2")

                        elif self.operations.get().split()[0] == "-":
                            # print(f"{A=}, {B=}")
                            a_shape = A.shape
                            b_shape = B.shape
                            if a_shape[0] != b_shape[0] or a_shape[1] != b_shape[1]:
                                messagebox.showwarning("ATTENTION", "LES MATRICES DOIVENT AVOIR LA MEME DIMENSION !")
                            else:
                                C = A - B
                                affiche_solution(self.fraction_element(C), "Matrice1 - Matrice2")

                def recup_valeurs(widget, valeurs_m, nc, mu):
                    if widget.winfo_class() == "Entry" and widget.winfo_x() not in [5, 7]:
                        # try:
                        mu.append(eval(widget.get()))
                        # except:
                        # messagebox.showerror("Erreur", "Revérifiez les valeurs entrées !")

                        if len(mu) == nc:
                            valeurs_m.append([x for x in mu])
                            mu.clear()

                def affiche_solution(matrice_s, texte_s):
                    self.destroy_element(self.frame_mat3)
                    Label(self.frame_mat3, text=texte_s, font=("Times New Roman", 26), bg="#0C283D",
                          fg="sky blue").place(x=5, y=0)
                    Button(self.frame_mat3, text="copier", font=("Fixedsys", 12), bg="#33AB0F",
                           command=lambda: self.copy_mat(self.frame_mat3, len(matrice_s[0]), co_entryx=None)).place(
                        x=310, y=10)
                    ydepart = 50
                    for x in range(len(matrice_s)):
                        xdepart = 5
                        for u in range(len(matrice_s[0])):
                            abc = Entry(self.frame_mat3, width=4, font=("Times New Roman", 12))
                            abc.insert(0, matrice_s[x][u])
                            abc.place(x=xdepart, y=ydepart)
                            xdepart += 40
                        ydepart += 30

                self.destroy_element(self.frame_mat1)
                self.destroy_element(self.frame_mat2)
                self.destroy_element(self.frame_mat3)
                self.dic_nc['nc1'] = nc1
                self.dic_nc['nc2'] = nc2
                Label(self.frame_mat1, text="Matrice 1", font=("Times New Roman", 26), bg="#0C283D", fg="orange").place(
                    x=55, y=0)
                Button(self.frame_mat1, text="copier", font=("Fixedsys", 12), bg="#33AB0F",
                       command=lambda: self.copy_mat(self.frame_mat1, self.dic_nc['nc1'], co_entryx=True)).place(x=245,
                                                                                                                 y=10)
                Button(self.frame_mat1, text="coller", font=("Fixedsys", 12), bg="#33AB0F",
                       command=lambda: self.paste_mat(self.frame_mat1, 50, 55, co_entryx=True)).place(x=310, y=10)
                ydepart = 50
                for x in range(nl1):
                    xdepart = 55
                    for u in range(nc1):
                        abc = Entry(self.frame_mat1, width=4, font=("Times New Roman", 12))
                        abc.insert(0, "0")
                        abc.place(x=xdepart, y=ydepart)
                        xdepart += 40
                    ydepart += 30
                coeff_mat1 = Entry(self.frame_mat1, width=4, font=("Times New Roman", 12))
                coeff_mat1.insert(0, "1")
                yinf1 = int((ydepart - 50) / 2) + 50

                Label(self.frame_mat2, text="Matrice 2", font=("Times New Roman", 26), bg="#0C283D", fg="purple").place(
                    x=55, y=0)
                Button(self.frame_mat2, text="copier", font=("Fixedsys", 12), bg="#33AB0F",
                       command=lambda: self.copy_mat(self.frame_mat2, self.dic_nc['nc2'], co_entryx=True)).place(x=245,
                                                                                                                 y=10)
                Button(self.frame_mat2, text="coller", font=("Fixedsys", 12), bg="#33AB0F",
                       command=lambda: self.paste_mat(self.frame_mat2, 50, 55, co_entryx=True)).place(x=310, y=10)
                ydepart = 50
                for x in range(nl2):
                    xdepart = 55
                    for u in range(nc2):
                        abc = Entry(self.frame_mat2, width=4, font=("Times New Roman", 12))
                        abc.insert(0, "0")
                        abc.place(x=xdepart, y=ydepart)
                        xdepart += 40
                    ydepart += 30
                coeff_mat2 = Entry(self.frame_mat2, width=4, font=("Times New Roman", 12))
                coeff_mat2.insert(0, "1")
                yinf2 = int((ydepart - 50) / 2) + 50
                coeff_mat1.place(x=5, y=min(yinf1, yinf2) - 10)
                coeff_mat2.place(x=5, y=min(yinf1, yinf2) - 10)
                self.operations.place(x=400, y=min(yinf1, yinf2) + 60)
                Button(self.f2_o2, text="Calculer", font=("Times New Roman", 16), bg="green", command=calculer).place(
                    x=435, y=10)

            nl1 = int(entr_l1.get())
            nl2 = int(entr_l2.get())
            nc1 = int(entr_col1.get())
            nc2 = int(entr_col2.get())

            def btn_reint():
                affiche_matrices(nc1, nl1, nc2, nl2)

            self.reinit_btn.config(command=btn_reint)
            self.reinit_btn.place(x=727, y=640)

            affiche_matrices(nc1, nl1, nc2, nl2)

            top.destroy()

        top = Toplevel()
        top.title("Dimensions des matrices")
        top.iconbitmap("alpha.ico")
        top.grab_set()
        top.geometry("480x400+800+100")
        top.config(background="#0C283D")

        m1 = Label(top, text="Matrice1", font=("Times New Roman", 26), bg="#0C283D", fg="white")
        m1.place(x=10, y=40)

        ligne1 = Label(top, text="Ligne:", font=("Constantia", 20), bg="#0C283D", fg="white")
        ligne1.place(x=10, y=80)
        entr_l1 = Spinbox(top, from_=2, to=8, width=7)
        entr_l1.place(x=100, y=90)

        col1 = Label(top, text="Colonne:", font=("Constantia", 20), bg="#0C283D", fg="white")
        col1.place(x=250, y=80)
        entr_col1 = Spinbox(top, from_=2, to=8, width=7)
        entr_col1.place(x=380, y=90)

        m2 = Label(top, text="Matrice2", font=("Times New Roman", 26), bg="#0C283D", fg="white")
        m2.place(x=10, y=200)
        ligne2 = Label(top, text="Ligne:", font=("Constantia", 20), bg="#0C283D", fg="white")
        ligne2.place(x=10, y=240)
        entr_l2 = Spinbox(top, from_=2, to=8, width=7)
        entr_l2.place(x=100, y=250)

        col2 = Label(top, text="Colonne:", font=("Constantia", 20), bg="#0C283D", fg="white")
        col2.place(x=250, y=240)
        entr_col2 = Spinbox(top, from_=2, to=8, width=7)
        entr_col2.place(x=380, y=250)
        Button(top, text="VALIDER", font=("Constantia", 16), bg="green", command=getvaleursdim).pack(side=BOTTOM)


app_mat = Matrix(f2)
app_mat.grid()

# ==================================================Onglet_Facteurs_premiers_ou_f3=========================================================================


class Prime_n(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)

        self.affiche_decomp = Text(root, width=70, height=6, takefocus=0, font=("Courier New", 20), bg='#9E9050',
                                   fg='black')
        self.affiche_decomp.pack(fill=X)

        self.btn_tt_effacer = Button(root, text="Réinitialiser", font=("Constantia", 20), bg="purple", fg="black",
                                     command=self.reinit_afficheur)
        self.btn_tt_effacer.pack()

        self.f3_entry = Entry(root, width=18, takefocus=1, font=("Times New Roman", 20), bg='white', fg='black')
        self.f3_entry.insert(0, "0")
        self.f3_entry.place(x=80, y=400)

        Button(f3, text=" \u232B ", font=("Times New Roman", 16), width=3, bg="red", fg="black",
               command=self.bouton_effacer).place(x=270, y=450)
        Button(f3, text=" AC ", font=("Times New Roman", 16), width=3, bg="red", fg="black",
               command=self.bouton_AC).place(x=270, y=500)
        Button(f3, text="  =  ", font=("Times New Roman", 16), width=3, bg="green", fg="black",
               command=self.bouton_egal).place(x=270, y=550)
        Button(f3, text=" 0 ", font=("Times New Roman", 16), width=3, bg="sky blue", fg="black",
               command=lambda: self.bouton_nbre('0')).place(x=160, y=600)

        lste_btns = [7, 8, 9, 4, 5, 6, 1, 2, 3]
        xa = 105
        ya = 450
        ipq = 0
        for h in lste_btns:
            Button(f3, text=f" {h} ", font=("Times New Roman", 16), width=3, bg="sky blue", fg="black",
                   command=lambda h=h: self.bouton_nbre(f'{h}')).place(x=xa, y=ya)
            ipq += 1
            xa += 55
            if ipq == 3:
                xa = 105
                ya += 50
                ipq = 0

        self.zone_pgcd = Frame(f3, width=470, height=200, bg="#0C283D")
        self.zone_pgcd.place(x=370, y=400)
        self.list_premier = []

    def premier(self, a, rac_a):
        j = 999985
        if rac_a < j:  # si entre 1 et sqrt(a) il n'y a pas de diviseurs de a, alors a est permier !
            return a  # a est premier
        else:
            while j <= int(rac_a):
                check = a % j
                if check == 0:
                    # print("Le plus petit diviseur de {} hors mis 1 est {}.".format(a, j))
                    return j  # retourne le plus petit diviseur de a
                    # break
                else:
                    j += 2

                if j > int(rac_a):
                    # print(a,"est un nombre premier !")
                    return a  # retourne a lui mm

    def bouton_nbre(self, nbre):
        if self.f3_entry.get() == "0":
            self.f3_entry.delete(0, END)
        pos = len(self.f3_entry.get())
        self.f3_entry.insert(pos, nbre)

    def bouton_effacer(self):
        pos = len(self.f3_entry.get())
        self.f3_entry.delete(pos - 1)

    def bouton_AC(self):
        self.f3_entry.delete(0, END)

    def reinit_afficheur(self):
        destroy_element(self.zone_pgcd)
        self.list_premier.clear()
        self.affiche_decomp.delete(1.0, END)

    def id_bezout(self, m, n):
        l = []
        a = max(m, n)
        b = min(m, n)
        r = 1
        while r != 0:
            q = a // b
            r = a % b
            l.append([1, a, -q, b])
            a, b = b, r

        d = len(l[:-1])
        # substitution remontante pour obtenir les coefficients de Bezout
        for j in range(d - 1):
            for k in range(0, 4, 2):
                l[-2 - j - 1][k] *= l[-2 - j][2]
            l[-2 - j - 1][2] += l[-2 - j][0]

        destroy_element(self.zone_pgcd)
        pos = self.zone_pgcd.config(bg='#7A7830')
        Label(self.zone_pgcd, text=f"ppcm({m}, {n}) = {int(abs(m * n) / a)}", font=("Mongolian Baiti", 18),
              bg="#7A7830",
              fg="black").place(x=0, y=10)
        Label(self.zone_pgcd, text=f"pgcd({m}, {n}) = {a}", font=("Mongolian Baiti", 18), bg="#7A7830",
              fg="black").place(x=0, y=55)
        Label(self.zone_pgcd, text="Identité de Bézout", font=("Mongolian Baiti", 18, "underline"), bg="#7A7830",
              fg="black").place(x=0, y=95)
        Label(self.zone_pgcd, text=f"{a} = ({l[0][0]}) x {l[0][1]} + ({l[0][2]}) x {l[0][3]}",
              font=("Mongolian Baiti", 18),
              bg="#7A7830", fg="black").place(x=0, y=135)

    def bouton_egal(self):
        nbre = self.f3_entry.get()
        if nbre != "0":
            try:
                f = int(nbre)
            except:
                messagebox.showerror("ERREUR",
                                     "UNE ERREUR S'EST PRODUITE !\nREVERIFIEZ LES VALEURS ENTREES")
            else:
                self.list_premier.append(f)
                if len(self.list_premier) >= 2:
                    if len(self.list_premier) == 2:
                        self.id_bezout(self.list_premier[0], self.list_premier[1])
                    else:
                        self.list_premier.pop(0)
                        self.id_bezout(self.list_premier[0], self.list_premier[1])
                y = f
                g = []
                gt = []
                for v in lp:
                    if v <= y:
                        u = 0
                        d = 0
                        while d == 0:
                            r = y // v
                            d = y % v

                            if d == 0:
                                u += 1
                                y = r

                            if d != 0 and u >= 1:
                                if u > 1:
                                    g.extend([v, u])
                                    a = "^".join(str(p) for p in g)
                                    g = []
                                    gt.append(a)
                                else:
                                    gt.append(str(v))

                            if y == 1 and d != 0:  # décomposition terminée
                                break
                    else:
                        break

                while y != 1:  # décomposition inachevée avec un y sans diviseur dans lp
                    ra_y = sqrt(y)
                    h = self.premier(y, ra_y)
                    if h == y:  # y est un nbre 1er
                        gt.append(str(h))
                        break

                    else:  # y est un nbre 1er > 999983 ou un produit de nbres 1ers > 999983
                        u = 0  # suite de la décomposition
                        d = 0
                        while d == 0:
                            r = y // h
                            d = y % h
                            if d == 0:
                                u += 1
                                y = r

                            if u >= 1:
                                if u > 1:
                                    g.extend([h, u])
                                    a = "^".join(str(p) for p in g)
                                    g = []
                                    gt.append(a)
                                else:
                                    gt.append(str(h))

                j = " x ".join(k for k in gt)
                self.affiche_decomp.insert(1.0, f"{f} = {j}\n")


app_prime = Prime_n(f3)
app_prime.pack()

# ===============================Onglet_Sys_num_f4==================================================#


class Converteur(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(bg="#0C283D")
        Label(self, text="Nombre ", font=("Times New Roman", 20), bg="#0C283D", fg="#B02836").grid(row=0, column=0)
        self.nconv = Entry(self, width=15, font=("Mongolian Baiti", 20), bg="ivory")
        self.nconv.grid(row=0, column=1)
        Button(self, text="\u232B", font=("Times New Roman", 14), bg="red", command=self.cleaning).grid(row=0, column=3,
                                                                                                        padx=40)
        self.place(x=0, y=50)

        Label(root, text="Base de départ", font=("Constantia", 20), bg="#0C283D", fg="#B02836").place(x=0, y=150)

        liste_bases = ["2", "8", "10", "16"]
        self.bases = ttk.Combobox(root, values=liste_bases, width=5, font=("Mongolian Baiti", 16))
        self.bases.current(0)
        self.bases.place(x=190, y=155)
        Button(root, text="CONVERTIR", font=("Mongolian Baiti", 20), bg="#2D7D4E", command=self.convertir).place(x=30,
                                                                                                                 y=250)

        self.label1 = Label(f4, text="", font=("Constantia", 20), bg="#0C283D", fg="blue")
        self.entr1 = Entry(f4, width=30, font=("Mongolian Baiti", 20))

        self.label2 = Label(f4, text="", font=("Constantia", 20), bg="#0C283D", fg="blue")
        self.entr2 = Entry(f4, width=30, font=("Mongolian Baiti", 20))

        self.label3 = Label(f4, text="", font=("Constantia", 20), bg="#0C283D", fg="blue")
        self.entr3 = Entry(f4, width=30, font=("Mongolian Baiti", 20))

    def cleaning(self):
        self.nconv.delete(0, END)

    def convertir(self):
        self.dep = int(self.bases.get())
        self.nbre = self.nconv.get()

        if "," in self.nbre:
            self.nbre = self.nconv.get().replace(",", ".")

        def deci_to_base2n(n, arr):
            j = int(float(n))
            l1 = ['A', 'B', 'C', 'D', 'E', 'F']
            q = 1
            l = []
            while q != 0:
                r = j % arr
                q = j // arr
                if arr == 16 and r >= 10:  # Remplacement des valeurs >= 10 par leurs équivalents en hexadécimal
                    d = r - 10
                    r = l1[d]
                l.append(r)
                j = q

            l.reverse()

            # Conversion de la partie décimale
            if float(n) != int(float(n)):
                l.append(".")
                i = float(n) - int(float(n))
                while int(i) != i:
                    i *= arr

                    d = int(i)
                    if arr == 16 and d >= 10:  # Remplacement des valeurs >= 10 par leurs équivalents en hexadécimal
                        r = d - 10
                        d = l1[r]

                    l.append(d)
                    i -= int(i)
                    # print(int(i))

                    # print(l)

            b = "".join(str(k) for k in l)
            return b

        def base2n_to_deci(n, dep):
            check = True
            if dep == 2 or dep == 8:
                # Vérificaton de l'appartenance à la base de départ
                verif_list = [m for m in n]
                if "." in verif_list: verif_list.remove(".")
                verif_list1 = [int(m) for m in verif_list]

                for m in verif_list1:
                    if m < 0 or m > (dep - 1):
                        messagebox.showerror("ERREUR", "REVERIFIEZ LES VALEURS ENTREES")
                        check = False
                        break

            if check:
                l = [h for h in n.upper()]
                t = len(l)
                lt = ['A', 'B', 'C', 'D', 'E', 'F']
                if dep == 16:
                    for k in range(t):
                        m = 0
                        while m < 6:
                            # print(m)
                            if l[k] == lt[m]:
                                l[k] = str(m + 10)
                                m = 6
                            m += 1

                # Traitement de la partie entière
                if "." in l:
                    m = l.index(".")
                    l1 = [int(c) for c in l[:m]]
                else:
                    l1 = [int(c) for c in l]
                h = len(l1)
                p = 0
                l1.reverse()
                for k in range(h):
                    p += (l1[k]) * (dep ** k)

                # Traitement de la partie décimale
                if "." in l:
                    m = l.index(".")
                    del l[:m + 1]
                    l1 = [int(c) for c in l]

                    h = len(l1)
                    for e in range(h):
                        d = pow(dep, -(e + 1))
                        p += (l1[e]) * (d)

                return str(p)

        if self.dep == 2:
            self.i = base2n_to_deci(self.nbre, self.dep)
            self.j = deci_to_base2n(self.i, 8)
            self.k = deci_to_base2n(self.i, 16)
            self.label1.config(text="Base 8", bg="#585E91")
            self.label2.config(text="Base 10", bg="#585E91")
            self.label3.config(text="Base 16", bg="#585E91")

        elif self.dep == 8:
            self.i = base2n_to_deci(self.nbre, self.dep)
            self.j = deci_to_base2n(self.i, 2)
            self.k = deci_to_base2n(self.i, 16)
            self.label1.config(text="Base 2")
            self.label2.config(text="Base 10")
            self.label3.config(text="Base 16")

        elif self.dep == 16:
            self.i = base2n_to_deci(self.nbre, self.dep)
            self.j = deci_to_base2n(self.i, 2)
            self.k = deci_to_base2n(self.i, 8)
            self.label1.config(text="Base 2")
            self.label2.config(text="Base 8")
            self.label3.config(text="Base 10")

        else:
            self.i = deci_to_base2n(self.nbre, 2)
            self.j = deci_to_base2n(self.nbre, 8)
            self.k = deci_to_base2n(self.nbre, 16)
            self.label1.config(text="Base 2")
            self.label2.config(text="Base 8")
            self.label3.config(text="Base 16")

        self.entr1.delete(0, END)
        self.entr1.insert(0, self.j)
        self.entr1.place(x=120, y=385)
        self.entr2.delete(0, END)
        self.entr2.insert(0, self.i)
        self.entr2.place(x=120, y=455)
        self.entr3.delete(0, END)
        self.entr3.insert(0, self.k)
        self.entr3.place(x=120, y=525)

        self.label1.place(x=0, y=380)

        # entr1.place(x=120, y=385)

        self.label2.place(x=0, y=450)

        # entr2.place(x=120, y=455)

        self.label3.place(x=0, y=520)


app_conv = Converteur(f4)
app_conv.grid()

# ==============================Onglet_Fonctions_f5===================================


class Functions(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        # +++++++++++++++++++++ Intégrales +++++++++++++++++++++++++

        self.labelframe1 = LabelFrame(root, width=550, height=210, text="Calcul d'intégrales", font=("Constantia", 20),
                                 bg="#0C283D", fg="#5DA8C3")
        self.labelframe1.place(x=10, y=10)
        
        Label(self.labelframe1, text="ʃ", font=("Times New Roman", 48), bg="#0C283D", fg="#5DA8C3").place(x=15, y=20)
        self.a_intg = Entry(self.labelframe1, width=2, font=('Mongolian Baiti', 14))
        self.a_intg.place(x=20, y=100)
        self.b_intg = Entry(self.labelframe1, width=2, font=('Mongolian Baiti', 14))
        self.b_intg.place(x=20, y=7)
        self.f_intg = Entry(self.labelframe1, width=15, font=('Mongolian Baiti', 18))
        self.f_intg.place(x=40, y=55)
        Label(self.labelframe1, text="dx  =", font=("Times New Roman", 22), bg="#0C283D", fg="#5DA8C3").place(x=225, y=50)
        self.r_intg = Entry(self.labelframe1, width=15, font=('Mongolian Baiti', 18))
        self.r_intg.place(x=290, y=55)
        Button(self.labelframe1, text="Calculer", font=('Constantia', 12), bg="#0BAE28", bd=3, command=lambda: self.calc_func("intg")).place(x=190, y=135)
        Button(self.labelframe1, text="Effacer", font=('Constantia', 12), bg="#B1100E", bd=3,
               command=lambda: self.eff_func([self.a_intg, self.b_intg, self.r_intg, self.f_intg])).place(x=270, y=135)
        
        # +++++++++++++++++++++ Limites +++++++++++++++++++++++++
        self.labelframe2 = LabelFrame(root, width=550, height=180, text="Calcul de limites", font=("Constantia", 22),
                                 bg="#0C283D", fg="#5DA8C3")
        self.labelframe2.place(x=10, y=280)
        Label(self.labelframe2, text="lim", font=("Times New Roman", 40), bg="#0C283D", fg="#5DA8C3").place(x=15, y=7)
        Label(self.labelframe2, text="x →", font=("Times New Roman", 16), bg="#0C283D", fg="#5DA8C3").place(x=15, y=68)
        self.v_lim = Entry(self.labelframe2, width=3, font=('Mongolian Baiti', 14))
        self.v_lim.place(x=65, y=70)
        
        self.mod = IntVar()
        # mod.set('normal')
        Checkbutton(self.labelframe2, text="-", font=("Times New Roman", 12), bg="#0C283D", fg="#076AFF",
                    onvalue=1, variable=self.mod).place(x=45, y=100)
        Checkbutton(self.labelframe2, text="+", font=("Times New Roman", 12), bg="#0C283D", fg="#076AFF",
                    onvalue=2, variable=self.mod).place(x=85, y=100)
        self.f_lim = Entry(self.labelframe2, width=15, font=('Mongolian Baiti', 18))
        self.f_lim.place(x=110, y=30)
        Label(self.labelframe2, text="=", font=("Times New Roman", 40), bg="#0C283D", fg="#5DA8C3").place(x=300, y=12)
        self.r_lim = Entry(self.labelframe2, width=15, font=('Mongolian Baiti', 18))
        self.r_lim.place(x=340, y=30)
        Button(self.labelframe2, text="Calculer", font=('Constantia', 12), bg="#0BAE28", bd=3, command=lambda: self.calc_func("limit")).place(x=190, y=100)
        Button(self.labelframe2, text="Effacer", font=('Constantia', 12), bg="#B1100E", bd=3,
               command=lambda: self.eff_func([self.v_lim, self.r_lim, self.f_lim])).place(x=270, y=100)
        
    def eff_func(self, tab):  # efface tous les champs relatifs au calcul
        for b in tab:
            b.delete(0, END)

    def transf_answ(self, resp):  # fonction permettant de transformer un flottant en fraction
        if str(resp) == '-oo' or str(resp) == 'oo':
            resp = resp
    
        elif type(resp) is sympy.core.numbers.Float:
            resp = Fraction(str(resp)).limit_denominator()
        return resp

    def calc_func(self, typ):  # fonction de calcul d'intégrale et de limite
        if typ == "intg":
            try:
                self.r_intg.delete(0, END)
                self.f_val = eval(self.f_intg.get())
                """a_val = eval(a_intg.get().replace("oo", "np.inf"))
                b_val = eval(b_intg.get().replace("oo", "np.inf"))"""
                self.a_val = eval(self.a_intg.get())
                self.b_val = eval(self.b_intg.get())
                # print(type(f_val), type(a_val), type(b_val))
                x = Symbol('x')
                ans = integrate(self.f_val, (x, self.a_val, self.b_val))
                # print(ans)
                "repo = round(integrate.quad(f_val, a_val, b_val)[0], 9)"
                self.r_intg.insert(0, f"{ans}")
            
            except:
                messagebox.showerror("Erreur !!!",
                                     "Revérifez les valeurs entrées !\nEn cas de persistance du problème cliquez sur le bouton \"Aide\" pour voir les règles de syntaxe.")
    
        elif typ == "limit":
            from sympy.abc import x
            try:
                self.r_lim.delete(0, END)
                self.f_val = eval(self.f_lim.get())
                self.v_val = eval(self.v_lim.get())
                #print(f_val, v_val)
                if self.mod.get() == 0:
                    resp = self.transf_answ(limit(self.f_val, x,self.v_val))
                    #print('   frf ',resp)
                    self.r_lim.insert(0, f"{resp}")
                elif self.mod.get() == 1:
                    resp = self.transf_answ(limit(self.f_val, x, self.v_val, dir='-'))
                    #print('   frf ',resp)
                    self.r_lim.insert(0, f"{resp}")
                elif self.mod.get() == 2:
                    resp = self.transf_answ(limit(self.f_val, x, self.v_val, dir='+'))
                    #print('   frf ',resp)
                    self.r_lim.insert(0, f"{resp}")
            except:
                messagebox.showerror("Erreur !!!",
                                     "Revérifez les valeurs entrées !\nEn cas de persistance du problème cliquez sur le bouton \"Aide\" pour voir les règles de syntaxe.")


app_func = Functions(f5)
app_func.grid()

# +++++++++++++++++++ Traceur de courbes ++++++++++++++++++++
Button(f5, text='Traceur de courbe', font=('Mongolian Baiti', 20),
       fg="#0C283D", command=draw_function).place(x=10, y=550)

# +++++++++++++++++++ Aide ++++++++++++++++++++++++++++++++


def aide():
    messagebox.showinfo("Règles de syntaxe", """\u2725 Variables: La variable de fonctions entrées doit être \"x\"\n
\u2725 Assurez vous de mettre correctement toutes les parenthèses\n
\u2725 Opérateurs: addition +, soustraction -, division ou fraction /, multiplication * (NE PAS UTILISER x qui est une variable),
puissance ou exposant **\n
\u2725 Infini: pour +∞ entrer oo (deux \"o\", se lit oh-oh) et pour -∞, -oo\n
\u2725 Racine carrée: sqrt( ) ou ( )**(1/2)\n 
\u2725 Exponentielle: exp( ), pour e=2.7182 utiliser e ou exp(1)\n
\u2725 Logarithmes: log( ), ln( )\n 
\u2725 Trigonométrie: cos( ), sin( ), tan( ), asin( ), acos( ), atan( ), cot( ), acot( )\n
\u2725 Trigo hyperbolique: cosh( ), sinh( ), tanh( ), asinh( ), acosh( ), atanh( ), coth( ), acoth( ). \n \u26A0Sauf indication contraire les angles sont en radian\n
\u2725 Valeur absolue: abs( )\n
\u2725 Exemples pratiques: 4x² + 2x + 6 <=> 4 * x**2 + 2*x + 3
                       √(exp(2x)) <=> (exp(2))**(1/2)""")


# Button(f5, text='Aide', font=('Mongolian Baiti', 20), fg="#0C283D", bg="#1C77FA", command=aide).place(x=350, y=550)
Button(f5, text=" Aide ", font=('Constantia', 14), relief=GROOVE, bg="#1CE116", command=aide).place(x=750, y=665)

# ============================== Onglet_Vecteurs_f6 ===========================================


class calc_vec(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.config(width=970, height=710)
        self.config(bg="#0C283D")

        def nothing():
            file = Toplevel(self)
            button = Button(file, text="do nothing")
            button.pack()

        self.operations = ttk.Combobox(self, values=["+", "-", "^", '.'], width=3, height=5)
        self.operations.current(0)
        self.frame_vec1 = Frame(self, relief=GROOVE, bg="#0C283D", borderwidth=10)
        self.frame_vec1.config(height=300, width=400)
        self.frame_vec2 = Frame(self, relief=GROOVE, bg="#0C283D", borderwidth=10)
        self.frame_vec2.config(height=300, width=400)
        self.frame_vec3 = Frame(self, relief=GROOVE, bg="#0C283D", borderwidth=10)
        self.frame_vec3.config(height=300, width=400)
        frame_pvec = Frame(self, relief=GROOVE, bg="white", borderwidth=10)
        self.frame_teta = Frame(self, relief=GROOVE, bg="#0C283D", borderwidth=10)

        self.frame_vec1.place(x=0, y=50)
        self.frame_vec2.place(x=470, y=50)

        entre = Button(self, text="Dimensions ", bg="#C72914", command=self.dim, font=("HELVETICA", 12))
        entre.place(x=300, y=5)

        self.dic = {}

    def dim(self):
        n = Toplevel()
        n.title("Dimension des vecteurs")
        n.grab_set()
        n.config(background="#0C283D")
        n.geometry("400x250+000+100")

        f = Frame(n, bg="#0C283D")
        m1 = Label(f, text="Vecteur(s)", bg="#0C283D", font=("HELVETICA", 26))
        m1.grid(column=0, row=0, padx=5, pady=20, columnspan=3, sticky='w')
        m1_ligne = Label(f, text="Dimension :", bg="#0C283D", font=("HELVETICA", 20))
        m1_ligne.grid(column=0, row=2, padx=5)
        self.entry_dim = Spinbox(f, from_=2, to=8, width=7)
        self.entry_dim.grid(column=1, row=2, padx=5)
        m2_ligne = Label(f, text="Calculs :", bg="#0C283D", font=("HELVETICA", 20))
        m2_ligne.grid(column=0, row=4, padx=5)
        self.calc = ttk.Combobox(f, values=["Opérations", "Norme"])
        self.calc.current(0)
        self.calc.grid(column=1, row=4, padx=5)
        valider = Button(f, text="Valider ", bg="#C72914",
                         command=lambda: self.getvaldim_vec(int(self.entry_dim.get()), n, self.calc.get()),
                         font=("HELVETICA", 12))
        valider.grid(column=4, row=10, columnspan=5, pady=50)
        f.pack()
        n.mainloop()

    def getvaldim_vec(self, cmy, frame, nsm):
        frame.destroy()
        self.nl1 = cmy

        if nsm == 'Opérations':
            self.operations = ttk.Combobox(self, values=["+", "-", "^", '.'], width=3, height=5)
            self.operations.current(0)
            self.frame_vec3 = Frame(self, relief=GROOVE, bg="#0C283D", borderwidth=10)
            self.frame_vec3.config(height=300, width=400)
            self.frame_vec3.place(x=210, y=400)

            def affiche_vec(nl1, coef1, coef2):
                valeurs_vec1 = []
                valeurs_vec2 = []

                for widget in self.frame_vec1.winfo_children():
                    if widget is not coef1:
                        recup_valeurs(widget, valeurs_vec1, nl1)

                for widget in self.frame_vec2.winfo_children():
                    if widget is not coef2:
                        recup_valeurs(widget, valeurs_vec2, nl1)

                A = eval(coeff_vec1.get()) * np.array(valeurs_vec1)
                B = eval(coeff_vec2.get()) * np.array(valeurs_vec2)
                if self.operations.get().split()[0] == '+':
                    C = A + B
                    affiche_solution(C, " Vecteur 1 + Vecteurs 2")

                elif self.operations.get().split()[0] == '-':
                    C = A - B
                    affiche_solution(C, " Vecteur 1 - Vecteurs 2")

                elif self.operations.get().split()[0] == '.':
                    C = np.vdot(A, B)
                    affiche_solution(C, " Vecteur 1 . Vecteurs 2", '.')

                elif self.operations.get().split()[0] == '^':
                    if self.nl1 == 3:
                        C = np.cross(A, B)
                        affiche_solution(C, " Vecteur 1 ^ Vecteurs 2")
                    else:
                        messagebox.showwarning("Attention!!!",
                                               "Pour le produit vectoriel, les vecteurs doivent etre de dimension 3")

            def recup_valeurs(widget, valeurs_m, nc):
                if widget.winfo_class() == "Entry" and widget.winfo_x() != 7 and len(valeurs_m) <= nc:
                    valeurs_m.append(eval(widget.get()))

            def affiche_solution(vec_s, texte_s, b='+'):
                destroy_element(self.frame_vec3)
                Label(self.frame_vec3, text=texte_s, font=("Times New Roman", 16), bg="#0C283D", fg="sky blue").place(
                    x=5,
                    y=0)
                Button(self.frame_vec3, text="copier", font=("Fixedsys", 12), bg="#33AB0F",
                       command=lambda: copy_vec(self.frame_vec3, len(vec_s), co_entryx=None)).place(x=310, y=10)
                ydepart = 50
                if b == '.':
                    abc = Label(self.frame_vec3, text=str(vec_s), font=("Times New Roman", 26), bg="#0C283D")
                    abc.place(x=125, y=125)

                else:
                    for x in range(len(vec_s)):
                        xdepart = 100
                        abc = Entry(self.frame_vec3, width=4, font=("Times New Roman", 12))
                        abc.insert(0, vec_s[x])
                        abc.place(x=xdepart, y=ydepart)
                        ydepart += 30

            def destroy_element(frame):
                for widget in frame.winfo_children():
                    widget.destroy()

            valeurs_copie = []

            def copy_vec(frame, nc, co_entryx=None):
                valeurs_copie.clear()
                mu = []
                for widget in frame.winfo_children():
                    if widget.winfo_class() == "Entry":
                        if co_entryx and widget.winfo_x() == 7:
                            continue
                        mu.append(widget.get())
                        if len(mu) == nc:
                            valeurs_copie.append([x for x in mu])
                            mu.clear()

            def past_vec(frame, ydep, xdep, coef, co_entryx=None):
                if len(valeurs_copie) != 0:
                    for widget in frame.winfo_children():
                        if widget.winfo_class() == "Entry" and widget is not coef:
                            if co_entryx and widget.winfo_x() == 7:
                                continue
                            widget.destroy()

                    for x in range(self.nl1):
                        abc = Entry(frame, width=4, font=("Times New Roman", 12))
                        abc.insert(0, valeurs_copie[0][x])
                        abc.place(x=xdep, y=ydep)
                        ydep += 30

            destroy_element(self.frame_vec1)
            destroy_element(self.frame_vec2)
            destroy_element(self.frame_vec3)

            Label(self.frame_vec1, text="Vecteur 1", font=("Times New Roman", 26), bg="#0C283D", fg="orange").place(
                x=55,
                y=10)
            Button(self.frame_vec1, text="copier", font=("Fixedsys", 12), bg="#33AB0F",
                   command=lambda: copy_vec(self.frame_vec1, self.nl1, co_entryx=None)).place(x=245, y=10)
            Button(self.frame_vec1, text="coller", font=("Fixedsys", 12), bg="#33AB0F",
                   command=lambda: past_vec(self.frame_vec1, 50, 55, coeff_vec1, co_entryx=None)).place(x=310, y=10)
            ydepart = 50
            le_bay = self.nl1
            for x in range(le_bay):
                xdepart = 55
                abc = Entry(self.frame_vec1, width=4, font=("Times New Roman", 12))
                abc.insert(0, "0")
                abc.place(x=xdepart, y=ydepart)
                ydepart += 30
            coeff_vec1 = Entry(self.frame_vec1, width=4, font=("Times New Roman", 12))
            coeff_vec1.insert(0, "1")
            yinf1 = int((ydepart - 50) / 2) + 50
            Label(self.frame_vec2, text="Vecteur 2", font=("Times New Roman", 26), bg="#0C283D", fg="orange").place(
                x=55,
                y=10)
            Button(self.frame_vec2, text="copier", font=("Fixedsys", 12), bg="#33AB0F",
                   command=lambda: copy_vec(self.frame_vec2, self.nl1, co_entryx=None)).place(x=245, y=10)
            Button(self.frame_vec2, text="coller", font=("Fixedsys", 12), bg="#33AB0F",
                   command=lambda: past_vec(self.frame_vec2, 50, 55, coeff_vec2, co_entryx=None)).place(x=310, y=10)
            ydepart = 50
            for x in range(self.nl1):
                xdepart = 55
                abc = Entry(self.frame_vec2, width=4, font=("Times New Roman", 12))
                abc.insert(0, "0")
                abc.place(x=xdepart, y=ydepart)
                ydepart += 30
            coeff_vec2 = Entry(self.frame_vec2, width=4, font=("Times New Roman", 12))
            coeff_vec2.insert(0, "1")
            yinf2 = int((ydepart - 50) / 2) + 50
            coeff_vec1.place(x=5, y=yinf2 - 10)
            coeff_vec2.place(x=5, y=yinf2 - 10)
            self.operations.place(x=400, y=yinf1 + 60)
            Button(self, text='Calculer', font=("Times New Roman", 16), bg='green',
                   command=lambda: affiche_vec(self.nl1, coeff_vec1, coeff_vec2)).place(x=435, y=10)

        else:
            self.operations.destroy()
            self.frame_vec3.destroy()

            norme = Label(self.frame_vec2, text="Norme ", font=("Times New Roman", 26), bg="#0C283D", fg="orange")

            def destroy_element(frame):
                for widget in frame.winfo_children():
                    if widget is not norme:
                        widget.destroy()

            destroy_element(self.frame_vec1)
            destroy_element(self.frame_vec2)
            Label(self.frame_vec1, text="Vecteur 1", font=("Times New Roman", 26), bg="#0C283D", fg="orange").place(
                x=55,
                y=10)
            ydepart = 50
            le_bay = self.nl1
            for x in range(le_bay):
                xdepart = 55
                abc = Entry(self.frame_vec1, width=4, font=("Times New Roman", 12))
                abc.insert(0, "0")
                abc.place(x=xdepart, y=ydepart)
                ydepart += 30
            coeff_vec1 = Entry(self.frame_vec1, width=4, font=("Times New Roman", 12))
            coeff_vec1.insert(0, "1")
            yinf1 = int((ydepart - 50) / 2) + 50
            norme.place(x=55, y=10)

            coeff_vec1.place(x=5, y=yinf1 - 10)

            def aff_norm(nl1):
                valeurs_vec1 = []
                for widget in self.frame_vec1.winfo_children():
                    recup_valeurs(widget, valeurs_vec1, nl1)

                valeurs_vec1.pop(-1)
                A = eval(coeff_vec1.get()) * np.array(valeurs_vec1)
                C = np.linalg.norm(A)
                destroy_element(self.frame_vec2)
                abc = Label(self.frame_vec2, text=str(round(C, 3)), font=("Times New Roman", 26), bg="#0C283D")
                abc.place(x=125, y=125)

            def recup_valeurs(widget, valeurs_m, nc):
                if widget.winfo_class() == "Entry" and widget.winfo_x() != 7 and len(valeurs_m) <= nc:
                    valeurs_m.append(eval(widget.get()))

            Button(self, text='Calculer', font=("Times New Roman", 16), bg='green',
                   command=lambda: aff_norm(self.nl1)).place(x=435, y=10)


app_vect = calc_vec(f6)
app_vect.grid()

# ================================= A PROPOS ===================================================
img = PhotoImage(master=notebook, file="alpha.png")
Label(f7, image=img, text="   CALCULETTE\n   ALPHA", compound=LEFT, font=('Freestyle Script', 36, "bold"),
      bg="#0C283D", fg="deep sky blue").place(x=0, y=0)

Label(f7, text="        Cette application a été développée par Minervus & Kolobera, avec", font=("Constantia", 20)
      , bg="#0C283D", fg="deep sky blue").place(x=0, y=130)
Label(f7, text="pour public cible les taupins, les étudiants et toute autre personne",
      font=("Constantia", 20), bg="#0C283D", fg="deep sky blue").place(x=0, y=170)
Label(f7, text="évoluant dans un domaine en rapport avec les Mathématiques. La ", font=("Constantia", 20),
      bg="#0C283D", fg="deep sky blue").place(x=0, y=210)
Label(f7, text="Calculette Alpha permet d'effectuer divers calculs en Analyse, en Algèbre,", font=("Constantia", 20),
      bg="#0C283D", fg="deep sky blue").place(x=0, y=250)
Label(f7, text="de tracer des courbes de fonctions etc. Elle a entièrement été écrite en ",
      font=("Constantia", 20), bg="#0C283D", fg="deep sky blue").place(x=0, y=290)
Label(f7, text="python, dans le soucis d'apporter puissance et efficacité à vos calculs.", font=("Constantia", 20), bg="#0C283D",
      fg="deep sky blue").place(x=0, y=330)
Label(f7, text="       Nous vous remercions de vos éventuels commentaires, emails ",
      font=("Constantia", 20), bg="#0C283D", fg="deep sky blue").place(x=0, y=370)
Label(f7, text="d'encouragement, rapports de bugs, ...", font=("Constantia", 20), bg="#0C283D",
      fg="deep sky blue").place(x=0, y=400)
Label(f7, text="       Par ailleurs nous espérons qu'elle vous sera utile. Profitez bien!!\nMerci\n",
      font=("Constantia", 20), bg="#0C283D", fg="deep sky blue").place(x=0, y=450)

Label(f7, text="""                   ----------------------------------------
                    Python powered
                  Longue vie à Python
                   Et à l'Open-Source
                     ----------------------------------------\n""",
      font=("Constantia", 20), bg="#0C283D", fg="deep sky blue").place(x=100, y=520)
# =====================================================================================================================
notebook.grid(row=0, column=0, sticky="nw")
racine.mainloop()
