import random
import PySimpleGUI as sg

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

def tela_inicial():
    """
    Tela inicial para escolha do nível
    """
    sg.set_options(font=('Arial', 12))
    
    layout = [
        [sg.Text('JOGO DE CÁLCULOS MATEMÁTICOS', font=('Arial', 16, 'bold'), justification='center')],
        [sg.Text('Escolha o nível de dificuldade:', font=('Arial', 12))],
        [sg.Radio('Fácil - Números de 1 a 10 (apenas + e -)', 'NIVEL', key='-NIVEL1-')],
        [sg.Radio('Médio - Números de 10 a 50 (+, -, ×) - sem dezenas redondas', 'NIVEL', key='-NIVEL2-')],
        [sg.Radio('Difícil - Números de 50 a 100 (+, -, ×) - sem dezenas redondas ou terminados em 5', 'NIVEL', key='-NIVEL3-')],
        [sg.Button('Iniciar Jogo', size=(15, 2)), sg.Button('Sair', size=(15, 2))]
    ]
    
    window = sg.Window('Jogo de Cálculos', layout, element_justification='center')
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED or event == 'Sair':
            window.close()
            return None
        
        if event == 'Iniciar Jogo':
            if values['-NIVEL1-']:
                nivel = 1
            elif values['-NIVEL2-']:
                nivel = 2
            elif values['-NIVEL3-']:
                nivel = 3
            else:
                sg.popup('Por favor, selecione um nível de dificuldade!')
                continue
            
            window.close()
            return nivel

def tela_jogo(nivel):
    """
    Tela principal do jogo
    """
    # Gerar primeiro cálculo
    num1, num2, operacao = gerar_calculo(nivel)
    resultado_correto = calcular_resultado(num1, num2, operacao)
    score = 0
    
    # Layout principal
    layout = [
        [sg.Text(f'Score: {score}', key='-SCORE-', font=('Arial', 14), size=(15, 1))],
        [sg.Text('Quanto é:', font=('Arial', 12))],
        [sg.Text(f'{num1} {operacao} {num2} = ?', key='-CALCULO-', font=('Arial', 18, 'bold'))],
        [sg.Input('', key='-RESPOSTA-', size=(10, 1), font=('Arial', 14), justification='center')],
        [sg.Button('Verificar', size=(10, 2)), sg.Button('Novo Jogo', size=(10, 2))],
        [sg.Text('', key='-FEEDBACK-', text_color='white', size=(30, 2))]
    ]
    
    window = sg.Window('Jogo de Cálculos - Em Andamento', layout, element_justification='center', finalize=True)
    
    # Variáveis de estado do jogo
    jogo_ativo = True
    
    while True:
        event, values = window.read()
        
        if event == sg.WINDOW_CLOSED:
            break
        
        if event == 'Novo Jogo':
            window.close()
            return 'reiniciar'
        
        if event == 'Verificar' and jogo_ativo:
            try:
                resposta = int(values['-RESPOSTA-'])
            except ValueError:
                sg.popup('Por favor, digite um número inteiro válido!')
                continue
            
            if resposta == resultado_correto:
                score += 1
                window['-SCORE-'].update(f'Score: {score}')
                window['-FEEDBACK-'].update('✅ Correto!', text_color='green')
            else:
                window['-FEEDBACK-'].update(f'❌ Errado! Resposta correta: {resultado_correto}', text_color='red')
            
            # Perguntar se quer continuar
            continuar = sg.popup_yes_no('Deseja continuar jogando?', title='Continuar?')
            
            if continuar == 'Yes':
                # Gerar novo cálculo
                num1, num2, operacao = gerar_calculo(nivel)
                resultado_correto = calcular_resultado(num1, num2, operacao)
                window['-CALCULO-'].update(f'{num1} {operacao} {num2} = ?')
                window['-RESPOSTA-'].update('')
                window['-FEEDBACK-'].update('')
            else:
                jogo_ativo = False
                window['-FEEDBACK-'].update(f'🎮 Fim do jogo! Score final: {score}', text_color='yellow')
    
    window.close()
    return 'sair'

def main():
    """
    Função principal do jogo com interface gráfica
    """
    while True:
        # Tela inicial - escolha do nível
        nivel = tela_inicial()
        if nivel is None:
            break
        
        # Loop principal do jogo
        while True:
            resultado = tela_jogo(nivel)
            
            if resultado == 'sair':
                break
            elif resultado == 'reiniciar':
                continue
        
        # Perguntar se quer jogar novamente (após sair do jogo)
        jogar_novamente = sg.popup_yes_no('Deseja jogar novamente?', title='Jogar Novamente?')
        if jogar_novamente != 'Yes':
            break

if __name__ == "__main__":
    main()
    sg.popup('Obrigado por jogar!', title='Até logo!')