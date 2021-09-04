# [Aniversários](http://danilox.pythonanywhere.com)

<img src="https://github.com/Danilo-Xaxa/aniversarios/blob/main/static/screenshot1.png"/>

<img src="https://github.com/Danilo-Xaxa/aniversarios/blob/main/static/screenshot2.png"/>

[Aniversários](http://danilox.pythonanywhere.com) é uma aplicação web que registra nomes e aniversários de pessoas e manda e-mails personalizados ou padrões desejando feliz aniversário ao aniversariante do dia.

Ao acessar o site, o usuário pode registrar o seu nome, e-mail, dia e mês de nascimento, então a página será recarregada e o registro será adicionado ao banco de dados e à tabela.

Se houver algum aniversariante no dia, será mostrada uma caixa que diz "Hoje é o aniversário de Fulano! Clique aqui para dar os parabéns". Ao clicar, o usuário é redirecionado para uma página que pede o seu nome e diz para escolher uma das duas seguintes opções: "enviar e-mail personalizado" e "enviar e-mail padrão".

O e-mail padrão chegará ao aniversariante como a seguinte mensagem: "Fulano te enviou este e-mail: (mensagem)"

Já o e-mail personalizado, quem digita a mensagem é o usuário. Então o e-mail chegará ao aniversariante como a seguinte mensagem: "Parabéns, Cicrano! Fulano te desejou um feliz aniversário :)"

---

O projeto foi desenvolvido com Python e o framework Flask no back-end e JavaScript puro no front-end. O banco de dados utilizado é o SQLite. Para alguns detalhes de design/layout, o Bootstrap foi utilizado.

A hospedagem foi realizada via PythonAnywhere.

O projeto é inspirado no desafio Birthdays do curso CS50 de Harvard e tem fins apenas educacionais.
