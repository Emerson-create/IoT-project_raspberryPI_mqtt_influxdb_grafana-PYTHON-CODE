import paho.mqtt.client as mqtt#Biblioteca mqtt client
import sys
from gpiozero import CPUTemperature#Biblioteca para capturar temperatura do Core da RaspberryPI
import time

#definicoes do MQTT
Broker = "192.168.0.6" #broker publico utilizado.
porta_broker = 1883 #porta utilizada para comunicacao com o broker MQTT
                    #utilize a porta 1883 para comunicacao com conexao nao segura
keep_alive_broker = 60 #tempo (em segundos) do keep-alive
topico = "bic4p"  #topico MQTT que o programa ira "ouvir" (fazer subscribe)
                                     #dica: troque o nome do topico por algo "unico", 
                                     #Dessa maneira, ninguem ira saber seu topico de
                                     #subscribe e interferir em seus testes
#Callback - conexao ao broker realizada
def on_connect(client, userdata, flags, rc):
    print("[STATUS] Conectado ao Broker.")
    #faz subscribe automatico no topico
    client.publish(topico_publish)
#Callback - mensagem recebida do broker
#toda vez que uma mensagem for recebida do broker, esta funcao sera chamada
def on_message(client, userdata, msg):
    MensagemRecebida = str(msg.payload)    
    print("[MSG RECEBIDA] Topico: "+msg.topic+" / Mensagem: "+MensagemRecebida)    
#create function for callback
def on_publish(client,userdata,result):
    print("data published \n")
    pass
#programa principal:
try:
        print("[STATUS] Inicializando MQTT...")
        #inicializa MQTT:
        
        #create client object
        #assign function to callback
        #establish connection
        client= mqtt.Client("control1")
        client.on_publish = on_publish
        client.on_connect = on_connect
        client.connect(Broker, porta_broker, keep_alive_broker)
        #cria client MQTT e define funcoes de callback de conexao (client.on_connect) 
        #e recepcao de dados recebidos (client.on_message)
        while True:
                cpu = CPUTemperature()
                temp =str(cpu.temperature)
                client.publish(topico,temp)#publish
                time.sleep(5)
except KeyboardInterrupt:
        print ("\nCtrl+C pressionado, encerrando aplicacao e saindo...")
        sys.exit(0)