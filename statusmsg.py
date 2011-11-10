"""A stream wrapper class to facilitate single-line console status messages.

Created by nomuus <"".join(["adus@um.ex", "te@rn.um"]).replace(".", "").replace("@", "") + "@" + "nomuus.com">

Simple usage example:

    import sys
    from statusmsg import StatusMsg
    from time import sleep

    wait_status = StatusMsg(sys.stdout)
    wait_status.label("10 second wait : ")
    for x in range(1, 10):
      wait_status.write(str(x))
      sleep(1)
      wait_status.flush()
    wait_status.label("10 second wait : Completed\n")
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

class StatusMsg:
    """Prints status messages on single line.

    This will print a status message on a single line and clear
    the line with backspace characters to make it appear as a
    single line status message.
    """
    # TODO(nomuus): Research buffered/unbuffered
    # TODO(nomuus): Change docstrings

    def __init__(self, stream):
        """Initializes the StatusMsg class.
        
        Args:
            stream: stream object such as sys.stdout or sys.stderr.
            
        Raises:
            TypeError if stream is not a TTY.
        """
        if stream.isatty():
            pass
        else:
            raise TypeError("Stream must be TTY (sys.stdout, sys.stderr)")
        
        self._BS = "\x08"
        self._SP = " "
        self._last_width = 0
        self._label_width = -1
        self.stream = stream

    def write(self, kwmsg, auto_flush=False):
        """Writes message to stream (e.g. stdout).
        
        Args:
            kwmsg: message string to be printed to stream.
            auto_flush: boolean that auto-flushes the buffer. (Default=False)
            
        Raises:
            TypeError if kwmsg is not type basestring or dict.
            
        Notes:
            kwmsg can be a string or dictionary object. If kwmsg
            is a dictionary, then the virtual method StatusMsg.format()
            is called. By default, StatusMsg.format() expects the
            dict() object to have a "msg" key. If the method a
            derived class overrides this method, then any keys
            and values can be used accordingly.
        """
        if isinstance(kwmsg, dict):
            msg = self.format(kwmsg)
        elif isinstance(kwmsg, basestring):
            msg = kwmsg
        else:
            raise TypeError("Message must be dict or basestring")
            
        self.stream.write(msg)
        if auto_flush:
            self.flush()
        self._last_width = len(msg)

    def flush(self, _width=-1):
        """Flushes stream buffer with backspace and space characters."""
        if _width < 0:
            _width = self._last_width
        self.stream.flush()
        self.stream.write(self._BS * _width)
        self.stream.write(self._SP * _width)
        self.stream.write(self._BS * _width)

    def last_width(self):
        """Retrieves the width of the last msg.
        
        Returns:
            This returns the width of the last message.
        """
        return self._last_width

    def label(self, s):
        """Prefixes the status message with a fixed label.
        
        Args:
            s: string prefixed to the message.
            
        Notes:
            This method is most beneficial for use with a derived class
            that overrides the StatusMsg.format() method and with code
            that writes multiple status messages to the stream. This method
            maintains a separate width variable than the StatusMsg.write()
            method and thus causes StatusMsg.flush() to not "flush" it from
            the stream.
        """
        if self._label_width < 0:
            self.stream.write(s)
            self._label_width = len(s)
        else:
            self.flush(_width=self._label_width)
            self.stream.write(s)
            self._label_width = -1

    def label_width(self):
        """Retrieves the width of the last label.
        
        Returns:
            This returns the width of the last label.
        """
        return self._label_width

    def reset(self):
        """Reset width variables to defaults."""
        self._last_width = 0
        self._label_width = -1
    
    def format(self, kwmsg):
        """Virtual method to format status message.
        
        This method is used by StatusMsg.write() and is meant
        to be overwritten by a derived class. By default,
        StatusMsg.write() only calls this method if kwmsg
        is a dictionary object.
        """
        return kwmsg["msg"]

###########################################################################