# BattleSystem.py
import threading
import Entities


class BattleSystem:

  def __init__(self, player: Entities.Player, enemy: Entities.Enemy):
    self.player = player
    self.enemy = enemy

    # Estados possíveis: "PLAYER_MENU", "ACT_TALKING", "ENEMY_ATTACK", "VICTORY"
    self.state = "PLAYER_MENU"

    # Controle da IA em background
    self.is_waiting_ai = False
    self.ai_result = None

  def handle_act_action(self, player_input: str):
    """Chamado quando o jogador digita algo no botão ACT."""
    if self.is_waiting_ai:
      return

    self.state = "ACT_TALKING"
    self.is_waiting_ai = True

    def background_task():
      # Pega o HP atual do inimigo (supondo que ele tenha hp e max_hp)
      currentHp = getattr(self.enemy, "currentHp", 100)
      maxHp = getattr(self.enemy, "maxHp", 100)

      dialogue, score, convinced = self.enemy.try_to_convince(
          player_input, currentHp, maxHp
      )
      self.ai_result = {
          "dialogue": dialogue,
          "score": score,
          "convinced": convinced,
      }
      self.is_waiting_ai = False

    # Dispara a thread para não travar o Pygame
    threading.Thread(target=background_task, daemon=True).start()

  def update(self):
    """Atualizado a cada frame no game loop principal."""
    if self.state == "ACT_TALKING" and self.ai_result:
      # A resposta da IA chegou!
      dados = self.ai_result
      print(f"[{self.enemy.name}]: {dados['dialogue']}")

      if dados["convinced"]:
        self.state = "VICTORY"
        print("Batalha vencida pacificamente!")
      else:
        # Passa a vez para o ataque do inimigo (Bullet Hell)
        self.state = "ENEMY_ATTACK"

      self.ai_result = None

  def defense_phase(self):
    """Aqui entraria a lógica da classe Ataque (Bullet Hell)."""
    # Quando o ataque do inimigo acabar, volta para o menu do jogador:
    # self.state = "PLAYER_MENU"
    pass