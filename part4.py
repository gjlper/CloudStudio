# 4.7
from abc import ABCMeta,abstractmethod
class AbstractBettingStrategy(metaclass=ABCMeta):
  __slots__=()
  @abstractmethod
  def bet(self,hand):
    return 1
  @abstractmethod
  def record_win(self,hand):
    pass
  #@abstractmethod
  def record_loss(self,hand):
    pass
  @classmethod
  def __subclasshook__(cls,subclass):
    if cls is Hand:
      if(any("bet" in B.__dict__ for B in subclass.__mro__) and any("record_win" in B.__dict__ for B in subclass.__mro__) and any("record_loss" in B.__dict__ for B in subclass.__mro__)):
        return True
    return NotImplemented
class Simple_Broken(AbstractBettingStrategy):
  def bet(self,hand):
    return 1
  def record_win(self,hand):
    pass
# 5.1
import collections.abc
class Power1(collections.abc.Callable):
  def __call__(self,x,n):
    p=1
    for i in range(n):
      p*=x
    return p
# 5.2
class Power4(collections.abc.Callable):
  def __call__(self,x,n):
    if n == 0:return 1
    elif n%2 == 1:
      return self.__call__(x,n-1)*x
    elif n%2 == 0:
      t=self.__call__(x,n/2)
      return t*t
class Power5(collections.abc.Callable):
  def __init__(self):
    self.memo={}
  def __call__(self,x,n):
    if (x,n) not in self.memo:
      if n == 0:
        self.memo[x,n]=1
      elif n%2 == 1:
        self.memo[x,n]=self.__call__(x,n-1)*x
      elif n%2 == 0:
        t=self.__call__(x,n/2)
        self.memo[x,n]= t*t
      else:
        raise Exception("Logic Error")
    return self.memo[x,n]
# 5.4
class BettingStrategy:
  def __init__(self):
    self.win=0
    self.loss=0
  def __call__(self):
    return 1
class BettingMartingale(BettingStrategy):
  def __init__(self):
    self._win= 0
    self._loss= 0
    self.stage= 1
  @property
  def win(self):return self._win
  @win.setter
  def win(self,value):
    self._win= value
    self.stage= 1
  @property
  def loss(self):return self._loss
  @loss.setter
  def loss(self,value):
    self._loss= value
    self.stage*=2
  def __call__(self):
    return self.stage
class BettingMartingale2(BettingStrategy):
  def __init__(self):
    self._win= 0
    self._loss= 0
    self.stage= 1
  def __setattr__(self,name,value):
    if name == "win":
      self.stage=1
    elif name == "loss":
      self.stage*=2
    super().__setattr__(name,value)
  def __call__(self):
    return self.stage
# 5.6
import random
class KnownSequence:
  def __init__(self,seed=0):
    self.seed= 0
  def __enter__(self):
    self.was= random.getstate()
    random.seed(self.seed,version=1)
    return self
  def __exit__(self,exc_type,exc_value,traceback):
    random.setstate(self.was)
# 5.7
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
if __name__ == "__main__":
  """simple=Simple_Broken()"""
  ## 5.1
  """pow1=Power1()
  print(pow1(2,0))
  print(pow1(2,1))"""
  ## 5.2
  """pow5=Power5()
  print(pow5(2,10))"""
  ## 5.6
print(tuple(random.randint(-1,36) for i in range(5)))
with KnownSequence():
  print(tuple(random.randint(-1,36) for i in range(5)))
print(tuple(random.randint(-1,36) for i in range(5)))
with KnownSequence():
  print(tuple(random.randint(-1,36) for i in range(5)))
print(tuple(random.randint(-1,36) for i in range(5)))