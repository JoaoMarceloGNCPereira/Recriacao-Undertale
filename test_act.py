# test_act.py
from Entities import Frog, Knight

# Cria um inimigo para teste
inimigo_atual = Knight()
print(f"Batalha iniciada contra: {inimigo_atual.name}!")
print(f"Meta de convencimento: {inimigo_atual.ai_chat.threshold}%\n")

# Loop de conversa no terminal
while not inimigo_atual.ai_chat.is_convinced:
  acao_jogador = input("Você (ACT): ")

  resposta, score, resolvido = inimigo_atual.try_to_convince(acao_jogador)

  print(f"\n[{inimigo_atual.name}]: {resposta}")
  print(f"-> Progresso de convencimento: {score}%\n")

  if resolvido:
    print(f"🎉 Vitória pacífica! {inimigo_atual.name} desistiu da luta.")