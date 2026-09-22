# 🚀 Walkthrough: Auto-Refresh, Sigilo e Change Log

Mais um pacote de funcionalidades implantadas no Port.Ico focadas na experiência em nuvem e na segurança da informação!

## O que mudou?

### 1. 🔄 Atualização em Tempo Real (Invisível)
Diferente das estratégias tradicionais que atualizam a página inteira, implantamos a nova tecnologia de Fragmentos do Streamlit. 
A cada 10 segundos, o miolo do seu painel consulta os dados mais recentes na nuvem, enquanto todo o restante da tela (menus, cabeçalho e janelas abertas) fica completamente intacto e congelado. O resultado? O painel está sempre atualizado de forma silenciosa, sem jamais fechar a sua janela na sua cara!

### 2. 🛡️ Sigilo de Reuniões (Filtro Blur)
Como os perfis **TI** e **Copa** são focados apenas no apoio operacional (equipamentos e alimentação), eles não precisam saber o assunto estratégico da reunião.
- A partir de agora, se alguém desses dois perfis logar no sistema, o Título (Nome do Cartão) aparecerá completamente borrado na interface, sendo impossível de ler e bloqueado contra 'Copiar e Colar'.

### 3. ℹ️ Nova Tela 'Sobre' & Histórico
Para consolidar o controle de versões, o sistema ganhou uma central administrativa ao lado do botão de Sair:
- **Sobre:** Créditos de desenvolvimento e um robô inteligente que lê nativamente a base do Git para cravar com exatidão a versão do código e o último instante de atualização.
- **Change Log:** Um documento vivo embutido no painel para que a equipe sempre possa ler quais foram as últimas inovações liberadas!


---

# Novo Recurso: Histórico de Auditoria (Logs) 📜

A infraestrutura do seu Kanban foi expandida para incluir um sistema rigoroso de rastreio de ações. Nenhuma modificação nos agendamentos passa despercebida agora.

## Mudanças Realizadas

### 1. Novo Banco de Dados (`logs.csv`)
Um novo arquivo foi criado automaticamente na pasta `data` para armazenar o log de todas as ações de forma imutável. Ele registra:
- O **ID do cartão**
- O **E-mail** de quem executou a ação
- A **Data e Hora** exatas (Timestamp)
- O **Tipo da Ação** (Criação, Edição, Movimentação, Conclusão, Reabertura)
- Os **Detalhes** da ação

### 2. Monitoramento Inteligente (Diffing)
Quando você edita um cartão, o sistema não salva apenas "Cartão Editado". Ele compara internamente o que o cartão tinha antes com os novos valores preenchidos.
- Se você mudar a sala de reuniões e adicionar o diretor, o log ficará exatamente:
  > *Alterou Local/Sala de 'AUDITÓRIO' para 'DIR 1' | Alterou Diretor de '' para 'ELOIR'*

### 3. Interface de Histórico
- Foi adicionado o botão **📜** (Ver Histórico) na base de todos os cartões (tanto nos Ativos quanto nos Concluídos).
- Ao clicar no botão, uma janela modal se abre listando as ações da mais recente para a mais antiga. Cada ação possui destaque visual (uma barra laranja lateral) facilitando a leitura da linha do tempo daquele agendamento específico.

## Como Testar
1. Acesse o sistema e crie um novo cartão.
2. Abra o histórico (📜) dele e veja o evento de *Criação*.
3. Edite o cartão e mude qualquer informação e salve. 
4. Abra o histórico (📜) novamente e veja o detalhamento da *Edição*.
5. Conclua o cartão (✅), vá na aba *Concluídos* e abra o histórico dele de lá!


---

# 🎨 Walkthrough: Cores Dinâmicas e Personalizáveis

Acabamos de dar um enorme passo na liberdade de uso do seu sistema! Todo aquele processo rígido que nos obrigava a alterar o código-fonte só para mudar a cor de uma etiqueta foi removido.

As cores agora moram dentro do seu banco de dados, em união com o nome de cada sala, diretor ou serviço.

## O que mudou?

### 1. Tudo é Gerenciável 🎛️
Na sua aba **Utilitários**, na manutenção de Diretores, Salas e Serviços Adicionais, tanto a função de "Adicionar" quanto a de "Editar" ganharam um campo de seleção de cor. 
Você pode, a qualquer momento, mudar a cor de um diretor (de verde para azul, por exemplo), e imediatamente todos os cartões antigos e novos daquele diretor mudarão de cor automaticamente!

### 2. A Paleta de Cores 🖌️
Deixei 9 cores disponíveis padronizadas que harmonizam bem com o fundo claro das etiquetas e que não cansam os olhos:
* `green` (Verde Padrão - Diretores)
* `light_green` (Verde Claro)
* `purple` (Roxo - Salas)
* `lilac` (Lilás - Salas CAD/DIR)
* `brown` (Marrom - Alimentação Padrão)
* `red` (Vermelho - Entregas / TI / Carro)
* `blue` (Azul - Qtd. de Pessoas)
* `yellow` (Amarelo)
* `gray` (Cinza)

### 3. Migração Sem Perdas 🛡️
Rodei um script silencioso por trás dos bastidores que pegou todas as opções que você tinha no banco e gravou as cores nelas exatamente conforme você havia me passado na tabela anterior. Portanto, nada mudou visualmente no seu painel para as etiquetas velhas, a única mudança é que você agora tem o poder de alterá-las pela tela!

> [!TIP]
> **Teste rápido:**
> Vá em **Utilitários**, clique em **Editar Sala**, selecione a `A1 ARENA` (que é roxa) e altere a cor dela para `yellow`. Depois volte para o Painel e veja os cartões mudarem de cor magicamente!


---

# 🚀 Walkthrough: O Novo Kanban Moderno

O Kanban passou por uma grande modernização estrutural para ficar mais com a cara de ferramentas consagradas (como o Trello), melhorando tanto o visual quanto o poder de gestão por baixo dos panos. 

Aqui estão as mudanças que você notará a partir de agora:

## 1. 🪟 Tudo agora é Modal (Pop-up)
Em vez daqueles enormes "acordeões" (Expanders) que ficavam no meio da tela poluindo a visão após o uso, agora o sistema interage com você através de janelas nativas flutuantes.
* **Adicionar Cartão:** O botão principal `+ Adicionar Novo Agendamento` chama a tela sobre a página.
* **Editar Cartão:** Ao clicar no emoji de lápis (✏️) na base do cartão, você edita todos os campos no mesmo layout modal flutuante.
* **Mover Cartão:** Ao clicar no emoji de seta (➡️) na base do cartão, você altera rapidamente a coluna em que ele se encontra.

## 2. 🗂️ Múltiplos Diretores e Salas (Multiseleção)
Agora você não está mais restrito a selecionar apenas um diretor ou apenas uma sala por cartão. 
Os campos de "Diretores" e "Salas" na criação e edição do cartão viraram **múltipla escolha**!
* Você pode adicionar 3 diretores e 2 salas simultaneamente.
* O cartão desenhará inteligentemente uma etiqueta independente para cada um, respeitando as cores da nossa regra (Verde escuro / Verde claro).

## 3. 🏷️ Etiquetas (Tags) embutidas no Cartão
O layout do cartão visual no painel também mudou. Toda a caixa possui uma borda nativa limpa, e as etiquetas (Diretores, Salas, Pessoas, Serviços, TI, Carro) agora são desenhadas **dentro da caixa do cartão** de maneira mais limpa e moderna, abandonando aquele aspecto de "texto solto na página" que tínhamos antes.

## 4. ⚙️ Manutenção de "Serviços Adicionais"
A antiga opção "Catering / Copa" foi renomeada para "Serviços Adicionais". Mais importante do que isso: as opções não estão mais travadas no código!
* **Aba Utilitários:** Criamos a tela de manutenção de Serviços Adicionais, exatamente igual às telas de Diretores e Salas.
* Você pode Adicionar, Remover e Editar o nome de opções (como Almoço, Coffee, iFood) por conta própria a qualquer momento.

---
> [!TIP]
> **Como testar agora mesmo:**
> 1. Vá na aba "Painel Kanban".
> 2. Clique em **➕ Adicionar Novo Agendamento**.
> 3. Na janela que abrir, tente selecionar mais de um **Diretor** e mais de uma **Sala**. Salve o cartão.
> 4. Repare que as etiquetas foram separadas por cores direitinho e agora o cartão possui os botões (✏️ e ➡️) embutidos no rodapé!
