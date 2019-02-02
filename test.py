# Card类
class Card:
  insure=False
  def __init__(self,rank,suit,hard,soft):
    self.rank=rank
    self.suit=suit
    self.hard=hard
    self.soft=soft
  def __repr__(self):
    return "{__class__.__name__}(suit={suit!r},rank={rank!r})".format(__class__=self.__class__,**self.__dict__)
  def __str__(self):
    return "{rank}{suit}".format(**self.__dict__)
  def __lt__(self,other):
    try:
      return self.rank<other.rank
    except AttributeError:
      return NotImplemented
  def __le__(self,other):
    try:
      return self.rank<=other.rank
    except AttributeError:
      return NotImplemented
  def __eq__(self,other):
    try:
      return self.suit == other.suit and self.rank == other.rank
    except AttributeError:
      return NotImplemented
  def __ne__(self,other):
    try:
      return self.suit != other.suit and self.rank != other.rank
    except AttributeError:
      return NotImplemented
  """def __hash__(self):
    return hash(self.suit) ^ hash(self.rank)"""
  __hash__ = None
class NumberCard(Card):
  def __init__(self,rank,suit):
    super().__init__(str(rank),suit,int(rank),int(rank))
class AceCard(Card):
  insure=True
  def __init__(self,rank,suit):
    super().__init__('A',suit,1,11)
class FaceCard(Card):
  def __init__(self,rank,suit):
    # super().__init__({11:'J',12:'Q',13:'K'}[rank],suit,10,10)
    super().__init__({11:'J',12:'Q',13:'K'}.get(rank,str(rank),suit,10,10)
# Hand类
class Hand:
  def __init__(self,dealer_card,*cards):
    self.dealer_card=dealer_card
    self.cards=list(cards)
  def __str__(self):
    return ", ".join(map(str,self.cards))
  def __repr__(self):
    return "{__class__.__name__}({dealer_card!r}, {_cards_str})".format(
      __class__=self.__class__,
      _cards_str=", ".join(map(str,self.cards)),
      **self.__dict__
    )
  def __eq__(self,other):
    return self.cards == other.cards and self.dealer_card == other.dealer_card
  __hash__=None
  def total(self):
    delta_soft=max(c.soft-c.hard for c in self.cards)
    hard=sum(c.hard for c in self.cards)
    if hard+delta_soft<=21:return hard+delta_soft
    return hardace

import sys
class FrozenHand(Hand):
  def __init__(self,*args,**kw):
    if len(args) == 1 and isinstance(arg[0],Hand):
      # Clone a hand
      other=args[0]
      self.dealer_card=other.dealer_card
      self.cards=other.cards
    else:
      # Build a fresh hand
      super().__init__(*args,**kw)
    def __hash__(self):
      h=0
      for c in self.cards:
        h=(h+hash(c)) % sys.hash_info.modules
      return h