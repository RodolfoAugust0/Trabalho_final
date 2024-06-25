from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label




class ModbusPopup(Popup):
    """
    Popup da configuração modbus
    """
    _info_lb = None
    def __init__(self,server_ip,server_port,**kwargs):
        """
        Construtor da classe ModBus
        """
        super().__init__(**kwargs)   #usei isso pois tem q invocar o construtor da classe base que é a Popup para fazer o construtor da classe derivada corretamente, será sempre assim. sempre que faz a herança e define o construtor dentro da herança, para evitar qualquer problema é bom inicializar o construtor da classe base nop kivy.
        self.ids.txt_ip.text = str(server_ip)  #eu relaciono oq vai aparecer no text input do modbus no ip com oq eu irei receber de argumento
        self.ids.txt_porta.text = str(server_port) #eu relaciono oq vai aparecer no text input do modbus na porta com oq eu irei receber de argumento
    def setInfo(self, message):
        """
        criação do widget quando eu tento conectar no servidor e da errado, é aquele widget dinamico
        """
        self._info_lb = Label(text=message) # criação do label
        self.ids.layout.add_widget(self._info_lb) #inserção do label dentro do id:layout. olhar no popups.kv 
    def clearInfo(self):
        """
        função para deletar o label criado.
        """
        if self._info_lb is not None:
            self.ids.layout.remove_widget(self._info_lb)  #remoção do label criado acima
        
        


class ComandBomba(Popup):
    """
    Popup da configuração da bomba
    """
    pass



class Temperaturapopoup(Popup):
    """
    Popup das configurações 
    """
    def __init__(self,**kwargs):
        """
        Construtor da classe scanpopup
        """
        super().__init__(**kwargs)
    pass


class ScanPopup(Popup):
    
    """
    Popup do scantime
    """
    def __init__(self,scantime,**kwargs):
        """
        Construtor da classe scanpopup
        """
        super().__init__(**kwargs)   #usei isso pois tem q invocar o construtor da classe base que é a Popup para fazer o construtor da classe derivada corretamente, será sempre assim. sempre que faz a herança e define o construtor dentro da herança, para evitar qualquer problema é bom inicializar o construtor da classe base nop kivy.
        self.ids.txt_st.text = str(scantime)  #eu relaciono oq vai aparecer no text input do scantime com oq eu irei receber de argumento



 
    
    
    
    
    
    
    