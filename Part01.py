# 1.3
"""class Card:
  def __init__(self,rank,suit):
    self.suit = suit
    self.rank = rank
    self.hard, self.soft = self._points()
  def __repr__(self):
    return "{__class__.__name__}(suit={suit!r}, rank={rank!r})".format(__class__=self.__class__,**self.__dict__)
  def __str__(self):
    return "{rank}{suit}".format(**self.__dict__)
class NumberCard(Card):
  def _points(self):
    return int(self.rank), int(self.rank)
class AceCard(Card):
  def _points(self):
    return 1, 11
class FaceCard(Card):
  def _points(self):
    return 10, 10"""
# 1.4
class Suit:
  def __init__(self, name, symbol):
    self.name = name
    self.symbol = symbol
# 1.5
def card(rank, suit):
  if rank == 1:return AceCard('A',suit)
  elif 2 <= rank < 11:return NumberCard(str(rank),suit)
  elif 11 <= rank < 14:
    name = {11:'J', 12:'Q', 13:'K'}[rank]
    return FaceCard(name, suit)
  else:
    raise Exception("Rank out if range")
# 1.5.1
def card2(rank, suit):
  if rank == 1:return AceCard('A',suit)
  elif 2 <= rank < 11:return NumberCard(str(rank),suit)
  else:
    name = {11:'J', 12:'Q', 13:'K'}[rank]
    return FaceCard(name, suit)
## deck2=[card2(rank,suit) for rank in range(13) for suit in (Club,Diamond,Heart,Spade)]
# 1.5.2
def card3(rank, suit):
  if rank == 1:return AceCard('A',suit)
  elif 2 <= rank < 11:return NumberCard(str(rank),suit)
  elif rank == 11:
    return FaceCard('J',suit)
  elif rank == 12:
    return FaceCard('Q',suit)
  elif rank == 13:
    return FaceCard('K',suit)
  else:
    raise Exception("Rank out if range")
# 1.5.3
def card4(rank,suit):
  class_={1:AceCard, 11:FaceCard, 12:FaceCard, 13:FaceCard}.get(rank,NumberCard)
  return class_(rank,suit)
## 映射牌面值的元组
def card6(rank,suit):
  class_,rank_str={1:(AceCard,'A'),
          11:(FaceCard,'J'),
          12:(FaceCard,'Q'),
          13:(FaceCard,'K'),
          }.get(rank,(NumberCard,str(rank)))
  return class_(rank_str,suit)
## 工厂模式的流畅API设计
class CardFactory:
  def rank(self,rank):
    self.class_, self.rank_str={
      1:(AceCard,'A'),
      11:(FaceCard,'J'),
      12:(FaceCard,'Q'),
      13:(FaceCard,'K'),
    }.get(rank,(NumberCard,str(rank)))
    return self
  def suit(self,suit):
    return self.class_(self.rank_str,suit)
### card8=CardFactory()
### deck8=[card8.rank(r+1).suit(s) for r in range(13) for s in (Club,Diamond,Heart,Spade)]
# 1.6
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
class NumberCard(Card):
  def __init__(self,rank,suit):
    super().__init__(str(rank),suit,int(rank),int(rank))
class AceCard(Card):
  def __init__(self,rank,suit):
    super().__init__('A',suit,1,11)
class FaceCard(Card):
  def __init__(self,rank,suit):
    super().__init__({11:'J',12:'Q',13:'K'}.get(rank,str(rank)),suit,10,10)

def card10(rank,suit):
  if rank == 1:return AceCard(rank,suit)
  elif 2<=rank<11:return NumberCard(rank,suit)
  elif 11<=rank<14:return FaceCard(rank,suit)
  else:
    raise Exception("Rank out of range")
# 1.7.1
import random
class Deck:
  def __init__(self):
    self._cards = [card6(r+1,s) for r in range(13) for s in ("Club","Diamond","Heart","Spade")]
    random.shuffle(self._cards)
  def pop(self):
    return self._cards.pop()
## d=Deck()
## hand=[d.pop(),d.pop()]
# 1.7.2
class Deck2(list):
  def __init__(self):
    super().__init__(card6(r+1,s) for r in range(13) for s in (Club,Diamond,Heart,Spade))
    random.shuffle(self)
# 1.7.3
class Deck3(list):
  def __init__(self,decks=1):
    super().__init__()
    for i in range(decks):
      self.extend(card6(r+1,s) for r in range(13) for s in (Club,Diamond,Heart,Spade))
      random.shuffle(self)
      burn=random.randint(1,52)
      for i in range(burn):self.pop()
# 1.8
class Hand:
  def __init__(self,dealer_card):
    self.dealer_card=dealer_card
    self.cards=[]
  def hard_total(self):
    return sum(c.hard for c in self.cards)
  def soft_total(self):
    return sum(c.soft for c in self.cards)
##
"""
d=Deck()
h=Hand(d.pop())
h.cards.append(d.pop())
h.cards.append(d.pop())
"""
# 1.8
class Hand2:
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
  def hard_total(self):
    return sum(c.hard for c in self.cards)
  def soft_total(self):
    return sum(c.soft for c in self.cards)
  def total(self):
    delta_soft=max(c.soft-c.hard for c in self.cards)
    hard=sum(c.hard for c in self.cards)
    if hard+delta_soft<=21:return hard+delta_soft
    return hard
## d=Deck()
## h=Hand2(d.pop(),d.pop(),d.pop())
# 1.9
class GameStrategy:
  def insurance(self,hand):
    return False
  def split(self,hand):
    return False
  def double(self,hand):
    return False
  def hit(self,hand):
    return sum(c.hand for c in hand.cards) <=17
## dumb = GameStrategy()
# 1.10
class Table:
  def __init__(self):
    self.deck=Deck()
  def place_bet(self,amount):
    pring("Bet",amount)
  def get_hand(self):
    try:
      self.hand=Hand2(d.pop(),d.pop(),d.pop())
      self.hole_card=d.pop()
    except IndexError:
      # Out of cards: need to shuffle.
      self.deck=Deck()
      return self.get_hand()
    print("Deal",self.hand)
    return self.hand
  def can_insure(self,hand):
    return hand.dealer_card.insure

class BettingStrategy:
  def bet(self):
    raise NotImplementedError("No bet method")
  def record_win(self):
    pass
  def record_loss(self):
    pass

class Flat(BettingStrategy):
  def bet(self):
    return 1

import abc
class BettingStrategy2(metaclass=abc.ABCMeta):
  @abc.abstractmethod
  def bet(self):
    return 1
  def record_win(self):
    pass
  def record_loss(self):
    pass
# 1.11
class Hand3:
  def __init__(self,*args,**kw):
    if len(args) == 1 and isinstance(args[0],Hand3):
      # Clone an existing hand; often a bad idea
      other=args[0]
      self.dealer_card=other.dealer_card
      self.cards=other.cards
    else:
      # Build a fresh, new hand.
      dealer_card,*cards=args
      self.dealer_card=dealer_card
      self.cards=list(cards)
## h=Hand(deck.pop(),deck.pop(),deck.pop())
## memento=Hand(h)
# 1.11.1
class Hnad4:
  def __init__(self,*args,**kw):
    if len(args) == 1 and isinstance(args[0],Hand4):
      # Clone an existing hand; often a bad idea
      other=args[0]
      self.dealer_card=other.dealer_card
      self.cards=other.cards
    elif len(args) == 2 and isinstance(args[0],Hand4) and 'split' in kw:
      # Split an existing hand
      other,card=args
      self.dealer_card=other.dealer_card
      self.cards=[other.cards[kw['split']],card]
    elif len(args) == 3:
      # Build a fresh, new hand.
      dealer_card,*cards=args
      self.dealer_card=dealer_card
      self.cards=list(cards)
    else:
      raise TypeError("Invalid constructor args={0!r}".format(args,kw))
  def __str__(self):
    return ", ".join(map(str,self.cards))
##
"""
d=Deck()
h=Hnad4(d.pop(),d.pop(),d.pop())
s1=Hand4(h,d.pop(),split=0)
s2=Hand4(h,d.pop(),split=1)
"""
# 1.11.2
class Hand5:
  def __init__(self,dealer_card,*cards):
    self.dealer_card=dealer_card
    self.cards=list(cards)
    @staticmethod
    def freeze(other):
      hand=Hand5(other.dealer_card,*other.cards)
      return hand
    @staticmethod
    def split(other,card0,card1):
      hand0=Hand5(other.dealer_card,other.cards[0],card0)
      hand1=Hand5(other.dealer_card,other.cards[1],card1)
      return hand0,hand1
    def __str__(self):
      return ", ".join(map(str,self.cards))
## d=Deck()
## h=Hand5(d.pop(),d.pop(),d.pop())
## s1,s2=Hand5.split(h,d.pop(),d.pop())
# 1.12
class Player:
  def __init__(self,table,bet_strategy,game_strategy):
    """Create a new player associated with a table,and configured with proper betting and play strategies
    :param table: an instance of :class:'Table'
    :param bet_strategy: an instance of :class:'BettingStrategy'
    :param game_strategy: an instance of :class:'GameStrategy'
    """
    self.bet_strategy=bet_strategy
    self.game_strategy=game_strategy
    self.table=table
  def game(self):
    self.table.place_bet(self.bet_strategy.bet())
    self.hand=self.table.get_hand()
    if self.table.can_insure(self.hand):
      if self.game_strategy.insurance(self.hand):
        self.table.insure(self.bet_strategy.bet())
    # Yet more... Elided for now
##
"""
table=Table()
flat_bet=Flat()
dumb=GameStrategy()
p=Player(table,flat_bet,dumb)
p.game()
"""
class Player2:
  def __init__(self,**kw):
    """Must provide table, bet_strategy, game_strategy."""
    self.__dict__.update(kw)
  def game(self):
    self.table.place_bet(self.bet_strategy.bet())
    self.hand=self.table.get_hand()
    if self.table.can_insure(self.hand):
      if self.game_strategy.insurance(self.hand):
        self.table.insure(self.bet_strategy.bet())
    # etc.
## p2=Player2(table=table,bet_strategy=flat_bet,game_strategy=dumb)
class Player3(Player):
  def __init__(self,table,bet_strategy,game_strategy,**extras):
    self.bet_strategy=bet_strategy
    self.game_strategy=game_strategy
    self.table=table
    self.__dict__.update(extras)
# 2.3.3
class Card2:
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
  def __eq__(self,other):
    return self.suit == other.suit and self.rank == other.rank
  def __hash__(self):
    return hash(self.suit) ^ hash(self.rank)
class AceCard2(Card2):
  insure=True
  def __init__(self,rank,suit):
    super().__init__('A',suit,1,11)
# 2.3.4
# 2.6.4
