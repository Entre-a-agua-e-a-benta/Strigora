# The script of the game goes in this file.

# Define posicao de nome dos personagens
default name_side = "left"
# Define dia incial
default dia = 1
# Define quantas interações pode ter
default interacao = 1
################# Ainda não foi feito sistema de 3 interações por dia terminar o dia ###########

## Variaveis do diálogo com o Vincent
default progressoVincent = 0
default progrediuVincent = False
default ontemVincent = False
default suspeitoVincent = False

## Personagens
define personagens_list = list()
define personagens_dict = dict()
define p = Character("Padre") ## O JOGADOR
define v = Character("Vincent") ## DONO DA ESTALAGEM/TAVERNA
define s = Character("Seren") ## CRIANÇA GEMEA FILHA DO BEBADO
define m = Character("Margarida") ##COSTUREIRA

# The game starts here.

label start:

    show screen HUD

    init python:
        personagens_list = ["Bartolomeu", "Salvatore", "Holga", "Leproso", "Joana", "Margarida", "Agnes", "Bêbado", "Wiliam", "Vincent", "Seren"]
        for personagem in personagens_list:
            personagens_dict[personagem] = [False, 0]

        def alterar_interacao(valor: int):
            global interacao
            interacao = interacao + valor
            if valor >= 0:
                sinal = "+"
            else:
                sinal = ""
            renpy.notify(sinal + str(valor) + " interação")
        
        def checar_interacao():
            global interacao
            #if interacao == 0:
                # jump tela de escolher oq fazer a noite?

        #### Usar a função na tela de escolhas da noite ####
        def passar_dia():
            global dia, interacao, personagens_list, personagens_dict
            dia = dia + 1
            for personagem in personagens_list:
                personagens_dict[personagem][0] = False
            interacao = 3
            renpy.notify("interações restauradas")
            renpy.notify("passou o dia")
            ## jump casa do padre
        
        def progredir(personagem: str):
            global personagens_dict
            personagens_dict[personagem][0] = True
            personagens_dict[personagem][1] += 1

######################################## LOCAIS PELO MAPA ##############################################################

## Cena externa da taverna
label tavernaext:
    call hide_all_screens
    scene bg taverna ext
    call screen tavernaext

## Cena dentro da taverna
label tavernaint:
    call hide_all_screens
    scene bg taverna int
    show screen tavernaint
    call screen vincent_parado

## Cena casa do bebado
label casabebadoext:
    call hide_all_screens
    scene bg casa bebado ext
    call screen casabebado

## Cena quarto do padre dentro da taverna
label casapadre:
    call hide_all_screens
    scene bg casa padre int
    call screen casapadre

## Cena Casa Margarida Ext
label casamargaridaext:
    call hide_all_screens
    scene bg casa curandeira ext
    show screen casaMargaridaEXT
    call screen margarida_parada

label caminholeproso:
    call hide_all_screens
    scene bg casa leproso ext
    call screen casaLeprosoEXT

label caminhobebado_margarida:
    call hide_all_screens
    scene bg caminho curandeira
    call screen caminhobebado_margarida

############# Arruma posição dos personagens dentro do dialogo ###############################
transform padre_left:
    zoom 0.3
    ypos 0.3
    xpos -0.05

transform vincent_right:
    zoom 0.3
    ypos 0.3
    xpos 0.63

transform margarida_right:
    zoom 0.3
    ypos 0.3
    xpos 0.70

######################################## CENAS QUE OCORREM NA TAVERNA #######################################################

## Dialogo com o Vincent ao clicar no personagem
label dialogo_vincent:
    call hide_all_screens
    show screen padre
    p "Buongiorno… Agradeço a hospitalidade, dizem que é perigoso ficar andando de noite por aí… Então me sinto agradecido por ter onde dormir…"
    p "Agora…"
    jump escolhas_vincent
    
label escolhas_vincent:
    show screen padre
    menu:
        "Me conte sobre você" if personagens_dict["Vincent"] == [False, 0]:
            $ progredir("Vincent")
            jump meconte_vincent
        "O que aconteceu com a esposa do seu irmão?" if personagens_dict["Vincent"] == [False, 1] and dia >= 2:
            $ progredir("Vincent")
            jump esposa_vincent
        "Posso falar com a criança?" if personagens_dict["Vincent"] == [False, 2] and dia >= 3:
            $ progredir("Vincent")
            jump crianca_dialogo

        "Onde e o que você fez ontem a noite?":
            if ontemVincent == False:
                jump ontem_vincent
            else:
                jump default_vincent
        "Algum habitante te parece estranho?":
            if suspeitoVincent == False:
                jump suspeito_vincent
            else:
                jump default_vincen
        
        "Passar dia":
            $ passar_dia()
            jump tavernaint

        "Não perguntar nada":
            jump tavernaint

label meconte_vincent:
    #diminui interação do jogador
    $ alterar_interacao(-1)
    show screen vincentN
    v "Bom… Eu sou o Vincent, cuido da taverna e da estalagem… Ou o que sobrou dela, parece que a aldeia resolveu que o medo é  desculpa para parar de beber."
    v "Mas desde que você chegou, tenho limpado o quarto duas vezes por dia, pelo menos um pouco de trabalho para manter a mente ocupada …. "
    v "Não gosto de falar do que não vi com meus próprios olhos. E, pra ser sincero, ultimamente, prefiro ver cada vez menos. Gente demais sussurrando. Portas que antes ficavam abertas agora estão fechadas…"
    v "Mas minha porta… essa fica aberta. Sempre tem quem precise esquecer o que viu. Meu irmão aparece por aqui às vezes… Mas nunca fica muito tempo e nem fala muito."
    show screen padre
    menu:
        "Quem é seu irmão?":
            jump irmao_vincent
            
label irmao_vincent:
    show screen vincentN
    v "Ah, com certeza você vai vê- lo por aí… Ele está sempre pelos cantos da aldeia. Ele vem aqui, bebe sem pagar, mas não tenho coragem de cobrar."
    v "Depois que a mulher dele se foi, sobrou pouco dele também."
    jump tavernaint

label esposa_vincent:
    $ alterar_interacao(-1)
    show screen vincentN
    v "Ela estava grávida…Foi um parto difícil, apenas ela e a parteira dentro do quarto…"
    v "Infelizmente ela não resistiu, mas deu a luz a uma garotinha… Isso faz 10 anos, e desde então ele vive nesse estado… Conspiracionando e dizendo que há culpados pela morte da esposa."

    show screen padre
    menu:
        "E a criança? Onde ela está?":
            jump crianca_vincent
    show screen vincentN
    v "A menina… Bom… Ela está viva, isso é mais do que posso dizer de muita gente…"
    v "Eu cuido dela, mas de um tempo para cá, ela parece doente, às vezes fala coisa dormindo e acorda com febre alta. Eu tento ser como um pai para ela, mas mesmo assim acho que às vezes não sou o suficiente."
    jump tavernaint

label crianca_dialogo:
    show screen padre
    p "Buongiorno, pequena. Deus lhe abençoe, eu gostaria de conversar um pouco com você."
    menu:
        "Me conte sobre você.":
            jump meconte_seren
        "Onde e o que você fez ontem a noite?":
            jump ontem_seren
        "Algum habitante te parece estranho?":
            jump habitante_seren
    return

label ontem_vincent:
    $ ontemvincent = True
    show screen vincentN
    v "Fiz o que faço toda noite. Fechei a estalagem tarde, como sempre. Tinha um bêbado vomitando na entrada e um quarto reservado pro padre…"
    v "Passei a vassoura, contei os barris, limpei as mesas. E quando a lenha terminou, fui buscar mais atrás do depósito. Voltei antes da meia-noite."
    v "Tranquei tudo por dentro. Ninguém entrou depois disso, nem mesmo meu irmão, que vive dizendo que a bebida chama por ele."

    jump tavernaint

label suspeito_vincent:
    $ habitantevincent = True   
    show screen vincentN
    v "Estranhos? Aqui todos andam com o pescoço encolhido, como galinha no fio da faca."
    v "Mas se quer saber… Há alguém que me parece estranho, não sei o nome dele, mas ele mora quase fora da aldeia, isolado com razão. Alguém com o corpo ferido daquele jeito, com certeza boa coisa não fez e agora Deus o castiga pelos seus pecados."
    v "Não o deixo entrar aqui, mas não é pela doença. É por tudo o resto. Por esse silêncio dele que pesa, pelas coisas que diz sem dizer nada. Tem gente que traz má sorte sem precisar levantar a mão."
    jump tavernaint

label default_vincent:
    show screen vincentN
    v "De novo com essa pergunta..."
    jump tavernaint

label meconte_seren:
    s "Olá, me chamo Seren… Tenho dez anos, mas preferia não ter nascido… Desse jeito meu pai seria feliz e minha mãe ainda estaria aqui… Foi minha culpa ela ter morrido antes da hora."
    s "Entendo o jeito que meu pai me olha, quando pensa que não estou vendo. Como se fosse difícil me enxergar… como se visse outra pessoa em mim… Acho que ele nunca me perdoou por isso, nem eu me perdoei…"
    s "Ao menos ele bebe pra esquecer, mas eu lembro por nós dois. Lembro mesmo do que nunca vi… Ainda bem que meu tio me dá pão, me dá coberta, e até me deixa ficar atrás do balcão quando chove."
    s "Ele nunca disse que me ama, mas também nunca me culpou. E isso já é mais do que o suficiente… Mas quando a noite chega… tudo muda… Não é todo sonho que dói. Só os que parecem verdade."
    show screen padre
    menu:
        "Me conte mais sobre esses sonhos":
            jump sonhos_seren

label sonhos_seren:
    s "No começo, eu só via silhuetas. Um campo, uma árvore sozinha, uma sombra me seguindo de longe. Depois vieram os sussurros. E agora, agora… Agora eu vejo tudo…"
    s "No sonho, ando pelas ruas da aldeia com passos que não são meus… As mãos... as mãos que estendo são pequenas, como as minhas. Mas elas brilham. Como brasa acesa no escuro. E quando tocam algo, tudo escurece..."
    s "E o que mais me assusta: há uma voz dentro de mim. Mas ela não fala comigo. Ela me usa… Mas o pior é quando vejo ele… o menino com voz de mulher… Ele fala, mas a boca não mexe… Ele parece viver numa tristeza que me queima..."
    s "Quando acordo, a pele está quente como se eu tivesse corrido por horas. A febre queima atrás dos olhos, e minha garganta parece de vidro."
    s "O tio diz que é só vento, ou comida estragada. Mas toda vez que eu sonho, algo na aldeia amanhece errado.Eu queria contar, gritar... Dizer o que vejo…Mas quem vai acreditar numa menina que até o próprio pai não quis segurar no colo?"
    show screen padre
    menu:
        "Com o que você sonhou ontem?":
            jump sonhoontem_seren
        "Qual foi o seu sonho mais recente?":
            jump sonhoontem_seren
label sonhoontem_seren:
    s "Ontem… ontem no sonho eu estava em frente ao espelho de uma casa grande, e o menino estava dentro do espelho me olhando de volta. Só que, por um instante, os olhos dele eram os meus…"
    jump tavernaint

label ontem_seren:
    s "Fiquei sentada na escada da estalagem, olhando a lua por trás das nuvens. O tio me deu um pedaço de pão com mel… e eu guardei metade. Sempre guardo, caso encontre alguém com mais fome do que eu…"
    s "Depois subi pro quarto, mas não dormi logo. Fiquei ouvindo as vozes lá embaixo. Homens falando alto, rindo… e o padre perguntando coisas. Todo mundo pergunta coisas, ultimamente..."
    s "Quando o salão ficou em silêncio, fechei os olhos. Mas aí o sonho veio…Como se ele me chamasse de algum lugar longe… como se já soubesse onde eu estava."
    jump tavernaint

label habitante_seren:
    s "A dona Margarida me dá arrepios… Não que ela seja má, eu acho. Mas ela olha pras pessoas como se enxergasse o que tem dentro."
    s "Uma vez ela passou por mim e disse: 'Nem todo espelho mostra o que é de fora'. Eu nem entendi, mas senti um calafrio subir nas costas…"
    jump tavernaint

label dialogo_margarida:
    call hide_all_screens
    show screen padre
    p "Buongiorno…"
    show screen margaridaN
    m "A benção, padre. Veio aqui procurar um motivo para jogar a culpa em mim?"
    show screen padre
    p "Não, claro que não. Estou apenas investigando… Fale comigo…"
    jump escolhas_margarida

label escolhas_margarida:
    show screen padre
    menu:
        "Me conte sobre você":
            jump meconte_margarida
        "Onde e o que você fez ontem a noite?":
            jump ontem_margarida
        "Me conte uma história":
            jump historia_margarida

label meconte_margarida:
    show screen margaridaN
    m "Falar pra quê? Já sei o que pensa… Sei o que todos pensam… Vêem uma mulher sozinha, que mexe com coisas que não entendem, e já querem arrastar pra fogueira…"
    m "Chamam-me de contadora de histórias, como se fosse só isso que faço. Talvez seja mesmo… As palavras me obedecem mais do que as pessoas. Conto o que o povo quer ouvir, e escondo o que não estão prontos pra saber."
    m "Já vi mais gente morrer do que você viu nascer. Sei quando a terra tá doente, sei quando o vento muda de cheiro. Sei quando as mãos tremem antes mesmo de tocarem na porta"
    m "Não mexo com mortos. Não falo com sombras. Só aprendi a ouvir o que ninguém mais quer escutar."
    m "Quando o corpo deles falha… Eles veem rastejar até minha porta. Pedem chá e, pomadas. E depois… depois sussurram meu nome como se eu tivesse pacto com a minha própria sombra…"
    m "Hipócritas. Agora que a vila sangra, lembram de mim… Agora… Agora tudo fede a medo e carne podre. Quer caçar uma bruxa? Pois que caçe! Mas olhe direito, porque se me queimar, vai doer. E não só em mim."
    jump casamargaridaext

label ontem_margarida:
    show screen margaridaN
    m "O que eu fiz? O mesmo que faço quando o céu fica quieto demais."
    m "Acendi o fogo, deixei a chaleira cantar... e fiquei escutando… Alguns dormem pra esquecer, eu fico acordada pra lembrar e vigiar. Às vezes, o que a gente precisa ouvir só aparece no silêncio entre um estalo da madeira e outro…"
    jump casamargaridaext

label historia_margarida:
    show screen margaridaN
    m "Já ouviu a história da corça de três olhos? Não? Então sente e escute, ou vá embora de vez…"
    m "Dizem que, certa vez, uma mulher andava sozinha pela mata, cheia de dor e raiva do mundo. Chorava tanto que as árvores taparam os ouvidos. Foi quando encontrou um ninho, entre galhos partidos, com um choro que não era de ave nem de fera…"
    m "Lá dentro? Dois bebês, iguais… Como um espelho. Mas um tinha os olhos fechados e sorria dormindo. O outro tinha os olhos abertos… e não piscava… A mulher, sozinha no mundo, mesmo sabendo que não era seu,  levou um deles nos braços."
    m "Disse que era um sinal... Que o destino havia escolhido aquele pra ela criar, alimentou, deu nome, cobriu de orações… O outro bebe? talvez você se pergunte, o outro… ficou."
    m "Nunca chorou. Nunca morreu. Só ficou ali, esperando… Um dia, a criança levada perguntou quem era seu pai. Ela respondeu: “Um homem que não tem nome e que não pode ser acordado”."
    m "Desde então, a corça de três olhos ronda a aldeia, procurando seu parente perdido."
    m "E que a criança... bom, ela ainda vive entre nós. Só não sabe o que é."
    jump casamargaridaext