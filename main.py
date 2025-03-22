from typing import Dict,Optional,Tuple,List
import tkinter as tk
from tkinter import ttk
from random import randint


class InsuranceAgreement:
    """
        Класс описывает объект страхового договора. 
        
        Страховой договор представляет из себя множество клиентов и страховую программу, 
        которую они подписали.
    """

    def __init__(self,prog_id: int, prog_type: str, prog_price: int, prog_time: int, prog_refund: int):
        # параметры страховой программы
        self.prog_id: int = prog_id
        self.prog_type: str = prog_type
        self.prog_price: int = prog_price
        self.prog_time: int = prog_time
        self.prog_refund: int = prog_refund
        
        self.has_clients: bool = False 
        self.client_list: list[int] = [] 
        self.case_dates: list[int] = [] 



    def add_clients(client_arr:list[int]) -> None:
        """ добавляет новых клиентов, подписавших договор на текущей итерации """
        pass

    def gen_insurance_cases() -> int:
        """
        Активирует заранее вычисленные страховые случаи
        Возвращает сумму денежной компенсации на текущей итерации по данному страховому договору
        """
        pass

    def __repr__(self):
        return f"Prog_id: {self.prog_id}, prog_type: {self.prog_type}, clients: {self.client_list}"
    

class InsuranceComp:
    """
        Класс описывает страховую компанию
    """

    def __init__(self):

        self.client_num: int = 0 

        # флаги обновления конфигурации страховых программ
        self.auto_config_updated : bool = False
        self.estate_config_updated : bool = False 
        self.med_config_updated : bool = False

        """ Переменные интерфейса в зоне ответственности InsuranceComp"""

        # Текущие значения слайдеров автостраховки (нельзя определять до построения интерфейса)
        self.auto_slider_price : tk.Variable = None
        self.auto_slider_time : tk.Variable = None   
        self.auto_slider_refund : tk.Variable = None
        self.auto_slider_base_demand : tk.Variable = None

        # id созданной в последний раз программы страховки
        self.last_program_id = 0 

        # id текущих программ страхования различных типов
        self.cur_autoprog_id = None 
        self.cur_estateprog_id = None 
        self.cur_medprog_id = None 

        # "база" клиентов
        self.progs_active: List[int] = [] 
        self.ins_agreements: Dict[int,InsuranceAgreement] = dict()

    """ Инициализация """
    
    def init_state(self) -> None:
        self.init_slider_vars()
        self.init_programs_state()

        return

    # инициализация переменных отслеживания программ страхования
    def init_programs_state(self) -> None:
        self.cur_autoprog_id = 0 
        self.cur_estateprog_id = 1 
        self.cur_medprog_id = 2 

        self.last_program_id = 2 

        # инициализация начальных страховых программ
        self.progs_active.append(self.cur_autoprog_id)
        self.ins_agreements[self.cur_autoprog_id] = self.create_ins_agr("auto",self.cur_autoprog_id)

        self.progs_active.append(self.cur_estateprog_id)
        self.ins_agreements[self.cur_estateprog_id] = self.create_ins_agr("estate",self.cur_estateprog_id)

        self.progs_active.append(self.cur_medprog_id)
        self.ins_agreements[self.cur_medprog_id] = self.create_ins_agr("med",self.cur_medprog_id)
 
        return 
    
    # инициализация текущих переменных параметров страхования
    def init_slider_vars(self) -> None: 
        # временно поставил дефолтные значения
        self.auto_slider_price = tk.Variable(value = 5)
        self.auto_slider_time = tk.Variable(value = 5)
        self.auto_slider_refund = tk.Variable(value = 50)
        self.auto_slider_base_demand = tk.Variable(value = 10)

        return 
    
    # добавление проданных страховок в клиентскую базу
    def update_client_state(self,auto_demand,estate_demand = None,med_demand = None):
        # смотрим, не обновились ли у нас условия страхования
        pass
    
    # создание страхового договора определённого типа по заданным условиям
    def create_ins_agr(self,prog_type:str,prog_id: int)-> InsuranceAgreement:
        if prog_type == "auto":
            prog_price = self.auto_slider_price.get()
            prog_refund = self.auto_slider_refund.get()
            prog_time = self.auto_slider_time.get() 

        # пока что привязаны к слайдерам от автостраховки
        elif prog_type == "estate":
            prog_price = self.auto_slider_price.get()
            prog_refund = self.auto_slider_refund.get()
            prog_time = self.auto_slider_time.get() 

        elif prog_type == "med":
            prog_price = self.auto_slider_price.get()
            prog_refund = self.auto_slider_refund.get()
            prog_time = self.auto_slider_time.get() 

        else:
            raise ValueError
        
        
        return InsuranceAgreement(prog_id,prog_type,prog_price,prog_time,prog_refund)
    

    def reset(self) -> None:
        self.reset_programs()
        self.reset_slider_vars()

    def reset_slider_vars(self) -> None:
        self.auto_config_updated = False 
        
        self.auto_slider_price.set(5)
        self.auto_slider_time.set(5)
        self.auto_slider_refund.set(50)
        self.auto_slider_base_demand.set(10)

        return 
    
    def reset_programs(self) -> None: 
        self.last_program_id = 0 
        self.client_num = 0
        self.progs_active.clear() 
        self.ins_agreements.clear()

        # создаем начальные значения после сброса
        self.init_programs_state()
        return 

    def gen_ins_cases(self) -> Dict[str,int]:
        pass 

    def add_ins_agr(ins_agr:InsuranceAgreement) -> None:
        pass 

    def delete_ins_prog(ins_prog_id:int) -> None: 
        pass 


    """ Генерация спроса, подсчёт прибыли """

    # выдает спрос на страховки различного типа с учётом текущих условий страхования

    def gen_demand(self) -> Dict[str,Tuple[int,int]]:
        # вычисление коэ-фта выгодности 
        auto_profit_coef = (self.auto_slider_refund.get()*self.auto_slider_time.get())/self.auto_slider_price.get()
        auto_add_demand = int(auto_profit_coef//10)
        auto_demand = self.auto_slider_base_demand.get() + auto_add_demand + randint(-1*auto_add_demand,5)
        auto_profit = auto_demand*self.auto_slider_price.get()


        return_object = {"auto" : (auto_demand,auto_profit)}
        self.update_client_state(auto_demand)

        return return_object

    def print_slider_values(self):
        print(f"Auto price: {self.auto_slider_price.get()}")
        print(f"Auto time: {self.auto_slider_time.get()}")
        print(f"Auto refund: {self.auto_slider_refund.get()}")
        print(f"Auto demand: {self.auto_slider_base_demand.get()}")

        return 
    

    def print_programs(self):
        print(f"Кол-во клиентов: {self.client_num}")
        for id in self.progs_active:
            print(self.ins_agreements[id])

        return


class MainController:
    """
        Главный класс, отвечающий за взаимодействие между интерфейсом и всеми остальными классами
    """
    
    def __init__(self):
        # флаги для управления итерациями
        self.modeling_started : bool = False
        self.modeling_finished : bool = False
        self.is_bankrupt : bool = False 

        # номер текущего месяца
        self.curmonth : int = 1

        # финансовые показатели
        self.networth = 100
        self.cur_profit : int = 0 
        self.cur_loss : int = 0

        # количественные показатели
        self.auto_sold : int = 0 
        self.estate_sold : int = 0 
        self.med_sold : int = 0 

        # налог
        self.tax_percent = 5
        self.tax_value = 0

        self.ins_company : InsuranceComp = InsuranceComp()

        """ Переменные графического интерфейса в зоне ответственности MainController """

        self.root : tk.Tk = None


    # процедура запуска всей программы
    def run(self) -> None: 
        
        # создание корня интерфейса
        self.init_root() 

        # инициализация страховой компании (внутри неё есть перем., используемые интерфейсом)
        self.ins_company.init_state()

        # запускаем конструктор интерфейса 
        self.init_gui()

        # Запускаем главный цикл обработки событий
        self.root.mainloop()

        return  
    
    def init_root(self) -> None:
        self.root = tk.Tk()
        self.root.title("Моделирование работы страховой компании")
        
        return

    def init_gui(self) -> None:

        # Создаем главное окно
        

        params_label = ttk.Label(self.root,text="ПАРАМЕТРЫ",font=("Arial",20))
        params_label.grid(row=0, column=0, padx=10, pady=10)

        # Инициализируем переменные, хранящие значения слайдеров для параметров договора:

        self.ins_company.init_slider_vars()

        """ Создание слайдеров настройки программ страхования """

        auto_slider_label = ttk.Label(self.root, text="АВТО:",font=("Arial",16))
        auto_slider_label.grid(row=1, column=0, padx=10, pady=10)

        # сладер стоимости страховки
        auto_slider_price = tk.Scale(self.root, from_=3, to=10, orient="horizontal",resolution =1,
                                     variable = self.ins_company.auto_slider_price,command = self.update_auto_config)
        auto_slider_price.grid(row=1, column=1, padx=10, pady=10)

        # слайдер времени действия
        auto_slider_time = tk.Scale(self.root, from_=3, to=12, orient="horizontal",resolution =1,
                                    variable = self.ins_company.auto_slider_time,command = self.update_auto_config)
        auto_slider_time.grid(row=1, column=2, padx=10, pady=10)

        # слайдер возмещения
        auto_slider_refund = tk.Scale(self.root, from_=0, to=100, orient="horizontal",resolution =1,
                                      variable = self.ins_company.auto_slider_refund,command = self.update_auto_config)
        auto_slider_refund.grid(row=1, column=3, padx=10, pady=10)

        # слайдер базового спроса автостраховки
        auto_slider_label = ttk.Label(self.root, text="Базовый спрос:",font=("Arial",12))
        auto_slider_label.grid(row=2, column=0, padx=10, pady=10)

        auto_slider_demand = tk.Scale(self.root, from_=2, to=20, orient="horizontal",resolution =1,
                                      variable = self.ins_company.auto_slider_base_demand)
        auto_slider_demand.grid(row=2, column=1, padx=10, pady=10)

        """ Создание кнопок """
        
        # Кнопка старт/итерация
        button = ttk.Button(self.root, text="Старт/Итерация", command=self.iteration_button_click)
        button.grid(row=4, column=0, columnspan=1, pady=10)

        # Кнопка стоп
        button = ttk.Button(self.root, text="СТОП", command=self.stop_button_click)
        button.grid(row=4, column=1, columnspan=1, pady=10)

        # Кнопка Reset

        button = ttk.Button(self.root, text="ЗАНОВО", command=self.reset_button_click)
        button.grid(row=4, column=2, columnspan=1, pady=10, padx = 10)
 

    """ Обработчики кнопок """
    def iteration_button_click(self) -> None: 

        if not self.modeling_started:
            print("Моделирование запущено!")
            self.modeling_started = True

        # проверяем остались ли еще итерации
        if self.modeling_finished or self.is_bankrupt:

            if self.modeling_finished:
                print("Моделирование завершено!, нажмите Reset")

            if self.is_bankrupt:
                print("Компания обанкротилась!")

        else:
            self.simulate_month()

        return 
    

    def stop_button_click(self) -> None:
        print("Пока нереализована")
        return 

    def reset_button_click(self) -> None:
        print("Reset")

        self.reset()
        return 
        

    """ Обработчики слайдеров """

    def update_auto_config(self,event):
        self.ins_company.auto_config_updated = True 
        return 

    """ Методы выполнения итерации """

    def simulate_month(self) -> None:
        self.reset_sell()
        self.reset_loss()

        sell_stats = self.ins_company.gen_demand()
        self.update_sell(sell_stats)

        # пока не работает
        loss_stats = self.ins_company.gen_ins_cases()

        self.print_state()
        self.curmonth += 1

        # временно поставил 10 - конец симуляции по времени
        if self.curmonth>10:
            print("Симуляция завершена")
            self.modeling_finished = True 

        if self.networth<0:
            print("Компания обанкротилась")
            self.is_bankrupt = True

    # обнуляет показатели связанные с продажей
    def reset_sell(self):
        self.auto_sold = 0 
        self.med_sold = 0
        self.estate_sold = 0 
        self.cur_profit = 0 

        return 

    # изменяет внутренее состояние после прибыли от продажи страховок
    def update_sell(self,sell_stats:Dict[str,Tuple[int,int]]):
        auto_sold_quantity,auto_profit = sell_stats["auto"]
        self.auto_sold = auto_sold_quantity
        self.cur_profit += auto_profit



        self.networth += self.cur_profit

    
    # изменяет внутренее состояние после убытков в виде налогов и страховых случаев
    def update_loss(self) -> None: 
        pass

    def reset_loss(self) -> None:
        self.loss = 0 
        self.tax_value = 0 

    def reset(self) -> None:

        self.networth = 100
        self.curmonth = 1 

        self.reset_sell() 
        self.reset_loss() 

        self.modeling_started = False
        self.modeling_finished = False   

        # reset страховой компании  
        self.ins_company.reset() 


    """ Методы вывода (вывод значений слайдеров, фин. и количественных показателей)"""

    def print_state(self) -> None:
        print("-----------------------------------------")
        self.print_finance() 
        self.print_quantity()
        self.print_sliders()
        self.ins_company.print_programs()
        print("-----------------------------------------")


    def print_finance(self) -> None:
        print(f"Текущий месяц: {self.curmonth}")

        print(f"Капитал: {self.networth}")
        print(f"Прибыль: {self.cur_profit}")
        print(f"Убыток: {self.cur_loss}")

        return 

    def print_sliders(self) -> None:
        self.ins_company.print_slider_values()
        return 
    
    # вывод количества проданных страховок различного типа
    def print_quantity(self) -> None:
        print(f"Количество проданных автостраховок {self.auto_sold}")

        return 


main_controller = MainController()

main_controller.run() 

