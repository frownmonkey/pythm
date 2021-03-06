# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the pythm for the
#   copyright and license terms.
#
### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
""" TODO: Module description """

import pygtk
pygtk.require('2.0')
import gtk
from page import Page
from pythm.lang import _
from pythm.backend import Signals
from gtkhelper import ImageButton,get_scrolled_widget
from pythm.constants import *

class PageBrowse(Page):
    def __init__(self):
        self.model = gtk.ListStore(object,str)
        Page.__init__(self)

        self.btn_up = ImageButton(gtk.STOCK_GO_UP)
        self.btnbox.add(self.btn_up)
        self.btn_up.connect("clicked",self.btn_up_clicked)

        self.btn_open = ImageButton(gtk.STOCK_OPEN)
        self.btnbox.add(self.btn_open)
        self.btn_open.connect("clicked",self.btn_open_clicked)

        self.btn_play= ImageButton(gtk.STOCK_MEDIA_PLAY)
        self.btnbox.add(self.btn_play)
        self.btn_play.connect("clicked",self.btn_play_clicked)
        self.path = None

        self.btn_adddir = ImageButton(gtk.STOCK_ADD)
        self.btnbox.add(self.btn_adddir)
        self.btn_adddir.connect("clicked",self.btn_adddir_clicked)
        self.path = None

        self.cfg.get_backend().connect(Signals.BROWSER_CHANGED,self.browser_changed)

    def btn_adddir_clicked(self,btn):
        entry = self.get_selected_entry()
        if entry != None:
            if entry.isDir:
                self.cfg.get_backend().add_dir(entry.id)
            else:
                self.cfg.get_backend().add(entry.id)
        # else load the current dir (entry == None)
        else:
            self.cfg.get_backend().add_dir(self.path)

    def btn_up_clicked(self,btn):
        self.cfg.get_backend().browse_up(self.path)

    def btn_open_clicked(self,btn):
        self.add_selected_entry()


    def btn_play_clicked(self,btn):
        self.btn_adddir_clicked(btn)
        # TODO make it play from here !
        self.cfg.get_backend().play()

    def browser_changed(self,path,list):
        self.path = path
        self.model.clear()
        for f in list:
            self.model.append([f,f.caption])
            if self.cfg.get("pythm","showpath",False) == 'False':
                self.tv.get_column(0).set_title(os.path.basename(path).replace("_","__"))
            else:
                self.tv.get_column(0).set_title(path.replace(self.cfg.get(CFG_SECTION_BROWSER, CFG_SETTING_MUSICDIR,""),"<MusicDir>").replace("_","__"))

    def row_activated(self, tv, path, view_column):
        self.add_selected_entry()

    def get_selected_entry(self):
        iter = self.tv.get_selection().get_selected()[1]
        if iter is not None:
            return self.model.get_value(iter,0)
        return None

    def add_selected_entry(self):
        entry = self.get_selected_entry()
        if entry != None:
            if entry.isDir:
                self.cfg.get_backend().browse(entry.id)
            else:
                self.cfg.get_backend().add(entry.id)


    def content(self):
        vbox = gtk.VBox()
        self.tv = gtk.TreeView(self.model)
        self.tv.connect("row_activated", self.row_activated)

        browsefont = self.cfg.get("pythm","browsefont",None)
        col_rendr = gtk.CellRendererText()
        if browsefont is not None:
            col_rendr.set_property("font-desc", pango.FontDescription(browsefont))
        col_file = gtk.TreeViewColumn("<MusicDir>",col_rendr,text=1)
        self.tv.append_column(col_file)
        sc = get_scrolled_widget()

        sc.add(self.tv)
        vbox.pack_start(sc,True,True,0)
        return vbox

