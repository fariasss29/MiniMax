#!/usr/bin/env python3
from math import inf as infinito
from random import choice as escolher
import platform
import time
from os import system

JOGADOR = -1
PC = +1
tabuleiro = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


def avaliar(estado):
    if venceu(estado, PC):
        pontuacao = +1
    elif venceu(estado, JOGADOR):
        pontuacao = -1
    else:
        pontuacao = 0

    return pontuacao


def venceu(estado, jogador_atual):
    condicoes_vitoria = [
        [estado[0][0], estado[0][1], estado[0][2]],
        [estado[1][0], estado[1][1], estado[1][2]],
        [estado[2][0], estado[2][1], estado[2][2]],
        [estado[0][0], estado[1][0], estado[2][0]],
        [estado[0][1], estado[1][1], estado[2][1]],
        [estado[0][2], estado[1][2], estado[2][2]],
        [estado[0][0], estado[1][1], estado[2][2]],
        [estado[2][0], estado[1][1], estado[0][2]],
    ]
    if [jogador_atual, jogador_atual, jogador_atual] in condicoes_vitoria:
        return True
    else:
        return False


def fim_de_jogo(estado):
    return venceu(estado, JOGADOR) or venceu(estado, PC)


def casas_vazias(estado):
    casas = []

    for x, linha in enumerate(estado):
        for y, casa in enumerate(linha):
            if casa == 0:
                casas.append([x, y])

    return casas


def jogada_valida(x, y):
    if [x, y] in casas_vazias(tabuleiro):
        return True
    else:
        return False


def fazer_jogada(x, y, jogador_atual):
    if jogada_valida(x, y):
        tabuleiro[x][y] = jogador_atual
        return True
    else:
        return False


def minimax(estado, profundidade, jogador_atual):
    if jogador_atual == PC:
        melhor = [-1, -1, -infinito]
    else:
        melhor = [-1, -1, +infinito]

    if profundidade == 0 or fim_de_jogo(estado):
        pontuacao = avaliar(estado)
        return [-1, -1, pontuacao]

    for casa in casas_vazias(estado):
        x, y = casa[0], casa[1]
        estado[x][y] = jogador_atual
        pontuacao = minimax(estado, profundidade - 1, -jogador_atual)
        estado[x][y] = 0
        pontuacao[0], pontuacao[1] = x, y

        if jogador_atual == PC:
            if pontuacao[2] > melhor[2]:
                melhor = pontuacao  # valor máximo
        else:
            if pontuacao[2] < melhor[2]:
                melhor = pontuacao  # valor mínimo

    return melhor


def limpar_tela():
    nome_os = platform.system().lower()
    if 'windows' in nome_os:
        system('cls')
    else:
        system('clear')


def imprimir_tabuleiro(estado, escolha_pc, escolha_jogador):
    simbolos = {
        -1: escolha_jogador,
        +1: escolha_pc,
        0: ' '
    }
    linha_divisoria = '---------------'

    print('\n' + linha_divisoria)
    for linha in estado:
        for casa in linha:
            simbolo = simbolos[casa]
            print(f'| {simbolo} |', end='')
        print('\n' + linha_divisoria)


def jogada_do_pc(escolha_pc, escolha_jogador):
    profundidade = len(casas_vazias(tabuleiro))
    if profundidade == 0 or fim_de_jogo(tabuleiro):
        return

    limpar_tela()
    print(f'Vez do Computador [{escolha_pc}]')
    imprimir_tabuleiro(tabuleiro, escolha_pc, escolha_jogador)

    if profundidade == 9:
        x = escolher([0, 1, 2])
        y = escolher([0, 1, 2])
    else:
        jogada = minimax(tabuleiro, profundidade, PC)
        x, y = jogada[0], jogada[1]

    fazer_jogada(x, y, PC)
    time.sleep(1)


def sua_vez(escolha_pc, escolha_jogador):
    profundidade = len(casas_vazias(tabuleiro))
    if profundidade == 0 or fim_de_jogo(tabuleiro):
        return

    # Dicionário de jogadas válidas
    jogada = -1
    movimentos = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    limpar_tela()
    print(f'Sua vez [{escolha_jogador}]')
    imprimir_tabuleiro(tabuleiro, escolha_pc, escolha_jogador)

    while jogada < 1 or jogada > 9:
        try:
            jogada = int(input('Use o teclado numérico (1..9): '))
            coord = movimentos[jogada]
            pode_jogar = fazer_jogada(coord[0], coord[1], JOGADOR)

            if not pode_jogar:
                print('Jogada inválida! Essa casa já está ocupada.')
                jogada = -1
        except (EOFError, KeyboardInterrupt):
            print('\nFalou! Até a próxima.')
            exit()
        except (KeyError, ValueError):
            print('Opção inválida! Digite um número de 1 a 9.')


def principal():
    limpar_tela()
    escolha_jogador = ''  # X ou O
    escolha_pc = ''  # X ou O
    primeiro = ''  # se o jogador começa

    # Jogador escolhe X ou O para jogar
    while escolha_jogador != 'O' and escolha_jogador != 'X':
        try:
            print('')
            escolha_jogador = input('Escolha X ou O\nSua escolha: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('\nFalou! Até a próxima.')
            exit()
        except (KeyError, ValueError):
            print('Opção inválida!')

    # Configurando a escolha do computador
    if escolha_jogador == 'X':
        escolha_pc = 'O'
    else:
        escolha_pc = 'X'

    # Jogador pode escolher começar primeiro
    limpar_tela()
    while primeiro != 'S' and primeiro != 'N':
        try:
            primeiro = input('Você quer ser o primeiro a jogar? [s/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('\nFalou! Até a próxima.')
            exit()
        except (KeyError, ValueError):
            print('Opção inválida!')

    # Loop principal do jogo
    while len(casas_vazias(tabuleiro)) > 0 and not fim_de_jogo(tabuleiro):
        if primeiro == 'N':
            jogada_do_pc(escolha_pc, escolha_jogador)
            primeiro = ''

        sua_vez(escolha_pc, escolha_jogador)
        jogada_do_pc(escolha_pc, escolha_jogador)

    # Mensagens de fim de jogo
    if venceu(tabuleiro, JOGADOR):
        limpar_tela()
        print(f'Sua vez [{escolha_jogador}]')
        imprimir_tabuleiro(tabuleiro, escolha_pc, escolha_jogador)
        print('VOCÊ VENCEU!')
    elif venceu(tabuleiro, PC):
        limpar_tela()
        print(f'Vez do Computador [{escolha_pc}]')
        imprimir_tabuleiro(tabuleiro, escolha_pc, escolha_jogador)
        print('VOCÊ PERDEU!')
    else:
        limpar_tela()
        imprimir_tabuleiro(tabuleiro, escolha_pc, escolha_jogador)
        print('DEU VELHA!')

    exit()


if __name__ == '__main__':
    principal()