import random
# Card类及其子类
class Card:
  insure=False
  def __init__(self,rank,suit,hard,soft):
    self.rank=rank # 字号
    self.suit=suit # 花号
    self.hard=hard # 硬值
    self.soft=soft # 软值
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
  __hash__ = None
class NumberCard(Card):
  def __init__(self,rank,suit):
    super().__init__(str(rank),suit,rank,rank)
class AceCard(Card):
  insure=True
  def __init__(self,rank,suit):
    super().__init__('A',suit,1,11)
class FaceCard(Card):
  def __init__(self,rank,suit):
    super().__init__({11:'J',12:'Q',13:'K'}[rank],suit,10,10)
## Card类接口函数
def card(rank,suit):
  class_={1:AceCard, 11:FaceCard, 12:FaceCard, 13:FaceCard}.get(rank,NumberCard)
  return class_(rank,suit)

# Deck类
class Deck(list):
  def __init__(self):
    super().__init__(card(r+1,s) for r in range(13) for s in ("♣","♦","♥","♠"))
    random.shuffle(self)
## 另一个
class Deck2(list):
  def __init__(self,decks=1):
    super().__init__()
    for i in range(decks):
      self.extend(card(r+1,s) for r in range(13) for s in ("♣","♦","♥","♠"))
      random.shuffle(self)
      burn=random.randint(1,52)
      for i in range(burn):self.pop()

# Hand类
class Hand:
  def __init__(self,dealer_card,*cards):
    self.dealer_card=dealer_card
    self.cards=list(cards)
  def __str__(self):
    return ", ".join(map(str,self.cards))
  def __repr__(self):
    return "{__class__.__name__}({dealer_card!r},{_cards_str})".format(
      __class__=self.__class__,
      _cards_str=", ".join(map(repr,self.cards)),
      **self.__dict__
    )
  def __eq__(self,other):
    if isinstance(other,int):
      return self.total() == other
    try:
      return (self.cards == other.cards and self.dealer_card == other.dealer_card)
    except AttributeError:
      return NotImplemented
  def __lt__(self,other):
    if isinstance(other,int):
      return self.total() < other
    try:
      return self.total() < other.total()
    except AttributeError:
      return NotImplemented
  def __le__(self,other):
    if isinstance(other,int):
      return self.total() <= other
    try:
      return self.total() <= other.total()
    except AttributeError:
      return NotImplemented
  __hash__ = None
  def total(self):
    delta_soft=max(c.soft-c.hard for c in self.cards)
    hard=sum(c.hard for c in self.cards)
    if hard+delta_soft<=21:return hard+delta_soft
    return hard
  # 6.2测试
  def __contains__(self,rank):
    return any(c.rank == rank for c in self.cards)
## 
class Hand1:
  def __str__(self):
    return ", ".join(map(str,self.card))
  def __repr__(self):
    return "{__class__.__name__}({dealer_card!r},{_cards_str})".format(
      __class__=self.__class__,
      _cards_str=", ".join(map(repr,self.card)),
      **self.__dict__
    )
class Hnad_Lazy(Hand1):
  def __init__(self,dealer_card,*cards):
    self.dealer_card=dealer_card
    self._cards=list(cards)
  @property
  def total(self):
    delta_soft=max(c.soft-c.hard for c in self._cards)
    hard_total=sum(c.hard for c in self._cards)
    if hard_total+delta_soft<=21:return hard_total+delta_soft
    return hard_total
  @property
  def card(self):
    return self._cards
  """@card.getter
  def card(self):
    return self._cards[-1]"""
  @card.setter
  def card(self,aCard):
    self._cards.append(aCard)
  @card.deleter
  def card(self):
    self._cards.pop(-1)
  def split(self,deck):
    """Update this hand and also returns the new hand."""
    assert self._cards[0].rank==self._cards[1].rank
    c1=self._cards[-1]
    del self.card
    self.card=deck.pop()
    h_new=self.__class__(self.dealer_card,c1,deck.pop())
    return h_new
class Hand_Eager(Hand1):
  def __init__(self,dealer_card,*cards):
    self.dealer_card=dealer_card
    self.total=0
    self._delta_soft=0
    self._hard_total=0
    self._cards=list()
    for c in cards:
      self.card=c
  @property
  def card(self):
    return self._cards
  @card.setter
  def card(self,aCard):
    self._cards.append(aCard)
    self._delta_soft=max(aCard.soft-aCard.hard,self._delta_soft)
    self._hard_total+=aCard.hard
    self._set_total()
  @card.deleter
  def card(self):
    removed=self._cards.pop(-1)
    self._hard_total-=removed.hard
    # Issue: was the only ace?
    self._delta_soft=max(c.soft-c.hard for c in self._cards)
    self._set_total()
  def _set_total(self):
    if self._hard_total+self._delta_soft<=21:
      self.total=self._hard_total+self._delta_soft
    else:
      self.total=self._hard_total

if __name__ == "__main__":
  #d=Deck()
  """h1=Hnad_Lazy(d.pop(),d.pop(),d.pop())
  h2=Hand_Eager(d.pop(),d.pop(),d.pop())
  print(h1.total)
  print(h2.total)
  print(h1.card)
  h1.card=d.pop()
  print(h1.total)
  del h2.card
  print(h2.total)"""

  """c=d.pop()
  h=Hnad_Lazy(d.pop(),c,c) # Force splittable hand
  h2=h.split(d)
  print(h)
  print(h2)"""
  class Deterministic_Deck:
    def __init__(self,*args,**kw):
      self.args= args
      self.kw=kw
    def __enter__(self):
      self.was= random.getstate()
      random.seed(0,version=1)
      return Deck(*self.args,**self.kw)
    def __exit__(self,exc_type,exc_value,traceback):
      random.setstate(self.was)
with Deterministic_Deck() as d:
  h=Hand(d.pop(),d.pop(),d.pop())
  print('k' in h)