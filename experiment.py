

from typing import List,Dict,Tuple
from ins_comp import InsuranceComp

class Experiment:
    """ 
        Класс управления экспериментом 

        Управляет экспериментом получая сигналы от класса Interface (изменение положения слайдеров, нажатие кнопок Итерация и Reset и тд)
        Хранит информацию о финансовых и количественных показателяхupdate_auto_config

    """

    def __init__(self): 
        self.modeling_started : bool = False
        self.modeling_finished : bool = False
        self.is_bankrupt : bool = False 

        # срок моделирования
        self.modeling_duration : int = 12

        # номер текущего месяца
        self.curmonth : int = 1

        """ Финансовые и количественные показатели (прибыль,убыток,колво страх. случаев)"""
        self.networth = 100
        self.cur_profit : int = 0 
        self.cur_loss : int = 0
        self.cur_net_profit : int = 0 

        # количественные показатели
        self.cur_auto_sold : int = 0 
        self.cur_med_sold : int = 0 
        self.cur_estate_sold : int = 0 

    
        self.cur_auto_ins_cases : int = 0
        self.cur_med_ins_cases : int = 0 
        self.cur_estate_ins_cases : int = 0 

        # налог
        self.tax_percent = 10
        self.tax_value = 0

        self.ins_company : InsuranceComp = InsuranceComp() 

    def init_state(self):
        self.ins_company.init_state()

        return 

    # возвращает True если моделирование закончено (по какой либо причине)  
    def simulate_month(self) -> bool:
        self.reset_sell()
        self.reset_loss()

        # подсчёт прибыли 
        sell_stats = self.ins_company.gen_demand()
        self.update_sell(sell_stats)

        # подсчёт убытка
        loss_stats = self.ins_company.gen_ins_cases()
        self.update_loss(loss_stats)
        
        self.networth += self.cur_profit - self.cur_loss

        # изменяет капитал, вычитая налог
        self.apply_tax()

        self.cur_net_profit = self.cur_profit-self.cur_loss-self.tax_value

        # self.print_state()

        # обновление дат 
        self.ins_company.update_dates()
        self.curmonth += 1

        # временно поставил 10 - конец симуляции по времени
        if self.curmonth>self.modeling_duration:
            self.modeling_finished = True 

        if self.networth<0:
            self.is_bankrupt = True

        # если какой либо из флагов установлен в True, то моделирование закончено
        return self.is_bankrupt or self.modeling_finished

    # изменяет внутренее состояние после прибыли от продажи страховок
    def update_sell(self,sell_stats:Dict[str,Tuple[int,int]]):
        # распаковка значений
        auto_sold_quantity,auto_profit = sell_stats["auto"]
        med_sold_quantity,med_profit = sell_stats["med"]
        estate_sold_quantity,estate_profit = sell_stats["estate"]

        self.cur_auto_sold = auto_sold_quantity
        self.cur_med_sold = med_sold_quantity
        self.cur_estate_sold = estate_sold_quantity

        self.cur_profit += (auto_profit + med_profit + estate_profit)
        return
    
    # изменяет внутренее состояние после убытков в виде налогов и страховых случаев
    def update_loss(self,loss:Dict[str,List[int]]) -> None: #! пока принимает int, потом будет принимать 
        #! тут должна быть распаковка значений объекта

        self.cur_loss = loss["auto"][1] + loss["med"][1] + loss["estate"][1]
        
        self.cur_auto_ins_cases = loss["auto"][0]
        self.cur_med_ins_cases = loss["med"][0]
        self.cur_estate_ins_cases = loss["estate"][0]

        return 
    
    def apply_tax(self):

        if self.networth<=0:
            self.tax_value = 0

        else:
            self.tax_value = int(self.networth*(self.tax_percent/100))

        self.networth -= self.tax_value

        return
        
    # обнуляет показатели связанные с продажей
    def reset_sell(self):
        self.cur_auto_sold = 0 
        self.cur_med_sold = 0
        self.cur_estate_sold = 0 

        self.cur_profit = 0 
        self.cur_net_profit = 0
        return 

    # обнуляет показатели связанные с потерями денег (страховые случаи + налоги)
    def reset_loss(self) -> None:
        self.cur_loss = 0 

        self.cur_auto_ins_cases = 0
        self.cur_estate_ins_cases = 0 
        self.cur_med_ins_cases = 0 

        self.reset_tax()
        return 
    
    def reset_tax(self) -> None:
        self.tax_value = 0 
        self.tax_percent = 10
        return 


    def reset(self) -> None:

        # сброс финансовых показателей
        self.networth = 100
        self.curmonth = 1 
        self.modeling_duration = 12

        self.reset_sell() 
        self.reset_loss() 

        self.modeling_started = False
        self.modeling_finished = False   
        self.is_bankrupt = False


        # reset страховой компании  
        self.ins_company.reset() 

        return 

    """ Обработчики кнопок """

    # возвращает True если моделирование закончено (по какой либо причине)
    def iteration_button_click(self) -> bool: 


        if not self.modeling_started:
            self.modeling_started = True
 

        # проверяем остались ли еще итерации и не обанкротилась ли компания
        if self.modeling_finished or self.is_bankrupt:
            return True

        else:
            simulation_finished = self.simulate_month()

        return simulation_finished

    def to_the_end(self) -> None:
        
        if not self.modeling_finished:
            while not self.iteration_button_click():
                pass 

        return 

    """ Обновление параметров моделирования """
    def update_auto_config(self,price,time,refund):

        self.ins_company.auto_config_updated = True 
        self.ins_company.auto_slider_price = price
        self.ins_company.auto_slider_time = time
        self.ins_company.auto_slider_refund = refund
        return 
    
    def update_med_config(self,price,time,refund):
        self.ins_company.med_config_updated = True 
        self.ins_company.med_slider_price = price
        self.ins_company.med_slider_time = time
        self.ins_company.med_slider_refund = refund
        return

    def update_estate_config(self,price,time,refund):

        self.ins_company.estate_config_updated = True 
        self.ins_company.estate_slider_price = price
        self.ins_company.estate_slider_time = time
        self.ins_company.estate_slider_refund = refund
        return

     
    
    def update_base_demand(self,demand):
        self.ins_company.base_demand = demand
        return 
    
    def update_insurance_prob(self,percent : int):
        
        self.ins_company.insurance_prob = percent/100
        pass
    
    def update_tax(self,percent : int) -> None:
        self.tax_percent = percent
        return
    

    """ Методы вывода в консоль (временно для отладки)"""

    def print_state(self) -> None:
        print("-----------------------------------------")
        self.print_finance() 
        self.print_quantity()
        self.ins_company.print_slider_values()
        self.ins_company.print_programs()
        print("-----------------------------------------")


    def print_finance(self) -> None:
        print(f"Текущий месяц: {self.curmonth}")

        print(f"Капитал: {self.networth}")
        print(f"Прибыль: {self.cur_profit}")
        print(f"Убыток: {self.cur_loss}")
        print(f"Чистая прибыль: {self.cur_net_profit}")
        print(f"Процент налога {self.tax_percent}")
        print(f"Налог {self.tax_value}")
        return 

    def print_sliders(self) -> None:
        self.ins_company.print_slider_values()
        return 
    
    # вывод количества проданных страховок различного типа
    def print_quantity(self) -> None:
        print(f"Количество проданных автостраховок: {self.cur_auto_sold}")
        print(f"Количество страховых случаев (авто): {self.cur_auto_ins_cases}")

        print(f"Количество проданных медстраховок: {self.cur_med_sold}")
        print(f"Количество страховых случаев (мед): {self.cur_med_ins_cases}")

        return 
    

if __name__ == "__main__":
    pass 
