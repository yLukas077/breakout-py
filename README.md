## Projeto P1 - BREAKOUT

### Logo do game

![Logo do Game](images/logo-breakout.png)

### Resumo do Jogo

Este é um projeto para a disciplina de Introdução à Programação na Universidade Federal de Pernambuco (UFPE). É uma variação do clássico jogo "Breakout". O objetivo do jogo é destruir todos os blocos na tela usando uma bola que rebate em uma raquete controlada pelo jogador. A bola deve ser mantida em jogo o máximo possível, evitando que ela caia abaixo da raquete.

### Membros e Suas Contribuições

- **Lucas Vinícius**: Desenvolvimento e planejamento da lógica geral do jogo, parte da física e resolução de bugs, controle da barra e movimento da bola.
- **Juan Henrique**: Design visual, classes dos objetos e suas propriedades, criação dos assets de jogo, incluindo blocos, barra, bola, e power-ups.
- **Victor Daniel**: Implementação de parte da física do jogo, incluindo detecção de colisão dos blocos, música de fundo e efeitos sonoros.
- **Levi Serrano**: Desenvolvimento e implementação de power-ups e suas funcionalidades.

### Objetos

- **Barra**: Controlada pelo jogador usando as setas do teclado. A barra se move horizontalmente na parte inferior da tela e é usada para rebater a bola.
  
- **Bola**: Uma esfera que se move pela tela, rebatendo nas bordas, na barra e nos blocos. O jogador deve evitar que a bola caia abaixo da barra.

- **Blocos**: Objetos estáticos que a bola deve destruir para o jogador ganhar pontos.

- **Ball Duplicate (Multiplicador de Bolas)**: Um power-up que duplica o número de bolas em jogo, aumentando a dificuldade e o potencial de destruição de blocos.

- **Extra Ball (Bola extra)**: Um power-up que adiciona uma bola a mais em campo.
  
- **Extend Bar (Aumento de Barra)**: Um power-up que aumenta temporariamente o tamanho da barra, facilitando o controle da bola.

### Ferramentas, Bibliotecas, Frameworks e Conceitos de Programação Aplicados no Projeto

- **Linguagem de Programação**: Python
- **Biblioteca**: Pygame
- **Conceitos de Programação**: Orientação a Objetos, Detecção de Colisões, Física de Jogo, Animações, Gerenciamento de Estados

### Desafios e Aprendizados ao Longo do Projeto

- Desafios enfrentados na implementação da física da bola e na detecção de colisões precisas.
- Aprendizados significativos sobre o uso de bibliotecas gráficas e sonoras, como a Pygame.
- Melhor compreensão de como criar uma experiência de usuário fluida e envolvente através de design visual e som.

### Capturas do Jogo

<p align="center">
  <img src="images/captura1.png" alt="Captura de Tela 1" width="300">
  <img src="images/captura2.png" alt="Captura de Tela 2" width="300">
</p>
<p align="center">
  <img src="images/captura3.png" alt="Captura de Tela 3" width="300">
  <img src="images/captura4.png" alt="Captura de Tela 4" width="300">
</p>


---

## README do Projeto "Breakout"

### Descrição do Projeto

O nosso Breakout é uma recriação moderna do clássico jogo de arcade desenvolvido em Python usando a biblioteca Pygame. Este projeto foi criado para oferecer uma experiência de jogo divertida e envolvente, ao mesmo tempo que proporciona um excelente exercício de programação e desenvolvimento de jogos. O jogador controla uma raquete para rebater uma bola que destrói blocos na parte superior da tela. O objetivo é destruir todos os blocos para vencer, evitando que a bola caia abaixo da raquete. O jogo inclui power-ups que adicionam bolas extras, duplicam bolas ou aumentam o tamanho da raquete, aumentando a diversão e o desafio.

### Pré-requisitos

- Python 3.x
- Pygame

### Instalação

```bash
# Clonar o repositório
git clone <URL_DO_REPOSITÓRIO>

# Navegar até o diretório do projeto
cd breakout-py

# Instalar as dependências
pip install pygame


### Como Jogar

1. Inicie o jogo executando o script principal:
   ```bash
   python main.py
   ```
2. Use as setas do teclado para mover a barra.
3. Pressione "Espaço" para lançar a bola.
4. O objetivo é destruir todos os blocos na tela.

### Contribuições

Para contribuir com o projeto, siga estas etapas:

1. Faça um fork do repositório.
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`).
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`).
4. Envie para a branch (`git push origin feature/nova-feature`).
5. Abra um Pull Request.

### Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo LICENSE para mais detalhes.

### Contato

Para dúvidas ou sugestões, entre em contato com a equipe de desenvolvimento pelo email: equipe.breakout1@gmail.com
