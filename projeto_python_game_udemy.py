# Projeto Python 1 - Game (udemy)
# Devemos desenvolver uma aplicação onde ao ser inicializada solicite ao usuário escolher o nível de dificuldade do 
# jogo e após isso gera e apresenta, de forma aleatória, um cálculo para que possamos informar o resultado. Iremos 
# limitar as operações em somar, diminuir e multiplicar. Se o usuário acerta a resposta, somará 1 aponto ao seu score. 
# Acertando ou errando, ele poderá ou não continuar o jogo.

import random
import os

def gerar_numero_nao_redondo(min_val, max_val, evitar_cinco=False):
    """
    Gera um número que não é múltiplo de 10 e, se solicitado, não termina com 5
    """
    while True:
        numero = random.randint(min_val, max_val)
        
        # Verifica se é múltiplo de 10 (não permite)
        if numero % 10 == 0:
            continue
        
        # Se for evitar números que terminam com 5
        if evitar_cinco and numero % 10 == 5:
            continue
        
        return numero

def gerar_calculo(nivel):
    """
    Gera um cálculo aleatório baseado no nível de dificuldade
    """
    if nivel == 1:
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        operacoes = ['+', '-']
    elif nivel == 2:
        # Nível médio: números de 10 a 50, sem múltiplos de 10
        num1 = gerar_numero_nao_redondo(10, 50)
        num2 = gerar_numero_nao_redondo(10, 50)
        operacoes = ['+', '-', '*']
    else:  # nível 3
        # Nível difícil: números de 50 a 100, sem múltiplos de 10 e sem terminar com 5
        num1 = gerar_numero_nao_redondo(50, 100, evitar_cinco=True)
        num2 = gerar_numero_nao_redondo(50, 100, evitar_cinco=True)
        operacoes = ['+', '-', '*']
    
    operacao = random.choice(operacoes)
    
    # Garantir que subtrações não resultem em números negativos
    if operacao == '-' and num2 > num1:
        num1, num2 = num2, num1
    
    return num1, num2, operacao

def calcular_resultado(num1, num2, operacao):
    """
    Calcula o resultado da operação matemática
    """
    if operacao == '+':
        return num1 + num2
    elif operacao == '-':
        return num1 - num2
    elif operacao == '*':
        return num1 * num2

def main():
    """
    Função principal do jogo
    """
    score = 0
    
    print("=" * 50)
    print("          JOGO DE CÁLCULOS MATEMÁTICOS")
    print("=" * 50)
    print()
    
    # Solicitar nível de dificuldade
    while True:
        try:
            print("Escolha o nível de dificuldade:")
            print("1 - Fácil (números de 1 a 10, apenas + e -)")
            print("2 - Médio (números de 10 a 50, +, - e × - sem dezenas redondas)")
            print("3 - Difícil (números de 50 a 100, +, - e × - sem dezenas redondas ou terminados em 5)")
            
            nivel = int(input("Digite o número do nível (1-3): "))
            
            if nivel in [1, 2, 3]:
                break
            else:
                print("Por favor, digite um número entre 1 e 3.")
        except ValueError:
            print("Por favor, digite um número válido.")
    
    print(f"\nNível {nivel} selecionado! Vamos começar!\n")
    
    continuar_jogo = True
    
    while continuar_jogo:
        # Gerar cálculo
        num1, num2, operacao = gerar_calculo(nivel)
        
        # Calcular resultado correto
        resultado_correto = calcular_resultado(num1, num2, operacao)
        
        # Exibir cálculo para o usuário
        if operacao == '*':
            simbolo = '×'
        else:
            simbolo = operacao
        
        print(f"Quanto é {num1} {simbolo} {num2}?")
        
        # Solicitar resposta do usuário
        while True:
            try:
                resposta_usuario = int(input("Sua resposta: "))
                break
            except ValueError:
                print("Por favor, digite um número inteiro.")
        
        # Verificar resposta
        if resposta_usuario == resultado_correto:
            score += 1
            print(f"✅ Correto! Seu score: {score}")
        else:
            print(f"❌ Errado! A resposta correta era: {resultado_correto}")
            print(f"Seu score: {score}")
        
        # Perguntar se quer continuar
        while True:
            continuar = input("\nDeseja continuar jogando? (s/n): ").lower().strip()
            if continuar in ['s', 'sim', 'n', 'não', 'nao']:
                break
            else:
                print("Por favor, responda com 's' para sim ou 'n' para não.")
        
        if continuar in ['n', 'não', 'nao']:
            continuar_jogo = False
            print(f"\n🎮 Fim do jogo! Seu score final: {score}")
            print("Obrigado por jogar!")
        else:
            print("-" * 30)
    
    # Perguntar se quer jogar novamente
    while True:
        jogar_novamente = input("\nDeseja jogar novamente? (s/n): ").lower().strip()
        if jogar_novamente in ['s', 'sim', 'n', 'não', 'nao']:
            break
        else:
            print("Por favor, responda com 's' para sim ou 'n' para não.")
    
    if jogar_novamente in ['s', 'sim']:
        os.system('cls' if os.name == 'nt' else 'clear')
        main()

if __name__ == "__main__":
    main()