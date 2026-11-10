# ai_chat.py
import re
from google import genai
from google.genai import types
import os

class EnemyAIChat:

  def __init__(self, enemy_name: str, personality: str, threshold: int):
    self.enemy_name = enemy_name
    self.threshold = threshold
    self.current_score = 0
    self.is_convinced = False

    SUA_CHAVE_API = os.environ["GEMINI_API_KEY"]
    self.client = genai.Client(api_key=SUA_CHAVE_API)

    # System Prompt atualizado para considerar o HP e a personalidade frente ao perigo
    system_prompt = (
        f"Você é {enemy_name}, um monstro em uma batalha estilo Undertale."
        f" Sua personalidade e objetivos são: {personality}. "
        "O jogador está conversando com você usando o botão ACT para te convencer a parar de lutar. "
        "A cada mensagem, você receberá a sua vida atual (HP). Regra de comportamento sobre o HP: "
        "- Se você for covarde/simples, quanto menos HP você tiver, mais amedrontado você fica, facilitando seu convencimento. "
        "- Se você for sanguinário, orgulhoso ou malvado, quanto menos HP você tiver, mais furioso ou desesperado você fica, tornando-se MAIS DIFÍCIL de convencer (exigindo argumentos muito mais fortes). "
        "A cada resposta, avalie internamente o quão convencido você está de 0 a 100%. "
        "Você DEVE começar obrigatoriamente a sua resposta com uma tag no formato exato: [SCORE: X], onde X é o número de 0 a 100. "
        f"Se o score atingir ou passar de {threshold}%, ceda e declare explicitamente que desistiu da luta."
    )

    self.chat = self.client.chats.create(
        model="gemini-3.8-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.8,
        ),
    )

  def send_message(self, player_input: str, current_hp: int, max_hp: int):
    """Envia a fala do jogador junto com o status de HP atual."""
    if self.is_convinced:
      return (
          f"{self.enemy_name} já desistiu da luta e não quer mais conversar.",
      )

    # Constrói um contexto dinâmico informando o HP atual para a IA
    hp_context = (
        f"[STATUS DE BATALHA - Meu HP: {current_hp}/{max_hp}]"
        f" Jogador disse: {player_input}"
    )

    response = self.chat.send_message(hp_context)
    response_text = response.text

    score_match = re.search(r"\[SCORE:\s*(\d+)\]", response_text)
    if score_match:
      self.current_score = int(score_match.group(1))
      clean_text = re.sub(r"\[SCORE:\s*\d+\]", "", response_text).strip()
    else:
      clean_text = response_text

    if self.current_score >= self.threshold:
      self.is_convinced = True

    return clean_text, self.current_score, self.is_convinced