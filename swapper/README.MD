# Lista de tarefas a serem concluídas para o trocador

+ [ ] Criação do DOCKERFILE
+ [ ] Inicializar o serviço localmente usando sockets
+ [ ] Estabelecer comunicação entre um trocador e produtor
    + [ ] Permitir que o produtor envie as mensagens para o trocador
    + [ ] Criar nova thead a cada cliente (produtor/consumidor) conectado no trocador
    + [ ] Armazenar as mensagens recebidas pelo produtor em sua respectiva fila no trocador
    + [ ] Transmitir mensagem para o consumidor correto de acordo com o rótulo estabelecido nos parâmetros de inicialização
+ [ ] Implementação de exclusão mútua para filas nos consumidores

⚠️**aviso 1**⚠️: Produtor pode enviar mensagens de qualquer rótulo, mas um consumidor recebe mensagens apenas do seu rótulo de inicialização. (Mensagens com rótulo fanout devem ser recebidas por todos os consumidores).

⚠️**aviso 2**⚠️: Vários produtores podem acessar o mesmo consumidor, aí que entra a técnica de exclusão mútua!