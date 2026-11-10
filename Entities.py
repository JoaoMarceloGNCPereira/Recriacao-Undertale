# entidades.py
from AI_Chat import EnemyAIChat


class Player:

  def __init__(self, x, y, currentHp, maxHp):
    self.x = x
    self.y = y
    self.maxHp = maxHp
    self.currentHp = currentHp

class Enemy:

  def __init__(self, name: str, maxHp, personality: str, threshold: int):
    self.name = name
    self.maxHp = maxHp
    self.currentHp = maxHp
    # Inicializa o cérebro de IA do inimigo
    self.ai_chat = EnemyAIChat(name, personality, threshold)

  def attack(self):
    pass

  def try_to_convince(self, player_message: str, current_hp=None, max_hp=None):
    """Metodo chamado quando o jogador usa o ACT e digita algo."""
    dialogue, score, convinced = self.ai_chat.send_message(
        player_message,
        self.currentHp if current_hp is None else current_hp,
        self.maxHp if max_hp is None else max_hp,
    )
    return dialogue, score, convinced


class Frog(Enemy):

  def __init__(self):
    super().__init__(
        name="Froggit",
        maxHp=100,
        personality=(
            "Você é um sapo assustado e simples. Você só quer pular por aí,"
            " mas foi mandado para lutar. Você é muito fácil de convencer com"
            " elogios ou comida de inseto."
        ),
        threshold=30,  # 30% já basta para ele desistir
    )


class Skeleton(Enemy):

  def __init__(self):
    super().__init__(
        name="Sans-like Skeleton",
        maxHp=120,
        personality=(
            "Você é um esqueleto preguiçoso que prefere fazer piadas ruins do"
            " que lutar. Você desiste se o jogador rir das suas piadas ou"
            " demonstrar cansaço."
        ),
        threshold=50,
    )


class Knight(Enemy):

  def __init__(self):
    super().__init__(
        name="Royal Knight",
        maxHp=180,
        personality=(
            "Você é um cavaleiro estrito e honrado da guarda real. Você leva seu"
            " dever muito a sério e é extremamente cético. É muito difícil te"
            " convencer."
        ),
        threshold=70,  # Exige argumentos sólidos ou honrosos
    )
