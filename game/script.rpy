# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

define v = Character("Vincent")
define p = Character("Padre")


# The game starts here.

label start:   

    scene  bg taverna ext
    call screen botao_taverna_entrar

label tavernaint:

    scene bg taverna int
    call screen vincent_parado

label primeiro_dialogo_vincent:

    show padre
    p "Buongiorno… Agradeço a hospitalidade, dizem que é perigoso ficar andando de noite por aí… Então me sinto agradecido por ter onde dormir…"
    p "Agora…"
    
    menu:
        "Me conte sobre você":
            jump escolha1_vincent
        "Onde e o que você fez ontem a noite?":
            return
        "Algum habitante te pareçe estranho?":
            return

label escolha1_vincent:
    v "Bom… Eu sou o Vincent, cuido da taverna e da estalagem… Ou o que sobrou dela, parece que a aldeia resolveu que o medo é  desculpa para parar de beber.  Mas desde que você chegou, tenho limpado o quarto duas vezes por dia, pelo menos um pouco de trabalho para manter a mente ocupada …. "
    v "Não gosto de falar do que não vi com meus próprios olhos. E, pra ser sincero, ultimamente, prefiro ver cada vez menos. Gente demais sussurrando. Portas que antes ficavam abertas agora estão fechadas…"
    v "Mas minha porta… essa fica aberta. Sempre tem quem precise esquecer o que viu. Meu irmão aparece por aqui às vezes… Mas nunca fica muito tempo e nem fala muito."

    menu:
        "Quem é seu irmão?":
            jump irmao_vincent

label irmao_vincent:
    v "Ah, com certeza você vai vê- lo por aí… Ele está sempre pelos cantos da aldeia. Ele vem aqui, bebe sem pagar, mas não tenho coragem de cobrar."
    v "Depois que a mulher dele se foi, sobrou pouco dele também."
    return
