


import tkinter as tk

from typing import Dict,Tuple
from experiment import Experiment
from tkinter import ttk



class Interface:
    """
        Главный класс, отвечающий за взаимодействие между интерфейсом и всеми остальными классами
    """
    
    def __init__(self):

        self.experiment : Experiment = Experiment()
        
        # корень к которому все элементы цепляются
        self.root : tk.Tk = None

        # поля вывода финансовых показателей
        self.networth_entry : ttk.Entry = None
        self.profit_entry : ttk.Entry = None
        self.loss_entry: ttk.Entry = None
        self.net_profit_entry : ttk.Entry = None 
        

        """ Переменные графического интерфейса """

        # Текущие значения слайдеров автостраховки (нельзя определять до построения интерфейса, поэтому None)
        self.auto_slider_price : tk.Variable = None
        self.auto_slider_time : tk.Variable = None
        self.auto_slider_refund : tk.Variable = None
        self.auto_slider_base_demand : tk.Variable = None

        # вероятность возникновения страхового случая
        self.case_percent : tk.Variable = None 


    # процедура запуска всей программы
    def run(self) -> None: 
        
        # создание корня интерфейса
        self.init_root() 

        self.init_slider_vars()

        # запускаем конструктор интерфейса 
        self.init_gui()

        self.experiment.init_state()

        # Запускаем главный цикл обработки событий
        self.root.mainloop()

        return  
    
    def init_root(self) -> None:
        self.root = tk.Tk()
        self.root.title("Моделирование работы страховой компании")
        return

    def init_slider_vars(self) -> None:
        self.case_percent = tk.Variable(value = 7)

        self.auto_slider_price = tk.Variable(value = 5)
        self.auto_slider_time : tk.Variable = tk.Variable(value = 5)
        self.auto_slider_refund : tk.Variable = tk.Variable(value = 50)
        self.auto_slider_base_demand : tk.Variable = tk.Variable(value = 10)

        return


    def init_sliders(self) -> None: 
        auto_slider_label = ttk.Label(self.root, text="АВТО:",font=("Arial",16))
        auto_slider_label.grid(row=1, column=0, padx=10, pady=10)

        # сладер стоимости страховки
        auto_slider_price = tk.Scale(self.root, from_=3, to=10, orient="horizontal",label = "цена",resolution =1,
                                     variable = self.auto_slider_price,command = self.update_auto_config)
        auto_slider_price.grid(row=1, column=1, padx=10, pady=10)

        # слайдер времени действия
        auto_slider_time = tk.Scale(self.root, from_=3, to=12, orient="horizontal",label = "время",resolution =1,
                                    variable = self.auto_slider_time,command = self.update_auto_config)
        auto_slider_time.grid(row=1, column=2, padx=10, pady=10)

        # слайдер возмещения
        auto_slider_refund = tk.Scale(self.root, from_=0, to=100, orient="horizontal",label = "возврат",resolution =1,
                                      variable = self.auto_slider_refund,command = self.update_auto_config)
        auto_slider_refund.grid(row=1, column=3, padx=10, pady=10)

        # слайдер базового спроса автостраховки
        auto_slider_label = ttk.Label(self.root, text="Базовый спрос:",font=("Arial",12))
        auto_slider_label.grid(row=2, column=0, padx=10, pady=10)

        auto_slider_demand = tk.Scale(self.root, from_=2, to=20, orient="horizontal",resolution =1,
                                      variable = self.auto_slider_base_demand)
        auto_slider_demand.grid(row=2, column=1, padx=10, pady=10)

        # слайдер регулировки вероятности возникновения страховых случаев 
        
        case_percent_label = ttk.Label(self.root, text = "Вероятность страхового случая",font=("Arial",12))
        case_percent_label.grid(row=3, column=0, padx=10, pady=10)

        case_percent_slider = tk.Scale(self.root, from_ = 4,to = 20,orient="horizontal",resolution = 1,
                                       variable = self.case_percent)
        case_percent_slider.grid(row=3, column=1, padx=10, pady=10)

        return 
    

    def init_numeric_entries(self) -> None:
        # networth_label = ttk.Label(self.root,textvariable = self.experiment.networth)
        # networth_label.grid(row = 1,column = 4,pady = 10,padx = 10)
        params_label = ttk.Label(self.root,text="Капитал",font=("Arial",12))
        params_label.grid(row=1, column=4, padx=0, pady=0)

        self.networth_entry = ttk.Entry()
        self.networth_entry.grid(row=2,column =4,padx = 0,pady = 0)


        params_label = ttk.Label(self.root,text="Прибыль",font=("Arial",12))
        params_label.grid(row=3, column=4, padx=0, pady=0)

        self.profit_entry = ttk.Entry()
        self.profit_entry.grid(row = 4,column = 4,padx = 0,pady = 0)



        params_label = ttk.Label(self.root,text="Убыток",font=("Arial",12))
        params_label.grid(row=5, column=4, padx=0, pady=0)

        self.loss_entry = ttk.Entry()
        self.loss_entry.grid(row = 6,column = 4,padx = 0,pady = 0)

        params_label = ttk.Label(self.root,text="Чистая прибыль",font=("Arial",12))
        params_label.grid(row=7, column=4, padx=0, pady=0)

        self.net_profit_entry = ttk.Entry()
        self.net_profit_entry.grid(row = 8,column = 4,padx = 0,pady = 0)
        
        return

    def init_buttons(self) -> None:
        # Кнопка Reset
        button = ttk.Button(self.root, text="ЗАНОВО", command=self.reset_button_click)
        button.grid(row = 4, column = 2, columnspan = 1,pady = 10,padx = 10)

        # Кнопка старт/итерация
        button = ttk.Button(self.root, text="Старт/Итерация", command=self.iteration_button_click)
        button.grid(row=4, column=0, columnspan=1, pady=10)
        return 

    def init_gui(self) -> None:

        # подпись Параметры
        params_label = ttk.Label(self.root,text="ПАРАМЕТРЫ",font=("Arial",20))
        params_label.grid(row=0, column=0, padx=10, pady=10)

        # Создание слайдеров настройки программ автострахования
        self.init_sliders() 

        # создание кнопок    
        self.init_buttons()

        # создание полей вывода численных показателей
        self.init_numeric_entries()

        return 
        
 
    """ Обработчики кнопок """

    def update_auto_config(self,event):
        price = int(self.auto_slider_price.get())
        time = int(self.auto_slider_time.get())
        refund = int(self.auto_slider_refund.get())
        demand = int(self.auto_slider_base_demand.get())

        self.experiment.update_auto_config(price,time,refund,demand)
    

    def reset_slider_vars(self) -> None:
        self.auto_slider_price.set(5)
        self.auto_slider_time.set(5)
        self.auto_slider_refund.set(50)
        self.auto_slider_base_demand.set(10)

        self.case_percent.set(7)

        self.experiment.reset_modeling_params()
        return 
    
    def reset_button_click(self) -> None:
        print("Reset")

        # возврат слайдеров к дефолтным значениями
        self.reset_slider_vars()

        # обновление финансовых показателей и состояния страховой компании (удалиение всех договоров и тд)
        self.experiment.reset()

        # обновление значений окошек с финансовыми показателями
        self.display_updated_finance()

        return 
    
    def iteration_button_click(self) -> None: 
        self.experiment.iteration_button_click()
        self.display_updated_finance()
        return 
    
    """ Обновление числовых полей """

    def display_updated_finance(self) -> None:
        self.refresh_networth_entry()
        self.refresh_profit_entry()
        self.refresh_loss_entry()
        self.refresh_net_profit_entry()

        return 

    def refresh_networth_entry(self) -> None:
        # сразу делим на 50, чтобы наверняка удалить все число
        self.networth_entry.delete(0,50)
        self.networth_entry.insert(0,str(self.experiment.networth))

        return
    
    def refresh_profit_entry(self) -> None:
        # сразу делим на 50, чтобы наверняка удалить всё число
        self.profit_entry.delete(0,50)
        self.profit_entry.insert(0,str(self.experiment.cur_profit))

        return 
    
    def refresh_loss_entry(self) -> None:
        self.loss_entry.delete(0,50)
        self.loss_entry.insert(0,str(self.experiment.cur_loss))

        return 
    
    def refresh_net_profit_entry(self) -> None:
        self.net_profit_entry.delete(0,50)
        self.net_profit_entry.insert(0,str(self.experiment.cur_net_profit))

        return 

if __name__ == "__main__":
    pass 
