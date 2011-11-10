"""An example demomstrating a derived StatusMsg class.

Created by nomuus <"".join(["adus@um.ex", "te@rn.um"]).replace(".", "").replace("@", "") + "@" + "nomuus.com">

This will print specially formatted file path status messages
using an overridden StatusMsg.format() virtual method.
"""

__version__ = "1.0"

__copyright__ = """Copyright (c) 2011, nomuus. All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    * Neither the name of the copyright holder nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import sys
from statusmsg import StatusMsg


class path_status(StatusMsg):
    def format(self, kwmsg):
        msg = "(%d): " % kwmsg["count"]
        dot = "..."
        sep = os.sep
        t = kwmsg["msg"]
        
        if self.label_width() > -1:
            label_len = self.label_width()
        else:
            label_len = 0
        max_width = self.max_width
        msg_len = label_len + len(msg)
        tmp_len = msg_len + len(t)
        dot_len = len(dot)
        sep_len = len(sep)
        
        if tmp_len > max_width:
            head, tail = os.path.split(t)
            y = max_width - msg_len - (dot_len + sep_len) - len(tail)
            if y > 0:
                path_short = head[:y] + dot + sep + tail
            else:
                path_short = t[:max_width - msg_len]
        elif tmp_len < max_width:
            path_short = t
        else:
            path_short = ""
        
        return "%s%s" % (msg, path_short)
        
    def set_max_width(self, width):
        if width < 1:
            self.max_width = 79
        else:
            self.max_width = width
        
###########################################################################

def _fake_path_generator(width, max_paths):
    if width < 1:
        width = 79
    if max_paths < 1:
        max_paths = 1000
    
    for x in range(0, max_paths):
        s = "path" * width
        yield "%s%s%s%d.xyz" % (os.sep, s, os.sep, x)

###########################################################################

def main():
    pstatus = path_status(sys.stdout)
    pstatus.set_max_width(79)
    kwmsg = {"msg": "", "count": 0}
    
    pstatus.label("Paths over 79 characters ")
    for f in _fake_path_generator(width=100, max_paths=6000):
        kwmsg["msg"] = f
        kwmsg["count"] = kwmsg["count"] + 1
        pstatus.write(kwmsg)
        pstatus.flush()
    pstatus.label("Paths over 79 characters: Completed\n")
    
    pstatus.label("Paths under 79 characters ")
    kwmsg["count"] = 0
    for f in _fake_path_generator(width=1, max_paths=6000):
        kwmsg["msg"] = f
        kwmsg["count"] = kwmsg["count"] + 1
        pstatus.write(kwmsg)
        pstatus.flush()
    pstatus.label("Paths under 79 characters: Completed\n")
    
###########################################################################

if __name__ == "__main__":
    main()