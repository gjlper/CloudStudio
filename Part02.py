# 2.9.1
import collections
class Ordered_Attributes(type):
  @classmethod
  def __prepare__(metacls,name,bases,**kwds):
    return collections.OrderedDict()
  def __new__(cls,name,bases,namespace,**kwds):
    result=super().__new__(cls,name,bases,namespace)
    result._order=tuple(n for n in namespace if not n.startswith('__'))
    return result
class Order_Preserved(metaclass=Ordered_Attributes):
  pass
class Something(Order_Preserved):
  this='text'
  def z(self):
    return False
  b='order is preserved'
  a='more text'
# 2.9.2
class Unit:
  """Full name for the unit."""
  factor=1.0
  standard=None # Reference to the appropriate StandardUnit
  name="" # Abbreviation of the unit's name.
  @classmethod
  def value(class_,value):
    if value is None:return None
    return value/class_.factor
  @classmethod
  def convert(class_,value):
    if value is None:return None
    return value*class_.factor
class UnitMeta(type):
  def __new__(cls,name,bases,dict):
    new_class=super().__new__(cls,name,bases,dict)
    new_class.standard=new_class
    return new_class
class Standard_Unit(Unit,metaclass=UnitMeta):
  pass
class INCH(Standard_Unit):
  """Inches"""
  name="in"
class FOOT(Unit):
  """Feet"""
  name="ft"
  standard=INCH
  factor=1/12
class CENTIMETER(Unit):
  """Centimeters"""
  name="cm"
  standard=INCH
  factor=2.54
class METER(Unit):
  """Meters"""
  name="m"
  standard=INCH
  factor=.0254
# 3.1
class Generic:
  pass
# 3.3.3
class RateTimeDistance(dict):
  def __init__(self,*args,**kw):
    super().__init__(*args,**kw)
    self._solve()
  def __getattr__(self,name):
    return self.get(name,None)
  def __setattr__(self,name,value):
    self[name]=value
    self._solve()
  def __dir__(self):
    return list(self.keys())
  def _solve(self):
    if self.rate is not None and self.time is not None:
      self['distance']=self.rate*self.time
    elif self.rate is not None and self.distance is not None:
      self['time']=self.distance/self.rate
    elif self.time is not None and self.distance is not None:
      self['rate']=self.distance/self.time
# 3.5.1
class UnitValue_1:
  """Meausre and Unit combined."""
  def __init__(self,unit):
    self.value=None
    self.unit=unit
    self.default_format="5.2f"
  def __set__(self,instance,value):
    self.value=value
  def __str__(self):
    return "{value:{spec}} {unit}".format(spec=self.default_format,**self.__dict__)
  def __format__(self,spec="5.2f"):
    #print("formatting",spec)
    if spec == "": spec= self.default_format
    return "{value:{spec}} {unit}".format(spec=spec,**self.__dict__)
class RTD_1:
  rate=UnitValue_1("kt")
  time=UnitValue_1("hr")
  distance=UnitValue_1("nm")
  def __init__(self,rate=None,time=None,distance=None):
    if rate is None:
      self.time=time
      self.distance=distance
      self.rate=distance/time
    if time is None:
      self.rate=rate
      self.distance=distance
      self.time=distance/rate
    if distance is None:
      self.rate=rate
      self.time=time
      self.distance=rate*time
  def __str__(self):
    return "rate: {0.rate} time: {0.time} distance: {0.distance}".format(self)
# 3.5.2 使用数据修饰符
class Unit1:
  conversion=1.0
  def __get__(self,instance,owner):
    return instance.kph*self.conversion
  def __set__(self,instance,value):
    instance.kph=value/self.conversion
    print(instance.__class__.__name__)
class Knots(Unit1):
  conversion=0.5399568
class MPH(Unit1):
  conversion=0.62137119
class KPH(Unit1):
  def __get__(self,instance,owner):
    return instance._kph
  def __set__(self,instance,value):
    instance._kph=value
    print('kph',instance.__class__.__name__)
class Measurement:
  kph=KPH()
  knots=Knots()
  mph=MPH()
  def __init__(self,kph=None,mph=None,knots=None):
    if kph:self.kph=kph
    elif mph:self.mph=mph
    elif knots:self.knots=knots
    else:
      raise TypeError
  def __str__(self):
    return "rate: {0.kph} kph = {0.mph} mph = {0.knots} knots".format(self)
if __name__ == '__main__':
  # print(Something._order)
  """x_std=INCH.value(159.625)
  print(FOOT.convert(x_std))
  print(METER.convert(x_std))
  print(METER.factor)"""
  ## 3.3.3
  """rtd=RateTimeDistance(rate=6.3,time=8.25,distance=None)
  print("Rate={rate}, Time={time}, Distance={distance}".format(**rtd))"""
  ## 3.5.1
  """m1=RTD_1(rate=5.8,distance=12)
  print(str(m1))
  print("Time:",m1.time.value,m1.time.unit)"""
  ## 3.5.2
  m2=Measurement(knots=5.9)
  print(str(m2))
  print(m2.kph)
  print(m2.mph)