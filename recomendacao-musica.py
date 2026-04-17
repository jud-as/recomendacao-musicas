import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# 1. Definição das Variáveis (Representação do Conhecimento)
# Entradas: Nível de Energia (0 a 10) e Positividade/Humor (0 a 10)
energia = ctrl.Antecedent(np.arange(0, 11, 1), 'energia')
positividade = ctrl.Antecedent(np.arange(0, 11, 1), 'positividade')

# Saída: Ritmo sugerido em BPM (Batidas por Minuto, de 60 a 180)
ritmo = ctrl.Consequent(np.arange(60, 181, 1), 'ritmo')

# 2. Funções de Pertinência (Lidando com a Incerteza Subjetiva)
energia['baixa'] = fuzz.trimf(energia.universe, [0, 0, 5])
energia['media'] = fuzz.trimf(energia.universe, [3, 5, 8])
energia['alta'] = fuzz.trimf(energia.universe, [6, 10, 10])

positividade['triste'] = fuzz.trimf(positividade.universe, [0, 0, 5])
positividade['neutro'] = fuzz.trimf(positividade.universe, [3, 5, 8])
positividade['feliz'] = fuzz.trimf(positividade.universe, [6, 10, 10])

ritmo['lento'] = fuzz.trimf(ritmo.universe, [60, 60, 100])      # Ex: Lo-Fi, Acústico triste
ritmo['moderado'] = fuzz.trimf(ritmo.universe, [90, 120, 140])  # Ex: Pop tranquilo, Reggae
ritmo['acelerado'] = fuzz.trimf(ritmo.universe, [130, 180, 180])# Ex: Eletrônica, Rock agitado

# 3. Base de Regras (O "Cérebro" do Especialista Musical)
# Se a pessoa está sem energia e triste, sugere música lenta
regra1 = ctrl.Rule(energia['baixa'] & positividade['triste'], ritmo['lento'])
# Se a pessoa está com muita energia e muito feliz, sugere música acelerada
regra2 = ctrl.Rule(energia['alta'] & positividade['feliz'], ritmo['acelerado'])
# Se a pessoa está com energia média, humor neutro
regra3 = ctrl.Rule(energia['media'] & positividade['neutro'], ritmo['moderado'])
# Se a pessoa está com energia alta, mas triste (ex: raiva/frustração)
regra4 = ctrl.Rule(energia['alta'] & positividade['triste'], ritmo['acelerado'])
# Se a pessoa está com energia baixa, mas feliz (ex: relaxando, chill)
regra5 = ctrl.Rule(energia['baixa'] & positividade['feliz'], ritmo['moderado'])

# 4. Criando o Sistema de Controle
sistema_regras = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5])
sistema_recomendacao = ctrl.ControlSystemSimulation(sistema_regras)

# 5. Testando o Sistema (Simulação de um Usuário)
print("--- Sistema Especialista: Recomendação de Música ---")
energia_usuario = 8  # Pessoa bastante animada
positividade_usuario = 9  # Pessoa muito feliz

print(f"Usuário atual -> Energia: {energia_usuario}/10 | Positividade: {positividade_usuario}/10")

# Passando os valores para o sistema
sistema_recomendacao.input['energia'] = energia_usuario
sistema_recomendacao.input['positividade'] = positividade_usuario

# Executando o cálculo matemático fuzzy
sistema_recomendacao.compute()

# Exibindo o resultado
bpm_sugerido = sistema_recomendacao.output['ritmo']
print(f"O BPM (ritmo) sugerido para este estado de espírito é: {bpm_sugerido:.0f} BPM")

# Lógica simples tradicional em cima da saída fuzzy
if bpm_sugerido < 95:
    print("Sugestão de Gênero: Lo-Fi, Indie Folk, Blues ou Clássica.")
elif bpm_sugerido < 135:
    print("Sugestão de Gênero: Pop, R&B, Reggae ou Classic Rock.")
else:
    print("Sugestão de Gênero: EDM, House, K-Pop, Punk ou Heavy Metal.")