from MemoryRange import MemoryRange
from MemoryStruct import MemoryStruct
from AccessStruct import AccessStruct
from structure.ExecStruct import LibraryDef

import logging

class MemoryLib(MemoryStruct):
  
  op_jmp = 0x4ef9
  
  def __init__(self, name, addr, num_vectors, pos_size, struct=LibraryDef, lib=None, context=None):
    self.lib = lib
    self.ctx = context

    self.num_vectors = num_vectors
    self.pos_size = pos_size
    self.neg_size = num_vectors * 6
    
    self.lib_begin = addr
    self.lib_base  = addr + self.neg_size
    self.lib_end   = self.lib_base + self.pos_size

    MemoryStruct.__init__(self, name, addr, struct, size=self.pos_size + self.neg_size, offset=self.neg_size)
    self.access = AccessStruct(self, struct, struct_addr=self.lib_base)
    
  def __str__(self):
    return "%s base=%06x %s" %(MemoryRange.__str__(self),self.lib_base,str(self.lib))

  def get_lib_base(self):
    return self.lib_base
    
  def get_neg_size(self):
    return self.neg_size
    
  def get_pos_size(self):
    return self.pos_size

  def get_lib(self):
    return self.lib

  def read_mem(self, width, addr):
    # a possible trap?
    if addr < self.lib_base and width == 1:
      val = self.read_mem_int(1,addr)
      # is it trapped?
      if val != self.op_jmp:
        delta = self.lib_base - addr
        off = delta / 6
        addon = "-%d [%d]" % (delta,off)
        self.trace_read(width, addr, val, text="TRAP", level=logging.INFO, addon=addon)
      # native lib jump
      else:
        delta = self.lib_base - addr
        addon = "-%d" % delta
        self.trace_read(width, addr, val, text="JUMP", level=logging.INFO, addon=addon)
      return val
    # no use regular access
    return MemoryStruct.read_mem(self, width, addr)
