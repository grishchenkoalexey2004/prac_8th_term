from typing import Dict,Optional


class InsuranceProgram:
    """
        Класс описывающий конфигурацию страховой программы
    """

    def __init__(self,prog_id:int,prog_type:str,time:int,price:int,max_comp:int):

        self.prog_id : int = prog_id

        self.prog_type : str = prog_type
        self.time : int = time 
        self.price : int = price
        self.max_comp : int = max_comp

        self.profit_coef : float = (time*max_comp)/price


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

        self.auto_base_demand : int = 10    
        self.estate_base_demand : int = 5        
        self.med_base_demand : int = 20 

        self.auto_config : Optional[InsuranceProgram] = None 
        self.estate_config : Optional[InsuranceProgram] = None 
        self.med_config : Optional[InsuranceProgram] = None 

        self.progs_active: list[int] = [] 
        self.ins_agreements: Dict[int,InsuranceAgreement] = dict()


    def gen_ins_cases(self) -> Dict[str,int]:
        pass 

    def add_ins_agr(ins_agr:InsuranceAgreement) -> None:
        pass 

    def delete_ins_prog(ins_prog_id:int) -> None: 
        pass 

    def gen_demand() -> None: 
        pass 



class MainController:
    """
        Главный класс, отвечающий за взаимодействие между интерфейсом и всеми остальными классами
    """
    
    def __init__(self):
        self.curmonth = 1

        self.cur_profit = 0 
        self.cur_loss = 0

        self.networth = None
        self.tax_percent = None

        self.ins_company : InsuranceComp = InsuranceComp()


    def launch_modelling() -> None:
        pass 

    def restart_modelling() -> None:
        pass

    def simulate_month() -> None:
        pass
