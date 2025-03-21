from typing import Dict,Optional,Tuple,List
import tkinter as tk
from tkinter import ttk
from random import randint


class InsuranceProgram:
    """
        Класс описывающий конфигурацию страховой программы
    """

    def __init__(self,prog_id:int,prog_type:str,time:int,price:int,max_refund:int):

        self.prog_id : int = prog_id
        self.prog_type : str = prog_type

        # три главных параметра программы
        self.time : int = time 
        self.price : int = price
        self.max_refund : int = max_refund



class InsuranceAgreement:
    """
        Класс описывает объект страхового договора. 
        
        Страховой договор представляет из себя множество клиентов и страховую программу, 
        которую они подписали.
    """

    def __init__(self,prog_id: int, prog_config:InsuranceProgram):
        self.prog_id: int = prog_id
        self.prog_type: str = prog_config.prog_type 

        self.has_clients: bool = False 
        self.client_list: list[int] = [] 
        self.case_dates: list[int] = [] 

        self.prog_config : InsuranceProgram


    def add_clients(client_arr:list[int]) -> None:
        """ добавляет новых клиентов, подписавших договор на текущей итерации """
        pass

    def gen_insurance_cases() -> int:
        """
        Активирует заранее вычисленные страховые случаи
        Возвращает сумму денежной компенсации на текущей итерации по данному страховому договору
        """
        pass
    

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
        self.active_autoprog_id = None 
        self.active_estateprog_id = None 
        self.active_medprog_id = None 

        # "база" клиентов
        self.progs_active: List[int] = [] 
        self.ins_agreements: Dict[int,InsuranceAgreement] = dict()

    """ Управление состоянием страховой компании """
    
    # инициализация переменных отслеживания программ страхования
    def init_state(self):
        self.active_autoprog_id = 0 
        self.active_estateprog_id = 1 
        self.active_medprog_id = 2 

        self.active_program_id = 2 

        self.progs_active.append(self.active_autoprog_id)
        self.progs_active.append(self.active_estateprog_id)
        self.progs_active.append(self.active_medprog_id)

        return 
    
    # инициализация текущих переменных параметров страхования
    def init_slider_vars(self): 
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
    
    
    def print_slider_values(self):
        print(f"Auto price: {self.auto_slider_price.get()}")
        print(f"Auto time: {self.auto_slider_time.get()}")
        print(f"Auto refund: {self.auto_slider_refund.get()}")
        print(f"Auto demand: {self.auto_slider_base_demand.get()}")

        return 

    def reset(self) -> None:

        # возвращение слайдеров и связанных с ними переменных в исходное положение 
        self.auto_config_updated = False

        # пока только для машин
        self.auto_slider_price.set(5)
        self.auto_slider_time.set(5)
        self.auto_slider_refund.set(50)
        self.auto_slider_base_demand.set(10)

        # обнуление конфигураций договоров
        self.last_program_id = 0 

        self.auto_config = None
        self.estate_config = None 
        self.med_config = None 

        # обнуление клиентской "базы" и всего, что с ней связано
        self.client_num = 0
        self.progs_active.clear() 
        self.ins_agreements.clear()


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
    



class MainController:
    """
        Главный класс, отвечающий за взаимодействие между интерфейсом и всеми остальными классами
    """
    
    def __init__(self):
        self.modeling_started : bool = False
        self.curmonth : int = 1

        self.cur_profit : int = 0 
        self.cur_loss : int = 0

        self.networth = 100
        self.tax_percent = 5

        self.ins_company : InsuranceComp = InsuranceComp()

        """ Переменные графического интерфейса в зоне ответственности MainController """

        self.root : tk.Tk = None




    def run(self) -> None: 
        """ Самая первая процедура для запуска """

        # запускаем конструктор интерфейса 
        self.construct_gui()
        
        # запускаем инициализацию состояния компании 
        self.ins_company.init_state() 
        # Запускаем главный цикл обработки событий
        self.root.mainloop()

        return  
    

    def construct_gui(self) -> None:

        # Создаем главное окно
        self.root = tk.Tk()
        self.root.title("Моделирование работы страховой компании")

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

        self.simulate_month()

        return 
    

    def stop_button_click(self) -> None:
        print("Пока нереализована")

    def reset_button_click(self) -> None:
        print("Reset")

        self.reset()
        

    """ Обработчики слайдеров """

    def update_auto_config(self,event):
        self.ins_company.auto_config_updated = True 


    """ Методы выполнения итерации """

    def simulate_month(self) -> None:

        sell_stats = self.ins_company.gen_demand()
        print(sell_stats)


        self.print_finance()
        self.print_sliders() 
        self.curmonth += 1

        # временно поставил 10 - конец симуляции по времени
        if self.curmonth>10:
            print("Симуляция завершена")


    def reset(self) -> None:

        self.networth = 100
        self.curmonth = 1 

        self.modeling_started = False 

        # сброс переменных класса InsuranceComp
        self.ins_company.reset() 



    def print_finance(self) -> None:
        print(f"Текущий месяц: {self.curmonth}")
        print(f"Капитал: {self.networth}")
        print(f"Прибыль: {self.cur_profit}")
        print(f"Убыток: {self.cur_loss}")

        return 

    def print_sliders(self) -> None:
        self.ins_company.print_slider_values()
        return 


main_controller = MainController()

main_controller.run() 

