import tkinter as tk
from tkinter import ttk
from tkinter import Button
from tkinter import simpledialog
from tkinter import messagebox
import tkinter.simpledialog as sd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import logging
import threading
from threading import Thread
import os
import glob
import inspect
import time

from Config import *
import Config
from Simulation import Simulation

class Gui(Thread):
    def __init__(self):
        super().__init__()
        self.reports = []
        self.simulation = None
        self.graphing_thread = None
        
    def run(self):
        Config.gui_running = True
        Config.simulation_running = False
        
        self.root = tk.Tk()
        self.root.title("Scheduling simulation")

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=1, sticky='s')

        self.options = glob.glob('./Schedulers/*.py')
        self.options = [os.path.basename(f)[:-3] for f in self.options]
        self.options = [f for f in self.options if f != 'Method']
    
        self.selected_scheduling = tk.StringVar(self.root)
        self.selected_scheduling.set(self.options[0])
        
        self.combo = ttk.Combobox(self.root, textvariable=self.selected_scheduling, state="readonly")
        self.combo['values'] = self.options
        self.combo.bind('<<ComboboxSelected>>', self.on_combo_change)
        self.combo.grid(row=0, column=1)
        self.selected_schedulers = []
        
        self.selected_type = tk.StringVar(button_frame)
        self.selected_type.set(order_type_names[0])

        option_menu = tk.OptionMenu(button_frame, self.selected_type, *order_type_names)
        option_menu.grid(row=0, column=0)

        add_scheduler_button = Button(button_frame, text="Add scheduler", command=self.add_scheduler)
        add_scheduler_button.grid(row=1, column=0, sticky='ew')
        
        remove_scheduler_button = Button(button_frame, text="Remove scheduler", command=self.remove_scheduler)
        remove_scheduler_button.grid(row=2, column=0, sticky='ew')

        start_simulation_button = Button(button_frame, text="Start simulation", command=self.start_simulation)
        start_simulation_button.grid(row=3, column=0, sticky='ew')

        stop_simulation_button = Button(button_frame, text="Stop simulation", command=self.stop_simulation)
        stop_simulation_button.grid(row=4, column=0, sticky='ew')
        
        stop_simulation_button = Button(button_frame, text="Change configuration", command=self.configuration_menu)
        stop_simulation_button.grid(row=5, column=0, sticky='ew')

        self.fig = Figure(figsize=(10, 5))
        self.ax_stock = self.fig.add_subplot(121)
        self.ax_tn = self.fig.add_subplot(122)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=2)

        self.root.mainloop()
        Config.gui_running = False

        if self.simulation is not None:
            self.simulation.join()

        if self.graphing_thread is not None:
            self.graphing_thread.join()
        
    def draw_plot(self):
        while Config.simulation_running:
            self.ax_stock.clear()
            self.ax_tn.clear()
            
            lines_tn = []
            
            for i in range(len(Config.methods)):
                if i < len(self.reports):
                    lines_tn = self.reports[i].draw(Config.methods[i].name, self.ax_stock, self.ax_tn, None, lines_tn, order_type_map[self.selected_type.get()])
                else:
                    logging.error("Reports index out of range")

            self.ax_stock.set_title("Stock")
            self.ax_stock.set_xlabel("Time (min)")
            self.ax_stock.set_ylabel("Stock (pieces)")
            self.ax_stock.set_ylim(bottom=0)  # Ensure y-axis starts at 0
            self.ax_stock.grid()

            self.ax_tn.set_xlim([0, 100])
            self.ax_tn.set_title("Tardiness")

            self.ax_tn.set_xlabel("% of orders")
            self.ax_tn.set_ylabel("Tardiness (min)")
            self.ax_tn.set_yscale('log')
            self.ax_tn.grid()

            self.fig.subplots_adjust(hspace=0.5)
            self.fig.legend(handles=lines_tn, loc='upper right')
            # self.fig.legend(handles=[self.line_rr, self.line_tn], loc='upper right')
            self.canvas.draw()
    
    def start_simulation(self):
        if not Config.simulation_running:
            Config.simulation_running = True
            Config.methods = []
            
            for name in self.selected_schedulers:
                try:
                    cls = globals()[name]
                except KeyError:
                    messagebox.showerror("ERROR", f"import {name} in  Config.py")
                    return

                args = inspect.signature(cls.__init__).parameters
                
                if len(args) > 1:
                    arg_values = {}
                    for arg in list(args.keys())[1:]:
                        value = simpledialog.askstring("Input", f"Enter value for {arg} in {name}:")
                        arg_values[arg] = value
                    instance = cls(**arg_values)
                else:
                    instance = cls()
                    
                Config.methods.append(instance)
            
            self.graphing_thread = Thread(target=self.draw_plot)
            self.graphing_thread.start()
            
            time.sleep(0.1)

            self.reports = []
            self.simulation = Simulation(self.reports).start()
    
    def stop_simulation(self):
        if Config.simulation_running:
            Config.simulation_running = False
            self.ax_stock.clear()
            self.ax_tn.clear()
            self.canvas.draw()
            
    def add_scheduler(self):
        selected = self.selected_scheduling.get()
        if not selected.endswith("*"):
            self.selected_schedulers.append(self.selected_scheduling.get())
            self.selected_scheduling.set(self.selected_scheduling.get() + "*")
            self.on_combo_change(None)
    
    def remove_scheduler(self):
        selected = self.selected_scheduling.get()[:-1]
        if selected in self.selected_schedulers:
            self.selected_schedulers.remove(selected)
            self.selected_scheduling.set(selected)
            self.on_combo_change(None)
            
    def configuration_menu(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Configuration")
        dialog.grab_set()

        self.tree = ttk.Treeview(dialog, columns=('Name',), show='headings')
        self.tree.heading('Name', text='Name')

        for config in Config.configurations:
            self.tree.insert('', 'end', values=(config.name,))

        self.tree.pack()

        button_frame = tk.Frame(dialog)
        button_frame.pack(fill='x')

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Edit", command=self.change_configuration).grid(row=0, column=0, sticky='ew')
        tk.Button(button_frame, text="Close", command=dialog.destroy).grid(row=0, column=1, sticky='ew')
        
    def change_configuration(self):
        selected_item_id = self.tree.selection()[0]
        configuration_name = self.tree.item(selected_item_id, 'values')[0]
        
        configuration = None
        
        for c in Config.configurations:
            if c.name == configuration_name:
                configuration = c
                break
        
        dialog = tk.Toplevel(self.root)
        self.render_tables(dialog, configuration)
        
    
    def render_tables(self, dialog, configuration):
        dialog.title(f"Configuration of {configuration.name}")
        dialog.grab_set()
        
        #########################
        #   TRANSITION TABLE    #
        #########################
        
        tk.Label(dialog, text="Transition table:").grid(row=0, column=0)
        
        transition_tree = self.render_transition_table(dialog, configuration)
        transition_tree.grid(row=1, column=0, sticky='nsew')
        
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=2, column=0, sticky='ew') 

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Add", command=lambda: self.add_transition_row(dialog, configuration, transition_tree)).grid(row=1, column=0, sticky='ew')
        tk.Button(button_frame, text="Edit", command=lambda: self.edit_transition_row(dialog, configuration, transition_tree)).grid(row=1, column=1, sticky='ew')
        tk.Button(button_frame, text="Remove ", command=lambda: self.remove_transition_row(dialog, configuration, transition_tree)).grid(row=1, column=2, sticky='ew')
        
        #########################
        #     RUNTIME TABLE     #
        #########################
        
        tk.Label(dialog, text="Runtime table:").grid(row=3, column=0)
        
        runtime_tree = self.render_runtime_table(dialog, configuration)
        runtime_tree.grid(row=4, column=0, sticky='nsew')
        tk.Button(dialog, text="Edit", command=lambda: self.edit_runtime_row(dialog, configuration, runtime_tree)).grid(row=5, column=0, sticky='ew')
        
        #########################
        #     ALLOWED TABLE     #
        #########################
        
        tk.Label(dialog, text="Allowed order types:").grid(row=0, column=1)
        
        allowed_tree = self.render_allowed_table(dialog, configuration)
        allowed_tree.grid(row=1, column=1, sticky='nsew')
        
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=2, column=1, sticky='ew') 

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Add", command=lambda: self.add_can_do_list_row(dialog, configuration, allowed_tree)).grid(row=1, column=0, sticky='ew')
        tk.Button(button_frame, text="Remove", command=lambda: self.remove_can_do_list_row(dialog, configuration, allowed_tree)).grid(row=1, column=1, sticky='ew')
        
        #########################
        #     PRIORITY QUEUE    #
        #########################
        
        tk.Label(dialog, text="Allowed order types:").grid(row=3, column=1)
        
        priority_tree = self.render_priority_list(dialog, configuration)
        priority_tree.grid(row=4, column=1, sticky='nsew')
        
        button_frame = tk.Frame(dialog)
        button_frame.grid(row=5, column=1, sticky='ew') 

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        tk.Button(button_frame, text="Up", command=lambda: self.higher_priority(dialog, configuration, priority_tree)).grid(row=1, column=0, sticky='ew')
        tk.Button(button_frame, text="Down", command=lambda: self.lower_priority(dialog, configuration, priority_tree)).grid(row=1, column=1, sticky='ew')
        
        tk.Button(dialog, text="Close", command=dialog.destroy).grid(row=6, column=0, sticky='ew')
    
    def render_transition_table(self, dialog, configuration):
        tree = ttk.Treeview(dialog, columns=('From', 'To', 'Cost'), show='headings')
        tree.heading('From', text='From')
        tree.heading('To', text='To')
        tree.heading('Cost', text='Cost')

        for key, value in configuration.transitions.items():
            tree.insert('', 'end', values=(key[0].name, key[1].name, value))
            
        return tree
    
    def add_transition_row(self, old_dialog, configuration, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Transition")
        dialog.grab_set()

        selected_type1_name = tk.StringVar(dialog)
        selected_type1_name.set(Config.order_type_names[0])
        type_menu = tk.OptionMenu(dialog, selected_type1_name, *Config.order_type_names)
        type_menu.grid(row=0, column=0)
        selected_type2_name = tk.StringVar(dialog)
        selected_type2_name.set(Config.order_type_names[0])
        type_menu = tk.OptionMenu(dialog, selected_type2_name, *Config.order_type_names)
        type_menu.grid(row=0, column=1)
        cost_entry = tk.Entry(dialog)
        cost_entry.grid(row=0, column=2)

        tk.Button(dialog, text="OK", command=lambda: self.add_transition(old_dialog, dialog, configuration, Config.order_type_map[selected_type1_name.get()], Config.order_type_map[selected_type2_name.get()], int(cost_entry.get()), tree)).grid(row=1, column=0, columnspan=3)

    def add_transition(self, old_dialog, dialog, configuration, from_value, to_value, cost, tree):
        configuration.transitions[(from_value, to_value)] = cost
        tree.insert('', 'end', values=(from_value.name, to_value.name, cost))
        self.render_tables(old_dialog, configuration)
        dialog.destroy()
    
    def edit_transition_row(self, old_dialog, configuration, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit transition entry")
        dialog.grab_set()

        tk.Label(dialog, text="Enter the new cost for the transition:").grid(row=0, column=0)
        cost_entry = tk.Entry(dialog)
        cost_entry.grid(row=1, column=0)

        selected_item = tree.selection()
        if not selected_item:
            return  # No item is selected

        values = tree.item(selected_item[0], 'values')
        from_value, to_value, _ = values

        tk.Button(dialog, text="OK", command=lambda: self.edit_transition(old_dialog, dialog, configuration, Config.order_type_map[from_value], Config.order_type_map[to_value], int(cost_entry.get()), tree)).grid(row=2, column=0, columnspan=3)
    
    def edit_transition(self, old_dialog, dialog, configuration, from_value, to_value, cost, tree):
        self.remove_transition_row(configuration, tree)
        configuration.transitions[(from_value, to_value)] = cost
        
        tree.insert('', 'end', values=(from_value.name, to_value.name, cost))
        self.render_tables(old_dialog, configuration)
        dialog.destroy()
        
    def remove_transition_row(self, old_dialog, configuration, tree):
        selected_item = tree.selection()
        if not selected_item:
            return  # No item is selected

        values = tree.item(selected_item[0], 'values')
        from_value, to_value, cost = values

        self.remove_transition(old_dialog, configuration, Config.order_type_map[from_value], Config.order_type_map[to_value], tree)

    def remove_transition(self, old_dialog, configuration, from_value, to_value, tree):
        del configuration.transitions[(from_value, to_value)]
        for item in tree.get_children():
            values = tree.item(item, 'values')
            if values[0] == from_value.name and values[1] == to_value.name:
                tree.delete(item)
                break
        self.render_tables(old_dialog, configuration)
            
    def render_runtime_table(self, dialog, configuration):
        tree = ttk.Treeview(dialog, columns=('Order type', '# units / day'), show='headings')
        tree.heading('Order type', text='Order type')
        tree.heading('# units / day', text='# units / day')

        for key, value in configuration.runtime.items():
            tree.insert('', 'end', values=(key.name, value))
            
        return tree
    
    def edit_runtime_row(self, old_dialog, configuration, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit runtime entry")
        dialog.grab_set()

        selected_item = tree.selection()
        if not selected_item:
            print(selected_item)
            return  # No item is selected
        
        tk.Label(dialog, text="Enter the new runtime value:").grid(row=0, column=0)
        cost_entry = tk.Entry(dialog)
        cost_entry.grid(row=1, column=0)

        values = tree.item(selected_item[0], 'values')
        tk.Button(dialog, text="OK", command=lambda: self.edit_runtime(old_dialog, dialog, configuration, Config.order_type_map[values[0]], int(cost_entry.get()), tree)).grid(row=2, column=0, columnspan=3)
    
    def edit_runtime(self, old_dialog, dialog, configuration, type, cost, tree):
        self.remove_runtime_row(old_dialog, configuration, tree)
        configuration.runtime[type] = cost
        
        tree.insert('', 'end', values=(type.name, cost))
        self.render_tables(old_dialog, configuration)
        dialog.destroy()
        
    def remove_runtime_row(self, old_dialog, configuration, tree):
        selected_item = tree.selection()
        if not selected_item:
            return  # No item is selected

        values = tree.item(selected_item[0], 'values')
        self.remove_runtime(old_dialog, configuration, Config.order_type_map[values[0]], tree)

    def remove_runtime(self, old_dialog, configuration, type, tree):
        # Remove the transition from the configuration
        del configuration.runtime[type]

        # Remove the transition from the tree
        for item in tree.get_children():
            values = tree.item(item, 'values')
            if values[0] == type.name:
                tree.delete(item)
                break
            
        self.render_tables(old_dialog, configuration)
            
    def render_allowed_table(self, dialog, configuration):
        tree = ttk.Treeview(dialog, columns=('Type'), show='headings')
        tree.heading('Type', text='Type')
        
        for value in configuration.can_do_list:
            tree.insert('', 'end', values=(value.name))
        
        return tree
    
    def add_can_do_list_row(self, old_dialog, configuration, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add order type")
        dialog.grab_set()

        tk.Label(dialog, text="Choose the new order type:").grid(row=0, column=0)

        selected_type_name = tk.StringVar(dialog)
        selected_type_name.set(Config.order_type_names[0])

        type_menu = tk.OptionMenu(dialog, selected_type_name, *Config.order_type_names)
        type_menu.grid(row=1, column=0)

        tk.Button(dialog, text="OK", command=lambda: self.add_can_do_list(old_dialog, dialog, configuration, Config.order_type_map[selected_type_name.get()], tree)).grid(row=2, column=0, columnspan=3)

    def add_can_do_list(self, old_dialog, dialog, configuration, type, tree):
        runtime_val = int(simpledialog.askinteger("Input", "Enter the runtime value"))
        if runtime_val is not None:
            configuration.add_type(type, runtime_val)
            tree.insert('', 'end', values=(type.name, runtime_val))
            self.render_tables(old_dialog, configuration)
            dialog.destroy()
        
    def remove_can_do_list_row(self, old_dialog, configuration, tree):
        selected_item = tree.selection()
        if not selected_item:
            return  # No item is selected

        type = tree.item(selected_item[0], 'values')

        self.remove_can_do_list(old_dialog, configuration, Config.order_type_map[type[0]], tree)

    def remove_can_do_list(self, old_dialog, configuration, type, tree):
        configuration.remove_type(type)
        for item in tree.get_children():
            values = tree.item(item, 'values')
            if values[0] == type.name:
                tree.delete(item)
                break
        self.render_tables(old_dialog, configuration)
    
    def render_priority_list(self, dialog, configuration):
        tree = ttk.Treeview(dialog, columns=('Type'), show='headings')
        tree.heading('Type', text='Type')
        
        for value in configuration.priority_list:
            tree.insert('', 'end', values=(value.name))
        
        return tree
    
    def higher_priority(self, old_dialog, configuration, tree):
        selected_id = tree.selection()[0]
        selected_index = tree.index(selected_id)

        if selected_index > 0:
            before_id = tree.get_children()[selected_index - 1]
            tree.move(selected_id, '', selected_index - 1)
            tree.move(before_id, '', selected_index)
            configuration.priority_list[selected_index], configuration.priority_list[selected_index - 1] = configuration.priority_list[selected_index - 1], configuration.priority_list[selected_index]
            
        self.render_tables(old_dialog, configuration)
        
    def lower_priority(self, old_dialog, configuration, tree):
        selected_id = tree.selection()[0]
        selected_index = tree.index(selected_id)

        if selected_index < len(configuration.priority_list):
            before_id = tree.get_children()[selected_index + 1]
            tree.move(selected_id, '', selected_index + 1)
            tree.move(before_id, '', selected_index)
            configuration.priority_list[selected_index], configuration.priority_list[selected_index + 1] = configuration.priority_list[selected_index + 1], configuration.priority_list[selected_index]
            
        self.render_tables(old_dialog, configuration)
    
    def use_new_configuration(self):
        self.root.grab_release()
    
    def on_combo_change(self, event):
        new_options = []
        for f in self.options:
            if f in self.selected_schedulers and not f.endswith('*'):
                new_options.append(f"{f}*")
            else:
                if f.endswith('*'):
                    new_options.append(f"{f[:-1]}")
                else:
                    new_options.append(f)
               
        self.combo["values"] = new_options