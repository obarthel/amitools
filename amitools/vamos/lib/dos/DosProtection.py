class DosProtection:
  FIBF_DELETE = 1
  FIBF_EXECUTE = 2
  FIBF_WRITE = 4
  FIBF_READ = 8
  FIBF_ARCHIVE = 16
  FIBF_PURE = 32
  FIBF_SCRIPT = 64
  
  flag_txt = "sparwed"
  
  def __init__(self, mask):
    self.mask = mask
  def __str__(self):
    txt = "[%02x]" % self.mask
    val = 64
    for i in xrange(7):
      if (self.mask ^ 15) & val == 0:
        txt += '-'
      else:
        txt += self.flag_txt[i]
      val >>= 1
    return txt
  def is_set(self, mask):
    return (self.mask ^ 15) & mask != 0
  def set(self, mask):
    self.mask = ((self.mask ^ 15) | mask) ^ 15
  def clr(self, mask):
    self.mask = ((self.mask ^ 15) & ~mask) ^ 15

  def is_d(self):
    return self.is_set(self.FIBF_DELETE)
  def is_e(self):
    return self.is_set(self.FIBF_EXECUTE)
  def is_w(self):
    return self.is_set(self.FIBF_WRITE)
  def is_r(self):
    return self.is_set(self.FIBF_READ)
  def is_s(self):
    return self.is_set(self.FIBF_SCRIPT)
  def is_p(self):
    return self.is_set(self.FIBF_PURE)
