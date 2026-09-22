# Novo Recurso: HistÃ³rico de Auditoria (Logs) ðŸ“œ

A infraestrutura do seu Kanban foi expandida para incluir um sistema rigoroso de rastreio de aÃ§Ãµes. Nenhuma modificaÃ§Ã£o nos agendamentos passa despercebida agora.

## MudanÃ§as Realizadas

### 1. Novo Banco de Dados (`logs.csv`)
Um novo arquivo foi criado automaticamente na pasta `data` para armazenar o log de todas as aÃ§Ãµes de forma imutÃ¡vel. Ele registra:
- O **ID do cartÃ£o**
- O **E-mail** de quem executou a aÃ§Ã£o
- A **Data e Hora** exatas (Timestamp)
- O **Tipo da AÃ§Ã£o** (CriaÃ§Ã£o, EdiÃ§Ã£o, MovimentaÃ§Ã£o, ConclusÃ£o, Reabertura)
- Os **Detalhes** da aÃ§Ã£o

### 2. Monitoramento Inteligente (Diffing)
Quando vocÃª edita um cartÃ£o, o sistema nÃ£o salva apenas "CartÃ£o Editado". Ele compara internamente o que o cartÃ£o tinha antes com os novos valores preenchidos.
- Se vocÃª mudar a sala de reuniÃµes e adicionar o diretor, o log ficarÃ¡ exatamente:
  > *Alterou Local/Sala de 'AUDITÃ“RIO' para 'DIR 1' | Alterou Diretor de '' para 'ELOIR'*

### 3. Interface de HistÃ³rico
- Foi adicionado o botÃ£o **ðŸ“œ** (Ver HistÃ³rico) na base de todos os cartÃµes (tanto nos Ativos quanto nos ConcluÃ­dos).
- Ao clicar no botÃ£o, uma janela modal se abre listando as aÃ§Ãµes da mais recente para a mais antiga. Cada aÃ§Ã£o possui destaque visual (uma barra laranja lateral) facilitando a leitura da linha do tempo daquele agendamento especÃ­fico.

## Como Testar
1. Acesse o sistema e crie um novo cartÃ£o.
2. Abra o histÃ³rico (ðŸ“œ) dele e veja o evento de *CriaÃ§Ã£o*.
3. Edite o cartÃ£o e mude qualquer informaÃ§Ã£o e salve. 
4. Abra o histÃ³rico (ðŸ“œ) novamente e veja o detalhamento da *EdiÃ§Ã£o*.
5. Conclua o cartÃ£o (âœ…), vÃ¡ na aba *ConcluÃ­dos* e abra o histÃ³rico dele de lÃ¡!


---

# ðŸŽ¨ Walkthrough: Cores DinÃ¢micas e PersonalizÃ¡veis

Acabamos de dar um enorme passo na liberdade de uso do seu sistema! Todo aquele processo rÃ­gido que nos obrigava a alterar o cÃ³digo-fonte sÃ³ para mudar a cor de uma etiqueta foi removido.

As cores agora moram dentro do seu banco de dados, em uniÃ£o com o nome de cada sala, diretor ou serviÃ§o.

## O que mudou?

### 1. Tudo Ã© GerenciÃ¡vel ðŸŽ›ï¸
Na sua aba **UtilitÃ¡rios**, na manutenÃ§Ã£o de Diretores, Salas e ServiÃ§os Adicionais, tanto a funÃ§Ã£o de "Adicionar" quanto a de "Editar" ganharam um campo de seleÃ§Ã£o de cor. 
VocÃª pode, a qualquer momento, mudar a cor de um diretor (de verde para azul, por exemplo), e imediatamente todos os cartÃµes antigos e novos daquele diretor mudarÃ£o de cor automaticamente!

### 2. A Paleta de Cores ðŸ–Œï¸
Deixei 9 cores disponÃ­veis padronizadas que harmonizam bem com o fundo claro das etiquetas e que nÃ£o cansam os olhos:
* `green` (Verde PadrÃ£o - Diretores)
* `light_green` (Verde Claro)
* `purple` (Roxo - Salas)
* `lilac` (LilÃ¡s - Salas CAD/DIR)
* `brown` (Marrom - AlimentaÃ§Ã£o PadrÃ£o)
* `red` (Vermelho - Entregas / TI / Carro)
* `blue` (Azul - Qtd. de Pessoas)
* `yellow` (Amarelo)
* `gray` (Cinza)

### 3. MigraÃ§Ã£o Sem Perdas ðŸ›¡ï¸
Rodei um script silencioso por trÃ¡s dos bastidores que pegou todas as opÃ§Ãµes que vocÃª tinha no banco e gravou as cores nelas exatamente conforme vocÃª havia me passado na tabela anterior. Portanto, nada mudou visualmente no seu painel para as etiquetas velhas, a Ãºnica mudanÃ§a Ã© que vocÃª agora tem o poder de alterÃ¡-las pela tela!

> [!TIP]
> **Teste rÃ¡pido:**
> VÃ¡ em **UtilitÃ¡rios**, clique em **Editar Sala**, selecione a `A1 ARENA` (que Ã© roxa) e altere a cor dela para `yellow`. Depois volte para o Painel e veja os cartÃµes mudarem de cor magicamente!


---

# ðŸš€ Walkthrough: O Novo Kanban Moderno

O Kanban passou por uma grande modernizaÃ§Ã£o estrutural para ficar mais com a cara de ferramentas consagradas (como o Trello), melhorando tanto o visual quanto o poder de gestÃ£o por baixo dos panos. 

Aqui estÃ£o as mudanÃ§as que vocÃª notarÃ¡ a partir de agora:

## 1. ðŸªŸ Tudo agora Ã© Modal (Pop-up)
Em vez daqueles enormes "acordeÃµes" (Expanders) que ficavam no meio da tela poluindo a visÃ£o apÃ³s o uso, agora o sistema interage com vocÃª atravÃ©s de janelas nativas flutuantes.
* **Adicionar CartÃ£o:** O botÃ£o principal `+ Adicionar Novo Agendamento` chama a tela sobre a pÃ¡gina.
* **Editar CartÃ£o:** Ao clicar no emoji de lÃ¡pis (âœï¸) na base do cartÃ£o, vocÃª edita todos os campos no mesmo layout modal flutuante.
* **Mover CartÃ£o:** Ao clicar no emoji de seta (âž¡ï¸) na base do cartÃ£o, vocÃª altera rapidamente a coluna em que ele se encontra.

## 2. ðŸ—‚ï¸ MÃºltiplos Diretores e Salas (MultiseleÃ§Ã£o)
Agora vocÃª nÃ£o estÃ¡ mais restrito a selecionar apenas um diretor ou apenas uma sala por cartÃ£o. 
Os campos de "Diretores" e "Salas" na criaÃ§Ã£o e ediÃ§Ã£o do cartÃ£o viraram **mÃºltipla escolha**!
* VocÃª pode adicionar 3 diretores e 2 salas simultaneamente.
* O cartÃ£o desenharÃ¡ inteligentemente uma etiqueta independente para cada um, respeitando as cores da nossa regra (Verde escuro / Verde claro).

## 3. ðŸ·ï¸ Etiquetas (Tags) embutidas no CartÃ£o
O layout do cartÃ£o visual no painel tambÃ©m mudou. Toda a caixa possui uma borda nativa limpa, e as etiquetas (Diretores, Salas, Pessoas, ServiÃ§os, TI, Carro) agora sÃ£o desenhadas **dentro da caixa do cartÃ£o** de maneira mais limpa e moderna, abandonando aquele aspecto de "texto solto na pÃ¡gina" que tÃ­nhamos antes.

## 4. âš™ï¸ ManutenÃ§Ã£o de "ServiÃ§os Adicionais"
A antiga opÃ§Ã£o "Catering / Copa" foi renomeada para "ServiÃ§os Adicionais". Mais importante do que isso: as opÃ§Ãµes nÃ£o estÃ£o mais travadas no cÃ³digo!
* **Aba UtilitÃ¡rios:** Criamos a tela de manutenÃ§Ã£o de ServiÃ§os Adicionais, exatamente igual Ã s telas de Diretores e Salas.
* VocÃª pode Adicionar, Remover e Editar o nome de opÃ§Ãµes (como AlmoÃ§o, Coffee, iFood) por conta prÃ³pria a qualquer momento.

---
> [!TIP]
> **Como testar agora mesmo:**
> 1. VÃ¡ na aba "Painel Kanban".
> 2. Clique em **âž• Adicionar Novo Agendamento**.
> 3. Na janela que abrir, tente selecionar mais de um **Diretor** e mais de uma **Sala**. Salve o cartÃ£o.
> 4. Repare que as etiquetas foram separadas por cores direitinho e agora o cartÃ£o possui os botÃµes (âœï¸ e âž¡ï¸) embutidos no rodapÃ©!

