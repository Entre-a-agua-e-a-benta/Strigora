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
    return
