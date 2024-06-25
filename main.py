from kivy.app import App
from mainwidget import MainWidget
from kivy.lang.builder import Builder

class MainApp(App):
    """
    Classe com o aplicativo
    """
    
    def build(self):
        """
        metodo que gera o aplicativo com base no widget principal
        """
        self._widget= MainWidget(scan_time=1000, server_ip= '127.0.0.1',server_port=502,
        modbus_addrs = {           #o modbus_addrs é um dicionario que vai possuir as tags que irão ser lidas e p seu endereço
            'Tensao':3000,
            'Rotacao':1334,
            'Corrente':1034,
            'Torque':727,
            'enrolamentoR':700,
            'enrolamentoS':702,
            'enrolamentoT':704,
            'temp_carcaca':706,
            
        }
                                 
                            
                                 
                                 
                                 
                                 
        )
        return self._widget
    
    def on_stop(self):
        """
        Metodo executado quando a aplicação é fechada
        """
        self._widget.stopRefresh()
    
if __name__ == '__main__':
    
    Builder.load_string(open("mainwidget.kv",encoding= "utf-8").read(),rulesonly= True)
    Builder.load_string(open("popups.kv",encoding= "utf-8").read(),rulesonly= True)
    MainApp().run()