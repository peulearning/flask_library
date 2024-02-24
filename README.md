# Gerenciamento de Biblioteca  📚
Olá saudações !

Este projeto tem como finalidade boas práticas de programação, além de conhecimentos específicos na linguagem Python, onde utilizamos recursos e libs como Flask, MySQL. Trabalho cujo está sendo ministrado na disciplina de Arquitetura de Software no 6 º período do curso de Bacharelado de Sistemas de Informações no 2 º semestre letivo de 2023/2024 . com intuito de consolidar conhecimentos foi proposto por meio do nosso Professor elaborar uma aplicação utilizando microserviços.

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.


### 📋 Pré-requisitos & 🔧 Instalação

De que coisas você precisa para instalar o software e como instalá-lo?

Independente do sistema operacional que esteja , verifique se possui o Python e sua versão instalada na sua máquina.

``
Faça o Clone do Projeto

``

```
git clone https://github.com/peulearning/flask_library.git

```


``
Nas depedências do projeto rodar no terminal se estiver utilizando PYTHON

```
pip install -r requirements.txt

```

Para inicializar deve está conectado com seu MySQL e fazer as configurações nos arquivos  ``setupDB.py``, ``app.py``e ``test.py`` os parâmetros a serem modificados estão comentados.

Em seguida deve criar as tabelas usando ``setupDB.py``

```
cd utils

python3 setupDB.py

cd ..

```

Faça o passo anterior para funcionar e ligue o seu servidor local (XAMPP OU SIMILAR) !


Por fim execute

```
python3 app.py

```

``

### 🔩 Analise os testes de ponta a ponta

```
    Teste de funcionalidade básica:
        Verificar se é possível adicionar novos livros ao sistema.
        Verificar se é possível pesquisar e encontrar livros no sistema.
        Verificar se é possível emprestar e devolver livros.
        Verificar se é possível atualizar informações de livros e usuários.
        Verificar se é possível visualizar histórico de empréstimos e reservas.

    Teste de integração com banco de dados:
        Verificar se os dados são corretamente armazenados e recuperados do banco de dados.
        Testar se as operações de leitura, escrita e atualização de dados estão funcionando corretamente.

    Teste de segurança:
        Verificar se há proteção contra acessos não autorizados.
        Testar se as senhas dos usuários são armazenadas de forma segura.
        Verificar se há proteção contra injeção de SQL e outros ataques comuns.

    Teste de usabilidade:
        Avaliar a facilidade de uso do sistema para os usuários.
        Verificar se a navegação é intuitiva e se as funcionalidades são facilmente acessíveis.
        Coletar feedback dos usuários sobre a experiência de uso do sistema.

    Teste de desempenho:
        Avaliar a velocidade de resposta do sistema em diferentes cenários de uso.
        Testar a capacidade do sistema em lidar com um grande volume de dados e usuários simultâneos.
        Identificar possíveis gargalos de desempenho e otimizar o sistema conforme necessário.

    Teste de integração com sistemas externos:
        Verificar se o sistema se integra corretamente com sistemas de pagamento, sistemas de gestão de bibliotecas externas, entre outros.

    Teste de compatibilidade:
        Verificar se o sistema funciona corretamente em diferentes navegadores web e dispositivos.
        Testar a compatibilidade com diferentes sistemas operacionais, se aplicável.
```

## 🛠️ Construído com

Mencione as ferramentas que você usou para criar seu projeto

- [Python](https://docs.python.org/pt-br/3/tutorial/) - PYTHON
- [Flask](https://flask.palletsprojects.com/en/3.0.x/) - MicroFramework
- [MySQL](https://www.mysql.com/) - Banco de Dados
- [XAMPP](https://www.apachefriends.org/pt_br/index.html) - LocalHost

## 🖇️ Colaborando

Por favor, leia o [COLABORACAO.md](https://gist.github.com/usuario/linkParaInfoSobreContribuicoes) para obter detalhes sobre o nosso código de conduta e o processo para nos enviar pedidos de solicitação.

## 📌 Versão

(Final) - 22-02-2024 (Versão_Final)


## ✒️ Autores

Mencione todos aqueles que ajudaram a levantar o projeto desde o seu início

- **Prof. Danilo Nunes** - _Ideia do Projeto Inicial_ - [Orientador](https://github.com/danilonunes)

- **Pedro Henrique (EU)** - _Dev_

Você também pode ver a lista de todos os [colaboradores](https://github.com/usuario/projeto/colaboradores) que participaram deste projeto.

## 📄 Licença

Este projeto está sob a licença (sua licença) - veja o arquivo [LICENSE.md](https://github.com/usuario/projeto/licenca) para detalhes.

---

⌨️ com ❤️ por [Pedrão Ribeiro](https://github.com/peulearning) 😊
