#Importa os módulos a serem utilizados
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 #Você pode  escolher qualquer porta de 0 a 65535
LISTENER_LIMIT = 5
active_clients = [] #Lista dos clientes

# Esperar as mensagens de um client
def listen_for_messages(client, username):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            
            final_msg = username + '~' + message
            send_messages_to_all(final_msg)

        else:
            print(f"A mensagem enviada pelo client {username} está vazia")


#Função para enviar as mensagens a um único cliente
def send_message_to_client(client, message):

    client.sendall(message.encode())

#Função para mandar mensagem para todos clientes conectados no servidor
def send_messages_to_all(message):
    
    for user in active_clients:

        send_message_to_client(user[1], message)

# Função para manipular os clientes
def client_handler(client):
    
    # O servidor vai esperar pela mensagem ser enviada
    # Além do nome de usuário
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "Servidor~" + f"{username} Adicionado ao chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("O nome de usuário está vazio!")

    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

# função 
def main():

    # Cria o objeto de classe do socket
    # AF_INET: Pois estamos lidando com endereços IPV4
    # SOCK_STREAM: Porque estamos utilizando pacotes TCP para a comunicação
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Cria um bloco try catch
    try:
        # Dá ao servidor um endereço na forma de Ip e porta
        server.bind((HOST, PORT))
        print(f"Rodando o servidor no IP {HOST} e porta {PORT}")
    except:
        print(f"Não foi possível rodar no IP {HOST} e na porta {PORT}")

    # Define o limite do servidor
    server.listen(LISTENER_LIMIT)

    # Recebe conexao de clientes
    while 1:

        client, address = server.accept()
        print(f"Conectado com sucesso ao cliente {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()


if __name__ == '__main__':
    main()