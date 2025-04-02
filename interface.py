import sys
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
        self.tax_entry : ttk.Entry = None
        self.curmonth_entry : ttk.Entry = None

        # поля вывода количества страховых случаев
        self.auto_ins_cases_entry : ttk.Entry = None
        self.med_ins_cases_entry : ttk.Entry = None
        self.estate_ins_cases_entry : ttk.Entry = None


        """ Константные переменные интерфейса """
        self.price_slider_len = 150
        self.time_slider_len = 150 
        self.refund_slider_len = 200

        self.common_label_font = ("Arial",12)
        self.large_label_font = ("Arial",20)

        """ Переменные графического интерфейса """

        # Текущие значения слайдеров автостраховки (нельзя определять до построения интерфейса, поэтому None)
        self.auto_slider_price : tk.Variable = None
        self.auto_slider_time : tk.Variable = None
        self.auto_slider_refund : tk.Variable = None

        # параметры медстраховки
        self.med_slider_price : tk.Variable = None
        self.med_slider_time : tk.Variable = None
        self.med_slider_refund : tk.Variable = None

        # параметры страхования недвижимости
        self.estate_slider_price : tk.Variable = None
        self.estate_slider_time : tk.Variable = None
        self.estate_slider_refund : tk.Variable = None
        

        # прочие параметры моделирования

        # время моделирования   
        self.modeling_duration : tk.Variable = None

        # вероятность возникновения страхового случая
        self.insurance_prob : tk.Variable = None 


        # базовый спрос на все виды страховок
        self.base_demand : tk.Variable = None

        # текст кнопки СТАРТ/итерация (может меняться в зависимости от состояния моделирования)
        self.iter_button_text : tk.StringVar = None
        self.to_the_end_button_text : tk.StringVar = None 

        # процент налога
        self.tax_percent : tk.Variable = None

    


    # процедура запуска всей программы
    def run(self) -> None: 
        
        # создание корня интерфейса
        self.init_root() 

        # установка начальных значений переменных интерфейса
        self.init_interface_vars()

        # запускаем конструктор интерфейса 
        self.init_gui()

        # инициализация внутреннего состояния эксперимента
        self.experiment.init_state()

        # Запускаем главный цикл обработки событий
        self.root.mainloop()

        return  
    
    def init_root(self) -> None:
        self.root = tk.Tk()
        self.root.title("Моделирование работы страховой компании")
        return

    def init_interface_vars(self) -> None:
        
        
        # установка начальных значений слайдеров
        self.auto_slider_price = tk.Variable(value = 5)
        self.auto_slider_time = tk.Variable(value = 5)
        self.auto_slider_refund = tk.Variable(value = 50)

        self.med_slider_price = tk.Variable(value = 2)
        self.med_slider_time = tk.Variable(value = 5)
        self.med_slider_refund = tk.Variable(value = 10)

        self.estate_slider_price = tk.Variable(value = 7)
        self.estate_slider_time = tk.Variable(value = 10)
        self.estate_slider_refund = tk.Variable(value = 60)

        # установка начальных значений прочих параметров моделирования
        self.insurance_prob = tk.Variable(value = 7)
        self.tax_percent = tk.Variable(value = 10)
        self.modeling_duration = tk.Variable(value = 12)
        self.base_demand = tk.Variable(value = 10)

        self.init_button_vars()

        return


    def init_sliders(self) -> None: 
        # устанавливаем слайдеры автостраховки 
        self.init_auto_sliders()

        # устанавливаем слайдеры медстраховки
        self.init_med_sliders()

        # устанавливаем слайдеры страховки на недвижимость 
        self.init_estate_sliders()

        """ Установка слайдеров на остальные виды страховки """

        # базовый спрос на все виды страховок
        demand_label = ttk.Label(self.root, text = "Базовый спрос на все виды страховок в ед.:", font=self.common_label_font)
        demand_label.grid(row=4, column=0, padx=10, pady=10)

        # слайдер базового спроса на все виды страховок
        demand_slider = tk.Scale(self.root, from_=2, to=20, orient="horizontal",resolution =1,command = self.update_base_demand,
                                      variable = self.base_demand)
        demand_slider.grid(row=4, column=1, padx=10, pady=10)


        # вероятность страхового случая
        insurance_prob_label = ttk.Label(self.root, text = "Вероятность страхового случая в процентах:", font=self.common_label_font)
        insurance_prob_label.grid(row=5, column=0, padx=10, pady=10)

        # слайдер регулировки вероятности возникновения страховых случаев 
        insurance_prob_slider = tk.Scale(self.root, from_ = 4,to = 25,orient="horizontal",resolution = 1,
                                       variable = self.insurance_prob,command = self.update_insurance_prob)
        insurance_prob_slider.grid(row=5, column=1, padx=10, pady=10)

        # налог
        tax_label = ttk.Label(self.root, text = "Налог в процентах:", font=self.common_label_font)
        tax_label.grid(row=6, column=0, padx=10, pady=10)

        # слайдер регулировки налога
        tax_slider = tk.Scale(self.root, from_ = 4,to = 20,orient="horizontal",resolution = 1,
                                       variable = self.tax_percent,command = self.update_tax)
        tax_slider.grid(row=6, column=1, padx=10, pady=10)


        modeling_label = ttk.Label(self.root, text = "Срок  моделирования (в мес.):", font=self.common_label_font)
        modeling_label.grid(row=7, column=0, padx=10, pady=10)

        # слайдер регулировки срока моделирования
        modeling_slider = tk.Scale(self.root, from_ = 8,to = 24,orient="horizontal",resolution = 1,
                                    variable = self.modeling_duration, command = self.update_modeling_duration)
        modeling_slider.grid(row=7, column=1, padx=10, pady=10)

        return 
    
    # установка слайдеров с параметрами автострахования
    def init_auto_sliders(self) -> None:
        # надпись "АВТОСТРАХОВКА:"
        auto_slider_label = ttk.Label(self.root, text="АВТОСТРАХОВКА:",font=("Arial",16))
        auto_slider_label.grid(row=1, column=0, padx=10, pady=10)

        # сладер стоимости автостраховки
        auto_slider_price = tk.Scale(self.root, from_=3, to=10, length = self.price_slider_len,orient="horizontal",
                                     label = "цена в у.е.д.",resolution =1,
                                     variable = self.auto_slider_price,command = self.update_auto_config)
        auto_slider_price.grid(row=1, column=1, padx=10, pady=10)

        # слайдер времени действия
        auto_slider_time = tk.Scale(self.root, from_=3, to=12, length = self.time_slider_len, orient="horizontal",
                                    label = "время в мес.",resolution =1,
                                    variable = self.auto_slider_time,command = self.update_auto_config)
        auto_slider_time.grid(row=1, column=2, padx=10, pady=10)

        # слайдер возмещения
        auto_slider_refund = tk.Scale(self.root, from_=10, to=75, length = self.refund_slider_len, orient="horizontal",
                                      label = "макс.возвр. у.е.д.",resolution =1,
                                      variable = self.auto_slider_refund,command = self.update_auto_config)
        auto_slider_refund.grid(row=1, column=3, padx=10, pady=10)

        

        return 

    # установка сладеров с параметрами медстрахования
    def init_med_sliders(self) -> None:
        # надпись "МЕД"
        med_slider_label = ttk.Label(self.root, text="МЕДИЦИНА:", font=("Arial", 16))
        med_slider_label.grid(row=2, column=0, padx=10, pady=10)

        # слайдер стоимости страховки
        med_slider_price = tk.Scale(self.root, from_=1, to=4, length=self.price_slider_len, orient="horizontal",
                                  label="цена в у.е.д.", resolution=1,
                                  variable=self.med_slider_price, command=self.update_med_config)
        med_slider_price.grid(row=2, column=1, padx=10, pady=10)

        # слайдер времени действия
        med_slider_time = tk.Scale(self.root, from_=1, to=12, length=self.time_slider_len, orient="horizontal",
                                 label="время в мес.", resolution=1,
                                 variable=self.med_slider_time, command=self.update_med_config)
        med_slider_time.grid(row=2, column=2, padx=10, pady=10)

        # слайдер возмещения
        med_slider_refund = tk.Scale(self.root, from_=5, to=15, length=self.refund_slider_len, orient="horizontal",
                                   label="макс.возвр. в у.е.д.", resolution=1,
                                   variable=self.med_slider_refund, command=self.update_med_config)
        med_slider_refund.grid(row=2, column=3, padx=10, pady=10)

        return

    # установка слайдеров с параметрами страхования недвижимости
    def init_estate_sliders(self) -> None:
        # надпись "СТРАХОВАНИЕ НЕДВИЖИМОСТИ:"
        estate_slider_label = ttk.Label(self.root, text="СТРАХОВАНИЕ НЕДВИЖИМОСТИ:", font=("Arial", 16))
        estate_slider_label.grid(row=3, column=0, padx=10, pady=10)
        
        # слайдер стоимости страховки
        estate_slider_price = tk.Scale(self.root, from_=5, to=13, length=self.price_slider_len, orient="horizontal",
                                  label="цена в у.е.д.", resolution=1,
                                  variable=self.estate_slider_price, command=self.update_estate_config)
        estate_slider_price.grid(row=3, column=1, padx=10, pady=10)
        
        # слайдер времени действия
        estate_slider_time = tk.Scale(self.root, from_=6, to=18, length=self.time_slider_len, orient="horizontal",
                                 label="время в мес.", resolution=1,
                                 variable=self.estate_slider_time, command=self.update_estate_config)
        estate_slider_time.grid(row=3, column=2, padx=10, pady=10)
        
        # слайдер возмещения
        estate_slider_refund = tk.Scale(self.root, from_=25, to=100, length=self.refund_slider_len, orient="horizontal",
                                      label="макс.возвр. в у.е.д.", resolution=1,
                                      variable=self.estate_slider_refund, command=self.update_estate_config)
        estate_slider_refund.grid(row=3, column=3, padx=10, pady=10)    

        return 


    def init_numeric_entries(self) -> None:
        # networth_label = ttk.Label(self.root,textvariable = self.experiment.networth)
        # networth_label.grid(row = 1,column = 4,pady = 10,padx = 10)
        networth_label = ttk.Label(self.root,text="Капитал в у.е.д.",font=("Arial",12))
        networth_label.grid(row=1, column=5, padx=0, pady=0)

        self.networth_entry = ttk.Entry()
        self.networth_entry.grid(row=2,column =5,padx = 0,pady = 0)

        params_label = ttk.Label(self.root,text="Прибыль в у.е.д.",font=("Arial",12))
        params_label.grid(row=3, column=5, padx=0, pady=0)

        self.profit_entry = ttk.Entry()
        self.profit_entry.grid(row = 4,column = 5,padx = 0,pady = 0)

        params_label = ttk.Label(self.root,text="Убыток в у.е.д.",font=("Arial",12))
        params_label.grid(row=5, column=5, padx=0, pady=0)

        self.loss_entry = ttk.Entry()
        self.loss_entry.grid(row = 6,column = 5,padx = 0,pady = 0)

        params_label = ttk.Label(self.root,text="Чистая прибыль в у.е.д.",font=("Arial",12))
        params_label.grid(row=7, column=5, padx=0, pady=0)

        self.net_profit_entry = ttk.Entry()
        self.net_profit_entry.grid(row = 8,column = 5,padx = 0,pady = 0)

        tax_label = ttk.Label(self.root,text="Налог в у.е.д.",font=("Arial",12))
        tax_label.grid(row=9, column=5, padx=0, pady=0)

        self.tax_entry = ttk.Entry()
        self.tax_entry.grid(row = 10,column = 5,padx = 0,pady = 0)
        
        
        # Текущий месяц (в верху окошка)
        curmonth_label = ttk.Label(self.root,text = "Текущий месяц:",font = self.common_label_font)
        curmonth_label.grid(row = 0,column = 1,padx = 10,pady = 10)

        self.curmonth_entry = ttk.Entry()
        self.curmonth_entry.grid(row = 0,column = 2,padx = 10,pady = 10)


        # поля вывода количества страховых случаев
        auto_ins_cases_label = ttk.Label(self.root,text = "Кол-во страх. случаев (авто):",font = self.common_label_font)
        auto_ins_cases_label.grid(row = 11,column = 5,padx = 10,pady = 10)

        self.auto_ins_cases_entry = ttk.Entry()
        self.auto_ins_cases_entry.grid(row = 12,column = 5,padx = 10,pady = 10)


        med_ins_cases_label = ttk.Label(self.root,text = "Кол-во страх. случаев (мед):",font = self.common_label_font)
        med_ins_cases_label.grid(row = 13,column = 5,padx = 10,pady = 10)

        self.med_ins_cases_entry = ttk.Entry()
        self.med_ins_cases_entry.grid(row = 14,column = 5,padx = 10,pady = 10)

        estate_ins_cases_label = ttk.Label(self.root,text = "Кол-во страх. случаев (недвиж):",font = self.common_label_font)
        estate_ins_cases_label.grid(row = 15,column = 5,padx = 10,pady = 10)

        self.estate_ins_cases_entry = ttk.Entry()
        self.estate_ins_cases_entry.grid(row = 16,column = 5,padx = 10,pady = 10)
        
        
        return

    def init_buttons(self) -> None:
        # Кнопка Reset
        button = ttk.Button(self.root, text="ЗАНОВО", command=self.reset_button_click)
        button.grid(row = 8, column = 1, columnspan = 1,pady = 10,padx = 10)

        # Кнопка старт/итерация
        iter_button = ttk.Button(self.root, textvariable=self.iter_button_text, command=self.iteration_button_click)
        iter_button.grid(row=8, column=0, columnspan=1, pady=10)

        # Кнопка Выход
        exit_button = ttk.Button(self.root, text="ВЫХОД", command=self.exit_button_click)
        exit_button.grid(row=8, column=2, columnspan=1, pady=10)

        # Кнопка "до конца"
        to_the_end_button = ttk.Button(self.root, textvariable=self.to_the_end_button_text, command=self.to_the_end_button_click)
        to_the_end_button.grid(row=8, column=3, columnspan=1, pady=10)

        return 
    
    def init_button_vars(self) -> None:

        self.iter_button_text = tk.StringVar(value="СТАРТ")
        self.to_the_end_button_text = tk.StringVar(value="ДО КОНЦА")

        return 
    
    def init_separators(self) -> None:
        vert_sep = ttk.Separator(self.root, orient="vertical")
        vert_sep.grid(column=4, row=0, rowspan=7, sticky="ns",ipadx=0)

        return 
    
    def init_top_labels(self) -> None: 

        results_label = ttk.Label(self.root,text = "РЕЗУЛЬТАТЫ",font = self.large_label_font)
        results_label.grid(row = 0,column = 5,padx = 10,pady = 10)


        params_label = ttk.Label(self.root,text="ПАРАМЕТРЫ",font = self.large_label_font)
        params_label.grid(row = 0, column=0, padx=10, pady=10)

        return


    def init_gui(self) -> None:
        # Инициализация верхних надписей
        self.init_top_labels()

        # Создание слайдеров настройки программ автострахования
        self.init_sliders() 

        # создание кнопок    
        self.init_buttons()

        # создание полей вывода численных показателей
        self.init_numeric_entries()

        self.init_separators()

        # установка начальных значений числовых полей
        self.display_updated_finance()

        return 
        
    
    """ Обработчики кнопок """

    def update_auto_config(self,event):
        price = int(self.auto_slider_price.get())
        time = int(self.auto_slider_time.get())
        refund = int(self.auto_slider_refund.get())

        self.experiment.update_auto_config(price,time,refund)
        return 
    
    def update_med_config(self,event):
        price = int(self.med_slider_price.get())
        time = int(self.med_slider_time.get())
        refund = int(self.med_slider_refund.get())
    
        self.experiment.update_med_config(price,time,refund)

        return 
    
    def update_estate_config(self,event):
        price = int(self.estate_slider_price.get())
        time = int(self.estate_slider_time.get())
        refund = int(self.estate_slider_refund.get())
    
        self.experiment.update_estate_config(price,time,refund)

        return 
    

    def update_base_demand(self,event):
        demand = int(self.base_demand.get())
        self.experiment.update_base_demand(demand)

        return 
        
    def update_insurance_prob(self,event) -> None:
        self.experiment.update_insurance_prob(percent = int(self.insurance_prob.get()))

        return
    
    def update_tax(self,event) -> None:
        self.experiment.update_tax(percent = int(self.tax_percent.get()))

        return 
    
    def update_modeling_duration(self,event) -> None:
        self.experiment.modeling_duration = int(self.modeling_duration.get())

        return 

    
    def exit_button_click(self) -> None:
        
        sys.exit(0)

        return 

    def reset_button_click(self) -> None:
        print("Reset")

        # возврат слайдеров к дефолтным значениями
        self.reset_interface_vars()
        # обновление финансовых показателей и состояния страховой компании (удаление всех договоров и тд)
        self.experiment.reset()

        # обновление значений окошек с финансовыми показателями (устанавливается начальное состояние)
        self.display_updated_finance()

        # установка исходного текста кнопок
        self.reset_button_vars()
        return 
    

    def reset_interface_vars(self) -> None:
        # установка начальных значений слайдеров параметров страхования
        self.auto_slider_price.set(5)
        self.auto_slider_time.set(5)
        self.auto_slider_refund.set(50)

        self.med_slider_price.set(2)
        self.med_slider_time.set(5)
        self.med_slider_refund.set(10)

        self.estate_slider_price.set(7)
        self.estate_slider_time.set(10)
        self.estate_slider_refund.set(60)
    
        # установка начальных значений прочих параметров моделирования
        self.insurance_prob.set(7)
        self.tax_percent.set(10)
        self.modeling_duration.set(12)
        self.base_demand.set(10)

        self.reset_button_vars()
        
    
    def reset_button_vars(self) -> None:

        self.iter_button_text.set("СТАРТ")
        self.to_the_end_button_text.set("ДО КОНЦА")

        return 

    def to_the_end_button_click(self) -> None:

        self.experiment.to_the_end()

        self.display_updated_finance()

        # меняем текст кнопки "до конца" в зависимости от состояния моделирования
        if self.experiment.is_bankrupt:
            self.to_the_end_button_text.set("Банкрот")
        else:
            self.to_the_end_button_text.set("УСПЕХ")

        return 
    
    
    def iteration_button_click(self) -> None: 

        # проверка на завершение моделирования
        self.experiment.iteration_button_click()
        self.display_updated_finance()

        # меняем текст кнопки итерации в зависимости от состояния моделирования
        if self.experiment.is_bankrupt:
            self.iter_button_text.set("Банкрот")

        elif self.experiment.modeling_finished:
            self.iter_button_text.set("УСПЕХ")

        else:
            self.iter_button_text.set("Сделать шаг")

        return 
    
    """ Обновление числовых полей после итерации """
    def display_updated_finance(self) -> None:
        self.refresh_networth_entry()
        self.refresh_profit_entry()
        self.refresh_loss_entry()
        self.refresh_net_profit_entry()
        self.refresh_tax_entry()
        self.refresh_curmonth_entry()
        self.refresh_ins_cases_entries()    

        return 

    def refresh_networth_entry(self) -> None:
        # сразу делим на 50, чтобы наверняка удалить всё число
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
    
    def refresh_tax_entry(self) -> None:
        self.tax_entry.delete(0,50)
        self.tax_entry.insert(0,str(self.experiment.tax_value))


    def refresh_curmonth_entry(self) -> None:
        self.curmonth_entry.delete(0,50)
        self.curmonth_entry.insert(0,str(self.experiment.curmonth-1))

        return 
    
    def refresh_ins_cases_entries(self) -> None:
        self.auto_ins_cases_entry.delete(0,50)
        self.auto_ins_cases_entry.insert(0,str(self.experiment.cur_auto_ins_cases))

        self.med_ins_cases_entry.delete(0,50)
        self.med_ins_cases_entry.insert(0,str(self.experiment.cur_med_ins_cases))
        
        self.estate_ins_cases_entry.delete(0,50)
        self.estate_ins_cases_entry.insert(0,str(self.experiment.cur_estate_ins_cases))
        return 

