#!/usr/bin/env python
#coding=utf-8
# -*- coding: utf-8 -*-

# PyTPV, software point of sale for restaurant, bar and pizzeria.
# Copyright (C) 2007 Juan Jose Rojo
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Can you contact with author by means of email: <jjrojoc@gmail.com> or the
# next postal address:
# Juan Jose Rojo. San Lazaro, 13. 30840 Alhama de Murcia. Murcia. Spain
# This program comes with ABSOLUTELY NO WARRANTY; for details type `show w'.
# This is free software, and you are welcome to redistribute it
# under certain conditions; type `show c' for details.

import gtk
import pango
#import gobject
#import pango

class TreeView(gtk.TreeView):
    def __init__(self):
        """
        This class is an intermediate class for construct
        the store and views of the treeviews, also contain
        the methods for add, addlist, del, getCount of all 
        treeviews
        """
        gtk.TreeView.__init__(self)  
        self.get_selection().set_mode(gtk.SELECTION_SINGLE)
        self.set_rules_hint(True)
#        self.set_grid_lines(gtk.TREE_VIEW_GRID_LINES_VERTICAL)
        
    def _new_column(self,name,size,visible,sort,width,height,renderer,columna):
        if renderer == 'cell':
            cell = gtk.CellRendererText()
            col = gtk.TreeViewColumn(name, cell, text=columna)
#            font = pango.FontDescription('9')
#            cell.set_property('font-desc', font)
        elif renderer == 'pixbuf':
            cell = gtk.CellRendererPixbuf()        
            col = gtk.TreeViewColumn(name, cell, stock_id=columna)
        col.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        col.set_fixed_width(size)
        col.set_resizable(True)
        col.set_visible(visible)
        col.set_sort_column_id(sort)
        col.set_alignment(0.5)
        
        
        cell.set_fixed_size(width, height)
        #col.pack_start(cell,True)
        #col.set_cell_data_func(cell, None)
        return col
    
    
    def update(self, iter, column, newtext):
        selection = self.get_selection() 
        model, iter = selection.get_selected()
        self.liststore.set_value(iter, column, newtext)
        
        
    def add(self, value):
        return self.liststore.append(value)
       
    
    def prepend(self, value):
        return self.liststore.prepend(value)
#        iter = self.liststore.append(value)
#
#        # select new row and start editing it
#        path = self.liststore.get_path(iter)
#        self.get_selection().select_path(path)
#        
#        self.scroll_to_cell(path)
#        self.get_selection().select_path(path)
    
    
    def insert(self, count, value):
        return self.liststore.insert(count, value)
        
    
    def addList(self, values):
        # Removes the model so the addition is quicker
        self.set_model(None)
        # Freezes list so to cancel refresh event
        self.freeze_child_notify()

        for value in values:
            self.liststore.append(value)

        # set model back
        self.set_model(self.liststore)
        # Unfreeze the list
        self.thaw_child_notify()
        
    
    def remove(self):
        #http://eccentric.cx/misc/pygtk/pygtkfaq.html#13.8
        selection = self.get_selection() 
        model, iter = selection.get_selected()
        if iter:
            path = model.get_path(iter)
            model.remove(iter)
          
            selection.select_path(path)

            if not selection.path_is_selected(path):
                row = path[0]-1
             
                if row >= 0:
                    selection.select_path((row,))
                    
                    
    def getSelectedRow(self):
        selection = self.get_selection()
        model, paths = selection.get_selected_rows()
        # Returns first selected row
        return paths[0]
    

    def getSelectedItem(self, index):
        selection = self.get_selection()
        model, iter, = selection.get_selected()
        print model, iter
        return  self.liststore.get_value(iter, index)
    

    def getCount(self):
        return len(self.liststore)
    
    
    def clear(self):
        self.liststore.clear()
        
    
    def model_foreach(self, value):
        iter = self.liststore.foreach(self.change_tier, value)
        
        
    def change_tier(self, model, path, iter, data):
        t = self.liststore.get_value(iter, 0)

        if t == data[0]:
            a = 2
            b = 0
            datos = ("%0.2f" % data[1]) + ("%0.2f" % 1), ("%0.2f" % data[2])
            for x in range(6):
                self.liststore.set_value(iter, a, datos[b])
                a += 2
                b += 1
                
        
         
class TicketView(TreeView):
    def __init__(self, liststore):
        """
        This class represent ticketview of ticketstore
        """
        TreeView.__init__(self)
        # Defines the TreeStore
        self.liststore = gtk.ListStore(int, str, str, str, str, str, str, str)
#        # Associates the listStore to the ListView object
        
#       self.sorted = gtk.TreeModelSort(self.liststore)
#        self.sorted.set_sort_column_id(0, gtk.SORT_ASCENDING)

        self.set_model(self.liststore)
    
        cols = (\
                (("ID"),30, False, -1, -1, 35, 'cell', 0),\
                (("CR"),30, True, -1, -1, 35, 'pixbuf', 1),\
                (("SD"),30, True, -1, -1, 35, 'pixbuf', 2),\
                (("CO"),30, True, -1, -1, 35, 'pixbuf', 3),\
                (("NOMBRE"),220, True, -1, -1, 35, 'cell', 4),\
                (("DIRECCION"),220, True, -1, -1, 35, 'cell', 5),\
                (("IMP"),40, True, -1, -1, 35, 'cell', 6),\
                (("HORA"),40, True, -1, -1, 35,'cell', 7))
        
        for col in cols:
            self.append_column(
                self._new_column(
                    col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]))

class TicketLineaView(TreeView):
    def __init__(self, ticketstore):
        """
        This class represent ticketview of ticketstore
        """
        TreeView.__init__(self)    
        self.liststore = gtk.ListStore(int, str, str, str, str)
        # Associates the listStore to the ListView object
        self.set_model(self.liststore)
        
        cols = (\
                (("ID"),30, False, -1, -1, 35, 'cell', 0),\
                (("TICKET_FK_ID"),30, False, -1, -1, 35, 'cell', 1),\
                (("UNI"),40, True, -1, -1, 35, 'cell', 2),\
                (("DESCRIPCION"),200, True, -1, -1, 35, 'cell', 3),\
                (("IMP"),50, True, 4, -1, 35, 'cell', 4))
                
        for col in cols:
            self.append_column(
                self._new_column(
                    col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]))        
                    
class ClientesView(TreeView):
    def __init__(self, liststore):
        """
        This class represent ticketview of ticketstore
        """
        TreeView.__init__(self)    
        self.liststore = gtk.ListStore(int, str, str, str, str, str)
        # Associates the listStore to the ListView object
        self.set_model(self.liststore)
        #self.cargaDatos(CONSULTA_BASE)
        
        cols = (\
                (("ID"),50, True, 0, -1, 35, 'cell', 0),\
                (("NOMBRE"),300, True, 1, -1, 35, 'cell', 1),\
                (("DIRECCION"),300, True, 2, -1, 35, 'cell', 2),\
                (("TELEFONO"),200, True, 3, -1, 35, 'cell', 3),\
                (("FECHA_ALTA"),200, True, 4, -1, 35, 'cell', 4),\
                (("ULTIMA_COMPRA"),200, True, 5, -1, 35, 'cell', 5))
                        
        for col in cols:
            self.append_column(
                self._new_column(
                    col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]))        

class ArticulosView(TreeView):
    def __init__(self, liststore):
        """
        This class represent ticketview of ticketstore
        """
        TreeView.__init__(self)    
        self.liststore = gtk.ListStore(int, str, str, str, str, str, str)
        # Associates the listStore to the ListView object
        self.set_model(self.liststore)
        #self.cargaDatos(CONSULTA_BASE)

        cols = (\
                (("ID"),50, True, 0, -1, 35, 'cell', 0),\
                (("FAMILIA_FK_ID"),100, True, 1, -1, 35, 'cell', 1),\
                (("DESCRIPCION"),300, True, 2, -1, 35, 'cell', 2),\
                (("STOCK"),80, True, 3, -1, 35, 'cell', 3),\
                (("STOCK_MINIMO"),120, True, 4, -1, 35, 'cell', 4),\
                (("PRECIO_VENTA"),120, True, 5, -1, 35, 'cell', 5),\
                (("IMAGEN"),300, True, -1, -1, 35, 'cell', 6))
                #("BOTONERA_FK_ID"),80, True, 6, -1, 25,'cell', 7)
        for col in cols:
            self.append_column(
                self._new_column(
                    col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]))
                    

class FamiliaView(TreeView):
    def __init__(self, liststore):
        TreeView.__init__(self)
        self.liststore = gtk.ListStore(int, str, str)
        
        self.set_model(self.liststore)
        
        cols = (\
                (("ID"),50, True, -1, -1, 25, 'cell', 0),\
                (("NOMBRE"),100, True, -1, -1, 25, 'cell', 1),\
                (("DESCRIPCION"),100, True, -1, -1, 25, 'cell', 2))     
        
        for col in cols:
            self.append_column(
                self._new_column(
                    col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]))        

class CreditoView(TreeView):
    def __init__(self, liststore):
        # This class represent ticketview of ticketstore
        TreeView.__init__(self)    
        self.liststore = gtk.ListStore(int, str, str, str, str, str,str,str)
        # Associates the listStore to the ListView object
        self.set_model(self.liststore)
        #self.cargaDatos(CONSULTA_BASE)

        cols = (\
                (("ID"),50, True, -1, -1, 25, 'cell', 0),\
                (("FECHA"),100, True, -1, -1, 25, 'cell', 1),\
                (("HORA"),100, True, -1, -1, 25, 'cell', 2),\
                (("TIPO"),100, True, -1, -1, 25, 'cell', 3),\
                (("DESCRIPCION"),300, True, 4, -1, 25, 'cell', 4),\
                (("IMPORTE"),100, True, 5, -1, 25, 'cell', 5),\
                (("ENTREGA"),100, True, -1, -1, 25, 'cell', 6),\
                (("DEUDA"),100, True, 6, -1, 25,'cell', 7))
                
        for col in cols:
            self.append_column(
                self._new_column(
                    col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]))

class HistoricoView(TreeView):
    def __init__(self, liststore):
        # This class represent ticketview of ticketstore
        TreeView.__init__(self)    
        self.liststore = gtk.ListStore(int, str, str, str, str, str, str, str)
        # Associates the listStore to the ListView object
        self.set_model(self.liststore)
        #self.cargaDatos(CONSULTA_BASE)

        cols = (\
                (("ID"),50, True, -1, -1, 25, 'cell', 0),\
                (("FAMILIA_FK_ID"),100, True, -1, -1, 25, 'cell', 1),\
                (("DESCRIPCION"),300, True, -1, -1, 25, 'cell', 2),\
                (("STOCK"),80, True, -1, -1, 25, 'cell', 3),\
                (("STOCK_MINIMO"),120, True, 4, -1, 25, 'cell', 4),\
                (("PRECIO_VENTA"),120, True, 5, -1, 25, 'cell', 5),\
                (("IMAGEN"),300, True, -1, -1, 25, 'cell', 6),\
                (("BOTONERA_FK_ID"),80, True, 6, -1, 25,'cell', 7))
                
        for col in cols:
            self.append_column(
                self._new_column(
                    col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7]))
