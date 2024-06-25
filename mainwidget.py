import os 
os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'
from kivy.uix.boxlayout import BoxLayout
from popups import ModbusPopup, ScanPopup, ComandBomba,Temperaturapopoup
from pyModbusTCP.client import ModbusClient 
from kivy.core.window import Window
from threading import Thread
from time import sleep
from datetime import datetime
import random
from pymodbus.payload import BinaryPayloadDecoder


class MainWidget(BoxLayout):
    """
    Widget principal da aplicação
    """
    
    _updateThread = None
    _updateWidgets = True #atributo que vai indicar se eu quero continuar atualizando os dados ou nao.
    _tags = {}
    
    
    def __init__(self,**kwargs):
        """
        Construtor do widget principal
        """
        super().__init__()
        self._scan_time = kwargs.get('scan_time')     #procuro nos argumentos o scan_time e aponto o atributo pra ele
        self._serverIP = kwargs.get('server_ip')       #procuro nos argumentos o Modbus e aponto o atributo pra ele
        self._port = kwargs.get('server_port')      #procuro nos argumentos o Modbus e aponto o atributo pra ele
        self._modbusPopup = ModbusPopup(server_ip = self._serverIP,server_port=self._port )  # ligo o modbuspopup no widget principal. no .kv eu uso root._modbusPopup.open() ai irá abrir o pop. uso os atributos como argumento para aparecer no textinput do ip e da porta
        self._scanPoPup = ScanPopup(scantime = self._scan_time)   # ligo o scanpopup no widget principal. no .kv eu uso root._scanPoPup.open() ai irá abrir o pop. ainda. uso o atributo como argumento para aparecer no textinput. 
        self._comandobomba = ComandBomba()                  # ligo o ComandoBomba no widget principal. no .kv eu uso root._comandobomba.open() ai irá abrir o pop
        self._modbusClient = ModbusClient(host = self._serverIP, port=self._port) # crio o cliente  que vai acessasar o servidor
        self._meas = {}    #atributo que é um dicionario que irá possuir as medições atuais
        self._opcoes = Temperaturapopoup()
        self._meas['timestamp'] = None #vai ter um campo chamado timestamp  
        self._meas['values'] = {}  #vai ser os valores das varias tags do sistema e ele será um dicionario, ou seja, o meas é um dicionario que ingloba o dicionario values.
        for key,value in kwargs.get('modbus_addrs').items():   #a leitura das tags é feita atraves do for. key são as tags e value é o endereço delas. 
            if key == 'Tensao':
                plot_color = (1,0,0,1)    # é a cor da linha do gráfico que irá ser criado
            else:
                plot_color = (random.random(),random.random(),random.random(),1)
            self._tags[key] ={'addr':value, 'color':plot_color}   #repare que está ocorrendo a criação de outro dicionario. estou pegando as key(tags) do dicionario modbus_adrrs e estou criando chaves com essas tags
                                                                 # e o valor está sendo outro dicionario onde a chave é addr e o valor é o value(endereço) do dicionario modbus_adrrs. o mesmo acontecer com color e plotcolor
        self.ids
        
        
        
    def startDataRead(self,ip,port):
        """
        Metodo utilizado para configuração do IP e porta do servidor ModBus e vai inicializar uma Thread
        para a leitura dos dados e atualização da interface gráfica.
        """
        self._serverIP = ip
        self._serverPort = port
        self._modbusClient.host = self._serverIP
        self._modbusClient.port = self._serverPort
        try:
            Window.set_system_cursor("wait")  #faz com que inquanto a conecção n seja realizada o mouse fica com aquele negocio de carregando
            self._modbusClient.open() #tenta realiazar a coneção com o servidor
            Window.set_system_cursor("arrow") # se a coneção for realizada volta a setinah normal
            if self._modbusClient.is_open:
                self._updateThread = Thread(target =self.updater)     # criação de uma thread para a leitura e atualização de dados. o self.updater é o metodo criado para a atualização.
                self._updateThread.start()  #inicio a atualização e leitura
                self.ids.img_con.source = 'imagens/Conectado.jpeg'  #mudo a iamgem
                self._modbusPopup.dismiss()
            else:
                self._modbusPopup.setInfo("Falha na conexõa do servidor")
        except Exception as e:
            print("Erro:", e.args)
            
    def updater(self):
        """
        Metodo que invoca as rotinas de leitura dos dados, 
        atualização da interface e inserção dos dados no banco de dados.

        """
        try:
            while self._updateWidgets:
                self.readData()   #ler os dados MODBUS
                self.updateGUI()   #atualizar a interface
                #inserir os dados no banco de dados.
                sleep(self._scan_time/1000) #regular o tempo pra n ficar fazendo essas coisas numa velocidade absurda
        except Exception as e:
            self._modbusClient.close()
            print("Erro:", e.args)
    def count_digits(self,num):
        self._num_str = str(abs(num))
        self._num_digits = len(self._num_str)
        return self._num_digits
    
    
    def readData(self):
        """
        Metodo para a leitura dos dados por meio do protocolo modbus
        """
    
        self._meas['timestamp'] = datetime.now()  #quando usa esse metodo ele retorna exatamente o horario corrente do sistema operacionmal 
        for key,value in self._tags.items():
                a =  self._modbusClient.read_holding_registers(value['addr'],1)[0]
                if  len(str(abs(a))) <= 3:
                    self._meas['values'][key] =self._modbusClient.read_holding_registers(value['addr'],1)[0]  # eu abro o meas e faço a chave values dele receber os valores dos registradores. eu uso o key(tags) para abrir e pegar os addr(endereço) de cada key
                else :
                    result = self._modbusClient.read_holding_registers(value['addr'],2)
                    decoder = BinaryPayloadDecoder.fromRegisters(result)
                    self._meas['values'][key] = decoder.decode_32bit_float()
                    
    
    def updateGUI(self):
        """
        Metodo para a atualização da interface gráfica a partir dos dados lidos
        """
        #atualização dos labels das temperaturas
        for key,value in self._tags.items():
            self.ids[key].text = str(self._meas['values'][key])
            
        self.ids.lb_temp1.size = (self.ids.lb_temp1.size[0],-(-137-24+(self._meas['values']['Temperatura']/1500*self.ids.regua_d.size[1])))
        self.ids.lb_temp2.size = (self.ids.lb_temp2.size[0],-24+(self._meas['values']['Temperatura']/1500*self.ids.regua_d.size[1]))
            
            
            
    def stopRefresh(self):
        self._updateWidgets = False
    
    
    
    
    def liga_motor(self):
        
        """
        aqui é a opção de ligar         o motor
        1-->soft
        2-->inversor
        3-->direta
        
        """
        if self._modbusClient.read_holding_registers(1324,1)[0] == 1:
            self._modbusClient.write_single_register(1316,1) #liga    
            
            
        elif self._modbusClient.read_holding_registers(1324,1)[0] == 2:
            self._modbusClient.write_single_register(1312,1)
            
            
        elif self._modbusClient.read_holding_registers(1324,1)[0] == 3:
            self._modbusClient.write_single_register(1319,1)
            
            
        else:
            print("erro")

    def desliga_motor(self):
    
        """
        aqui é a opção de desligar o motor
        1-->soft
        2-->inversor
        3-->direta
        
        """
        if self._modbusClient.read_holding_registers(1324,1)[0] == 1:
            self._modbusClient.write_single_register(1316,0) #desliga    
            
            
        elif self._modbusClient.read_holding_registers(1324,1)[0] == 2:
            self._modbusClient.write_single_register(1312,0)#desliga
            
            
        elif self._modbusClient.read_input_registers(1324,1)[0] == 3:
            self._modbusClient.write_single_register(1319,0)#desliga
            
                
        else:
            print("erro")

    def reset_motor(self):
    
        """
        aqui é a opção de resetar o motor
        1-->soft
        2-->inversor
        3-->direta
        
        """
        if self._modbusClient.read_holding_registers(1324,1)[0] == 1:
            self._modbusClient.write_single_register(1316,2) #reseta    
            
            
        elif self._modbusClient.read_holding_registers(1324,1)[0] == 2:
            self._modbusClient.write_single_register(1312,2) #reseta
            
            
        elif self._modbusClient.read_holding_registers(1324,1)[0] == 3:
            self._modbusClient.write_single_register(1319,2) #reseta
             
            
        else:
            print("erro")
                
            
            
            
    def escolhasoft(self):
        self._modbusClient.write_single_register(1324,1)
    def escolhainversor(self):
        self._modbusClient.write_single_register(1324,2)
    def escolhadireta(self):
        self._modbusClient.write_single_register(1324,3)    
        
        
    
    
        
    
        
    