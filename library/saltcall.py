#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json
from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: saltcall
version_added: "0.1"
short_description: wrapper to makina-states salt-call 'saltcaller' script
description:
    - call salt-call
    - thie module can use two modes of execution either by
      using the embedded (and maybe stale) saltcaller script
      or by using the original script on the filesystem if
      present and found.
options:
    function: exec module/fun to call
    args: positional/name args (salt cli formated)

TO maintainers:
    - do not edit saltcall.py but saltcall.py.in
    - run hacking/gen_ansible_saltcaller.py to
      refresh the SALTCALLER SLOT from saltcall.py.in
      and regerenerate saltcall.py
'''

EXAMPLES = '''
- action: saltcall \
        function=state.sls args='["makina-states.cloud.generic.dnsconf"]'
'''

# generated via hacking/gen_ansible_saltcaller.py
# this embeds the saltcaller script inside the ansible module
# but not in plain text as ansible would quote it
SALTCALLER = """
Cgpmcm9tIF9fZnV0dXJlX18gaW1wb3J0IGFic29sdXRlX2ltcG9ydApmcm9tIF9fZnV0dXJlX18g
aW1wb3J0IGRpdmlzaW9uCmZyb20gX19mdXR1cmVfXyBpbXBvcnQgcHJpbnRfZnVuY3Rpb24KJycn
Cgp3cmFwcGVycyB0byBzYWx0IHNoZWxsIGNvbW1hbmRzCj09PT09PT09PT09PT09PT09PT09PT09
PT09PT09PT09PQoKVGhpcyBpcyBub3QgaW5jbHVkZWQgaW4gYSBzYWx0IG1vZHVsZSBhbmQgaXNv
bGF0ZWQgdG8gYmUKcGlja2xhYmxlIGFuZCB1c2VkIHRob3JvdWdoIHB5dGhvbiBtdWx0aXByb2Nl
c3NpbmcgYXMgYSB0YXJnZXQKCgpUaGUgbW9kdWxlIGhhcyByZWR1bmRhbnQgZnVuY3Rpb25zIHdp
dGggdGhlIG1ha2luYS1zdGF0ZXMgY29kZWJhc2UgYnV0IHRoZSBnb2FsIGlzIHRoYXQgaXQgaXMg
c2VsZmNvbnRhaW5lZCBhbmQgZGVwZW5kZW5jeSBsZXNzLgoKJycnCgppbXBvcnQgc2hsZXgKaW1w
b3J0IGFyZ3BhcnNlCmltcG9ydCBjb3B5CmltcG9ydCBjU3RyaW5nSU8KaW1wb3J0IG9zCmltcG9y
dCBwaXBlcwppbXBvcnQgc3VicHJvY2VzcwppbXBvcnQgc3lzCmltcG9ydCBzaXgKaW1wb3J0IHRp
bWUKaW1wb3J0IHRyYWNlYmFjawppbXBvcnQgbG9nZ2luZwppbXBvcnQgZmNudGwKaW1wb3J0IGRh
dGV0aW1lCmltcG9ydCBqc29uCgoKdHJ5OgogICAgaW1wb3J0IGNoYXJkZXQKICAgIEhBU19DSEFS
REVUID0gVHJ1ZQpleGNlcHQgSW1wb3J0RXJyb3I6CiAgICBIQVNfQ0hBUkRFVCA9IEZhbHNlCgoK
X21hcmtlciA9IG9iamVjdCgpCk5PX1JFVFVSTiA9ICdfX0NBTExFUl9OT19SRVRVUk5fXycKTk9S
RVRVUk5fUkVUQ09ERSA9IDUKTk9EQVRBX1JFVENPREUgPSA2Ck5PRElDVF9SRVRDT0RFID0gNwpO
T19JTk5FUl9ESUNUX1JFVENPREUgPSA4ClNUQVRFX1JFVF9JU19OT1RfQV9ESUNUX1JFVENPREUg
PSAxMQpTVEFURV9GQUlMRURfUkVUQ09ERSA9IDkKVElNRU9VVF9SRVRDT0RFID0gLTY2NgpOT19S
RVRDT0RFID0gLTY2OApsb2cgPSBsb2dnaW5nLmdldExvZ2dlcihfX25hbWVfXykKCgpkZWYganNv
bl9sb2FkKGRhdGEpOgogICAgY29udGVudCA9IGRhdGEucmVwbGFjZSgnIC0tLUFOVExJU0xBU0hf
Ti0tLSAnLCAnXG4nKQogICAgY29udGVudCA9IGpzb24ubG9hZHMoY29udGVudCkKICAgIHJldHVy
biBjb250ZW50CgoKZGVmIGpzb25fZHVtcChkYXRhLCBwcmV0dHk9RmFsc2UpOgogICAgaWYgcHJl
dHR5OgogICAgICAgIGNvbnRlbnQgPSBqc29uLmR1bXBzKAogICAgICAgICAgICBkYXRhLCBpbmRl
bnQ9NCwgc2VwYXJhdG9ycz0oJywnLCAnOiAnKSkKICAgIGVsc2U6CiAgICAgICAgY29udGVudCA9
IGpzb24uZHVtcHMoZGF0YSkKICAgICAgICBjb250ZW50ID0gY29udGVudC5yZXBsYWNlKCdcbics
ICcgLS0tQU5UTElTTEFTSF9OLS0tICcpCiAgICByZXR1cm4gY29udGVudAoKCmRlZiBtYWdpY3N0
cmluZyh0aGVzdHIpOgogICAgJycnCiAgICBDb252ZXJ0IGFueSBzdHJpbmcgdG8gVVRGLTggRU5D
T0RFRCBvbmUKICAgICcnJwogICAgaWYgbm90IEhBU19DSEFSREVUOgogICAgICAgIHJldHVybiB0
aGVzdHIKICAgIHNlZWsgPSBGYWxzZQogICAgaWYgKAogICAgICAgIGlzaW5zdGFuY2UodGhlc3Ry
LCAoaW50LCBmbG9hdCwgbG9uZywKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRhdGV0aW1l
LmRhdGUsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICBkYXRldGltZS50aW1lLAogICAgICAg
ICAgICAgICAgICAgICAgICAgICAgZGF0ZXRpbWUuZGF0ZXRpbWUpKQogICAgKToKICAgICAgICB0
aGVzdHIgPSAiezB9Ii5mb3JtYXQodGhlc3RyKQogICAgaWYgaXNpbnN0YW5jZSh0aGVzdHIsIHVu
aWNvZGUpOgogICAgICAgIHRyeToKICAgICAgICAgICAgdGhlc3RyID0gdGhlc3RyLmVuY29kZSgn
dXRmLTgnKQogICAgICAgIGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgIHNlZWsgPSBUcnVl
CiAgICBpZiBzZWVrOgogICAgICAgIHRyeToKICAgICAgICAgICAgZGV0ZWN0ZWRlbmMgPSBjaGFy
ZGV0LmRldGVjdCh0aGVzdHIpLmdldCgnZW5jb2RpbmcnKQogICAgICAgIGV4Y2VwdCBFeGNlcHRp
b246CiAgICAgICAgICAgIGRldGVjdGVkZW5jID0gTm9uZQogICAgICAgIGlmIGRldGVjdGVkZW5j
OgogICAgICAgICAgICBzZGV0ZWN0ZWRlbmMgPSBkZXRlY3RlZGVuYy5sb3dlcigpCiAgICAgICAg
ZWxzZToKICAgICAgICAgICAgc2RldGVjdGVkZW5jID0gJycKICAgICAgICBpZiBzZGV0ZWN0ZWRl
bmMuc3RhcnRzd2l0aCgnaXNvLTg4NTknKToKICAgICAgICAgICAgZGV0ZWN0ZWRlbmMgPSAnSVNP
LTg4NTktMTUnCgogICAgICAgIGZvdW5kX2VuY29kaW5ncyA9IFsKICAgICAgICAgICAgJ0lTTy04
ODU5LTE1JywgJ1RJUy02MjAnLCAnRVVDLUtSJywKICAgICAgICAgICAgJ0VVQy1KUCcsICdTSElG
VF9KSVMnLCAnR0IyMzEyJywgJ3V0Zi04JywgJ2FzY2lpJywKICAgICAgICBdCiAgICAgICAgaWYg
c2RldGVjdGVkZW5jIG5vdCBpbiAoJ3V0Zi04JywgJ2FzY2lpJyk6CiAgICAgICAgICAgIHRyeToK
ICAgICAgICAgICAgICAgIGlmIG5vdCBpc2luc3RhbmNlKHRoZXN0ciwgdW5pY29kZSk6CiAgICAg
ICAgICAgICAgICAgICAgdGhlc3RyID0gdGhlc3RyLmRlY29kZShkZXRlY3RlZGVuYykKICAgICAg
ICAgICAgICAgIHRoZXN0ciA9IHRoZXN0ci5lbmNvZGUoZGV0ZWN0ZWRlbmMpCiAgICAgICAgICAg
IGV4Y2VwdCBFeGNlcHRpb246CiAgICAgICAgICAgICAgICBmb3IgaWR4LCBpIGluIGVudW1lcmF0
ZShmb3VuZF9lbmNvZGluZ3MpOgogICAgICAgICAgICAgICAgICAgIHRyeToKICAgICAgICAgICAg
ICAgICAgICAgICAgaWYgbm90IGlzaW5zdGFuY2UodGhlc3RyLCB1bmljb2RlKSBhbmQgZGV0ZWN0
ZWRlbmM6CiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGVzdHIgPSB0aGVzdHIuZGVjb2Rl
KGRldGVjdGVkZW5jKQogICAgICAgICAgICAgICAgICAgICAgICB0aGVzdHIgPSB0aGVzdHIuZW5j
b2RlKGkpCiAgICAgICAgICAgICAgICAgICAgICAgIGJyZWFrCiAgICAgICAgICAgICAgICAgICAg
ZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICAgICAgICAgICAgICAgICAgaWYgaWR4ID09IChsZW4o
Zm91bmRfZW5jb2RpbmdzKSAtIDEpOgogICAgICAgICAgICAgICAgICAgICAgICAgICAgcmFpc2UK
ICAgIGlmIGlzaW5zdGFuY2UodGhlc3RyLCB1bmljb2RlKToKICAgICAgICB0aGVzdHIgPSB0aGVz
dHIuZW5jb2RlKCd1dGYtOCcpCiAgICB0aGVzdHIgPSB0aGVzdHIuZGVjb2RlKCd1dGYtOCcpLmVu
Y29kZSgndXRmLTgnKQogICAgcmV0dXJuIHRoZXN0cgoKCmRlZiB0ZXJtaW5hdGUocHJvY2Vzcyk6
CiAgICBmb3IgaSBpbiBbJ3Rlcm1pbmF0ZScsICdraWxsJ106CiAgICAgICAgdHJ5OgogICAgICAg
ICAgICBnZXRhdHRyKHByb2Nlc3MsIGkpKCkKICAgICAgICBleGNlcHQgRXhjZXB0aW9uOgogICAg
ICAgICAgICBwYXNzCgoKZGVmIGRvX3ZhbGlkYXRlX3N0YXRlcyhkYXRhLCByZXRjb2RlX3Bhc3N0
aHJvdWdoPU5vbmUsIHJldGNvZGU9Tm9uZSk6CiAgICBpZiBub3QgZGF0YToKICAgICAgICByZXR1
cm4gTk9EQVRBX1JFVENPREUKICAgIGlmIG5vdCBpc2luc3RhbmNlKGRhdGEsIGRpY3QpOgogICAg
ICAgIHJldHVybiBOT0RJQ1RfUkVUQ09ERQogICAgdHJ5OgogICAgICAgICMgaWYgd2Ugc2V0IHJj
X3Bhc3N0aHJvdWdoKGRlZmF1bHQpCiAgICAgICAgIyBhbmQgd2UgZ290IGEgd2VsbCBrbm93biBy
ZXR1cm4gY29kZSwgdGhlbiB1c2UgaXQKICAgICAgICByYyA9IGludChyZXRjb2RlKQogICAgICAg
IGFzc2VydCByYyBpbiBbMCwgMl0gYW5kIHJldGNvZGVfcGFzc3Rocm91Z2gKICAgICAgICByZXR1
cm4gcmMKICAgIGV4Y2VwdCBBc3NlcnRpb25FcnJvcjoKICAgICAgICBwYXNzCiAgICAjIGVsc2Ug
dHJ5IHRvIGdldCBvdXJzZWx2ZXMgaWYgZXZlcnl0aGluZyBkaWQgZ29uZSB3ZWxsCiAgICBmb3Ig
aSwgcmRhdGEgaW4gZGF0YS5pdGVtcygpOgogICAgICAgIGlmIG5vdCBpc2luc3RhbmNlKHJkYXRh
LCBkaWN0KToKICAgICAgICAgICAgcmV0dXJuIE5PX0lOTkVSX0RJQ1RfUkVUQ09ERQogICAgICAg
IGZvciBqLCBzdGF0ZWRhdGEgaW4gcmRhdGEuaXRlbXMoKToKICAgICAgICAgICAgaWYgbm90IGlz
aW5zdGFuY2Uoc3RhdGVkYXRhLCBkaWN0KToKICAgICAgICAgICAgICAgIHJldHVybiBTVEFURV9S
RVRfSVNfTk9UX0FfRElDVF9SRVRDT0RFCiAgICAgICAgICAgIGVsaWYgc3RhdGVkYXRhLmdldCgn
cmVzdWx0JywgTm9uZSkgaXMgRmFsc2U6CiAgICAgICAgICAgICAgICBpZiBub3QgcmV0Y29kZV9w
YXNzdGhyb3VnaDoKICAgICAgICAgICAgICAgICAgICByZXR1cm4gU1RBVEVfRkFJTEVEX1JFVENP
REUKICAgIHJldHVybiAwCgoKZGVmIGZhaWxlZChyZXQsIGVycm9yPU5vbmUpOgogICAgcmV0Wydz
dGF0dXMnXSA9IHJldFsncmV0Y29kZSddID09IDAKICAgIGlmIGVycm9yIGlzIG5vdCBOb25lIGFu
ZCBub3QgcmV0WydzdGF0dXMnXToKICAgICAgICByZXRbJ2Vycm9yJ10gPSBlcnJvcgogICAgaWYg
cmV0WydlcnJvciddOgogICAgICAgIHJldFsnZXJyb3InXSA9IG1hZ2ljc3RyaW5nKHJldFsnZXJy
b3InXSkKICAgIHJldHVybiByZXQKCgpkZWYgbm9uX2Jsb2NrX3JlYWQob3V0cHV0KToKICAgIHRy
eToKICAgICAgICBmZCA9IG91dHB1dC5maWxlbm8oKQogICAgZXhjZXB0IFZhbHVlRXJyb3I6CiAg
ICAgICAgcmV0dXJuICIiCiAgICBlbHNlOgogICAgICAgIGZsID0gZmNudGwuZmNudGwoZmQsIGZj
bnRsLkZfR0VURkwpCiAgICAgICAgZmNudGwuZmNudGwoZmQsIGZjbnRsLkZfU0VURkwsIGZsIHwg
b3MuT19OT05CTE9DSykKICAgICAgICB0cnk6CiAgICAgICAgICAgIHJldHVybiBvdXRwdXQucmVh
ZCgpCiAgICAgICAgZXhjZXB0IEV4Y2VwdGlvbjoKICAgICAgICAgICAgcmV0dXJuICIiCgoKZGVm
IGRvX3Byb2Nlc3NfaW9zKHByb2Nlc3MsCiAgICAgICAgICAgICAgICAgICB2ZXJib3NlPUZhbHNl
LAogICAgICAgICAgICAgICAgICAgb3V0cHV0X291dD1zeXMuc3Rkb3V0LAogICAgICAgICAgICAg
ICAgICAgb3V0cHV0X2Vycj1zeXMuc3RkZXJyLAogICAgICAgICAgICAgICAgICAgc3Rkb3V0X3Bv
cz1Ob25lLAogICAgICAgICAgICAgICAgICAgc3RkZXJyX3Bvcz1Ob25lLAogICAgICAgICAgICAg
ICAgICAgc3Rkb3V0PU5vbmUsCiAgICAgICAgICAgICAgICAgICBzdGRlcnI9Tm9uZSk6CiAgICBp
ZiBzdGRvdXQgaXMgTm9uZToKICAgICAgICBzdGRvdXQgPSBjU3RyaW5nSU8uU3RyaW5nSU8oKQog
ICAgaWYgc3RkZXJyIGlzIE5vbmU6CiAgICAgICAgc3RkZXJyID0gY1N0cmluZ0lPLlN0cmluZ0lP
KCkKICAgIHN0cmVhbXMgPSB7J291dCc6IHN0ZG91dF9wb3MsICdlcnInOiBzdGRlcnJfcG9zfQog
ICAgc3RkbyA9IG5vbl9ibG9ja19yZWFkKHByb2Nlc3Muc3Rkb3V0KQogICAgc3RkZSA9IG5vbl9i
bG9ja19yZWFkKHByb2Nlc3Muc3RkZXJyKQogICAgaWYgc3RkbzoKICAgICAgICBzdGRvdXQud3Jp
dGUoc3RkbykKICAgIGlmIHN0ZGU6CiAgICAgICAgc3RkZXJyLndyaXRlKHN0ZGUpCiAgICBmb3Ig
aywgdmFsLCBvdXQgaW4gKAogICAgICAgICgnb3V0Jywgc3Rkb3V0LmdldHZhbHVlKCksIG91dHB1
dF9vdXQpLAogICAgICAgICgnZXJyJywgc3RkZXJyLmdldHZhbHVlKCksIG91dHB1dF9lcnIpLAog
ICAgKToKICAgICAgICBpZiBub3QgdmFsOgogICAgICAgICAgICBjb250aW51ZQogICAgICAgIHBv
cyA9IHN0cmVhbXNba10KICAgICAgICBucG9zID0gbGVuKHZhbCkgLSAxCiAgICAgICAgaWYgdmFs
IGFuZCAoKHBvcyA9PSAwKSBvciAobnBvcyAhPSBwb3MpKToKICAgICAgICAgICAgaWYgdmVyYm9z
ZToKICAgICAgICAgICAgICAgIG91dC53cml0ZSh2YWxbcG9zOl0pCiAgICAgICAgc3RyZWFtc1tr
XSA9IG5wb3MKICAgIHJldHVybiBzdHJlYW1zWydvdXQnXSwgc3RyZWFtc1snZXJyJ10sIHN0ZG8s
IHN0ZGUKCgpkZWYgZm9ybWF0X2Vycm9yKHJldCk6CiAgICAnJycKICAgIFRvIGF2b2lkIGxhcmdl
IG1lbW9yeSB1c2FnZSwgb25seSBsYXp5IGZvcm1hdCBlcnJvcnMgb24gZGVtYW5kCiAgICAnJycK
ICAgIHJldHVybiAoJycKICAgICAgICAgICAgJ19fU0FMVENBTExFUl9FUlJPUl97cGlkfVxuJwog
ICAgICAgICAgICAne2Vycm9yfVxuJwogICAgICAgICAgICAnX19TQUxUQ0FMTEVSX0VORF9FUlJP
Ul97cGlkfVxuJwogICAgICAgICAgICAnJykuZm9ybWF0KCoqcmV0KQoKCmRlZiBmb3JtYXRfb3V0
cHV0KHJldCk6CiAgICAnJycKICAgIFRvIGF2b2lkIGxhcmdlIG1lbW9yeSB1c2FnZSwgb25seSBs
YXp5IGZvcm1hdCBlcnJvcnMgb24gZGVtYW5kCiAgICAnJycKICAgIHJldHVybiAoJycKICAgICAg
ICAgICAgJ19fU0FMVENBTExFUl9TVERFUlJfe3BpZH1cbicKICAgICAgICAgICAgJ3tzdGRlcnJ9
XG4nCiAgICAgICAgICAgICdfX1NBTFRDQUxMRVJfRU5EX1NUREVSUl97cGlkfVxuJwogICAgICAg
ICAgICAnX19TQUxUQ0FMTEVSX1NURE9VVF97cGlkfVxuJwogICAgICAgICAgICAne3N0ZG91dH1c
bicKICAgICAgICAgICAgJ19fU0FMVENBTExFUl9FTkRfU1RET1VUX3twaWR9XG4nCiAgICAgICAg
ICAgICcnKS5mb3JtYXQoKipyZXQpCgoKZGVmIGZvcm1hdF9vdXRwdXRfYW5kX2Vycm9yKHJldCk6
CiAgICAnJycKICAgIFRvIGF2b2lkIGxhcmdlIG1lbW9yeSB1c2FnZSwgb25seSBsYXp5IGZvcm1h
dCBlcnJvcnMgb24gZGVtYW5kCiAgICAnJycKICAgIHJldHVybiBmb3JtYXRfZXJyb3IocmV0KSAr
IGZvcm1hdF9vdXRwdXQocmV0KQoKCmRlZiBjbWQoYXJncywKICAgICAgICB0aW1lb3V0PU5vbmUs
CiAgICAgICAgc3RkaW49Tm9uZSwKICAgICAgICBzdGRvdXQ9Tm9uZSwKICAgICAgICBzbGVlcF9p
bnRlcnZhbD1Ob25lLAogICAgICAgIHN0ZGVycj1Ob25lLAogICAgICAgIG5vX3F1b3RlPU5vbmUs
CiAgICAgICAgdmVyYm9zZT1Ob25lLAogICAgICAgIGVudj1Ob25lKToKICAgIGlmIG5vdCBzbGVl
cF9pbnRlcnZhbDoKICAgICAgICBzbGVlcF9pbnRlcnZhbCA9IDAuMDQKICAgIGlmIG5vX3F1b3Rl
IGlzIE5vbmU6CiAgICAgICAgbm9fcXVvdGUgPSBGYWxzZQogICAgaWYgbm90IGVudjoKICAgICAg
ICBlbnYgPSB7fQogICAgZW52aXJvbiA9IGNvcHkuZGVlcGNvcHkob3MuZW52aXJvbikKICAgIGVu
dmlyb24udXBkYXRlKGNvcHkuZGVlcGNvcHkoZW52KSkKICAgIG5vdyA9IHRpbWUudGltZSgpCiAg
ICBjbGkgPSBbbWFnaWNzdHJpbmcoYSkgZm9yIGEgaW4gYXJnc10KICAgIG9zcGlkID0gcGlkID0g
b3MuZ2V0cGlkKCkKICAgIGlmIG5vdCBub19xdW90ZToKICAgICAgICBjbGkgPSBbcGlwZXMucXVv
dGUoYSkgZm9yIGEgaW4gY2xpXQogICAgcmV0Y29kZSwgZm9yY2VfcmV0Y29kZSA9IE5vbmUsIE5v
bmUKICAgIHN0ZG91dF9wb3MsIHN0ZGVycl9wb3MgPSBOb25lLCBOb25lCiAgICBlcnJvciA9IE5v
bmUKICAgIGlmIHN0ZG91dCBpcyBOb25lOgogICAgICAgIHN0ZG91dCA9IGNTdHJpbmdJTy5TdHJp
bmdJTygpCiAgICBpZiBzdGRlcnIgaXMgTm9uZToKICAgICAgICBzdGRlcnIgPSBjU3RyaW5nSU8u
U3RyaW5nSU8oKQogICAgcHJvY2VzcyA9IE5vbmUKICAgIHRyeToKICAgICAgICBwcm9jZXNzID0g
c3VicHJvY2Vzcy5Qb3BlbigKICAgICAgICAgICAgY2xpLAogICAgICAgICAgICBlbnY9ZW52LAog
ICAgICAgICAgICBzdGRpbj1zdGRpbiwKICAgICAgICAgICAgc3Rkb3V0PXN1YnByb2Nlc3MuUElQ
RSwKICAgICAgICAgICAgc3RkZXJyPXN1YnByb2Nlc3MuUElQRSkKICAgICAgICB3aGlsZSBUcnVl
OgogICAgICAgICAgICBpZiBwaWQgPT0gb3NwaWQgb3IgcGlkIGlzIE5vbmU6CiAgICAgICAgICAg
ICAgICBwaWQgPSBwcm9jZXNzLnBpZAogICAgICAgICAgICBpZiB0aW1lb3V0IGlzIG5vdCBOb25l
IGFuZCAodGltZS50aW1lKCkgPj0gbm93ICsgdGltZW91dCk6CiAgICAgICAgICAgICAgICB0ZXJt
aW5hdGUocHJvY2VzcykKICAgICAgICAgICAgICAgIGVycm9yID0gKAogICAgICAgICAgICAgICAg
ICAgICdqb2IgdG9vIGxvbmcgdG8gZXhlY3V0ZSwgcHJvY2VzcyB3YXMga2lsbGVkXG4nCiAgICAg
ICAgICAgICAgICAgICAgJyAgezB9JwogICAgICAgICAgICAgICAgKS5mb3JtYXQoY2xpKQogICAg
ICAgICAgICAgICAgZm9yY2VfcmV0Y29kZSA9IFRJTUVPVVRfUkVUQ09ERQogICAgICAgICAgICBl
bHNlOgogICAgICAgICAgICAgICAgcmV0Y29kZSA9IHByb2Nlc3MucG9sbCgpCiAgICAgICAgICAg
ICAgICBzdGRvdXRfcG9zLCBzdGRlcnJfcG9zLCBzdGRvLCBzdGRlID0gZG9fcHJvY2Vzc19pb3Mo
CiAgICAgICAgICAgICAgICAgICAgcHJvY2VzcywgdmVyYm9zZT12ZXJib3NlLAogICAgICAgICAg
ICAgICAgICAgIHN0ZG91dF9wb3M9c3Rkb3V0X3Bvcywgc3RkZXJyX3Bvcz1zdGRlcnJfcG9zLAog
ICAgICAgICAgICAgICAgICAgIHN0ZG91dD1zdGRvdXQsIHN0ZGVycj1zdGRlcnIpCiAgICAgICAg
ICAgIHRpbWUuc2xlZXAoMC4wNCkKICAgICAgICAgICAgaWYgcmV0Y29kZSBpcyBub3QgTm9uZSBv
ciBmb3JjZV9yZXRjb2RlIGlzIG5vdCBOb25lOgogICAgICAgICAgICAgICAgYnJlYWsKICAgIGV4
Y2VwdCAoS2V5Ym9hcmRJbnRlcnJ1cHQsIEV4Y2VwdGlvbikgYXMgZXhjOgogICAgICAgIHRyYWNl
ID0gdHJhY2ViYWNrLmZvcm1hdF9leGMoKQogICAgICAgIHByaW50KHRyYWNlKQogICAgICAgIHRy
eToKICAgICAgICAgICAgdGVybWluYXRlKHByb2Nlc3MpCiAgICAgICAgZXhjZXB0IFVuYm91bmRM
b2NhbEVycm9yOgogICAgICAgICAgICBwYXNzCiAgICAgICAgcmFpc2UgZXhjCiAgICBmaW5hbGx5
OgogICAgICAgIGlmIHByb2Nlc3MgaXMgbm90IE5vbmU6CiAgICAgICAgICAgIHN0ZG91dF9wb3Ms
IHN0ZGVycl9wb3MsIHN0ZG8sIHN0ZGUgPSBkb19wcm9jZXNzX2lvcygKICAgICAgICAgICAgICAg
IHByb2Nlc3MsIHZlcmJvc2U9dmVyYm9zZSwKICAgICAgICAgICAgICAgIHN0ZG91dF9wb3M9c3Rk
b3V0X3Bvcywgc3RkZXJyX3Bvcz1zdGRlcnJfcG9zLAogICAgICAgICAgICAgICAgc3Rkb3V0PXN0
ZG91dCwgc3RkZXJyPXN0ZGVycikKICAgICAgICAgICAgdHJ5OgogICAgICAgICAgICAgICAgdGVy
bWluYXRlKHByb2Nlc3MpCiAgICAgICAgICAgIGV4Y2VwdCBVbmJvdW5kTG9jYWxFcnJvcjoKICAg
ICAgICAgICAgICAgIHBhc3MKICAgIGlmIGZvcmNlX3JldGNvZGUgaXMgbm90IE5vbmU6CiAgICAg
ICAgcmV0Y29kZSA9IGZvcmNlX3JldGNvZGUKICAgIGlmIHJldGNvZGUgaXMgTm9uZToKICAgICAg
ICByZXRjb2RlID0gTk9fUkVUQ09ERQogICAgaWYgcmV0Y29kZSAhPSAwIGFuZCBub3QgZXJyb3I6
CiAgICAgICAgZXJyb3IgPSAncHJvZ3JhbSBlcnJvciwgY2hlY2sgc3RkIHN0cmVhbXMnCiAgICBy
ZXRjb2RlID0gZm9yY2VfcmV0Y29kZSBvciByZXRjb2RlCiAgICByZXQgPSB7J3JldGNvZGUnOiBy
ZXRjb2RlLAogICAgICAgICAgICdzdGF0dXMnOiBOb25lLAogICAgICAgICAgICdlcnJvcic6IE5v
bmUsCiAgICAgICAgICAgJ3BpZCc6IHBpZCwKICAgICAgICAgICAnY2xpJzogJyAnLmpvaW4oY2xp
KSwKICAgICAgICAgICAnc3Rkb3V0Jzogc3Rkb3V0LmdldHZhbHVlKCksCiAgICAgICAgICAgJ3N0
ZGVycic6IHN0ZGVyci5nZXR2YWx1ZSgpfQogICAgZmFpbGVkKHJldCwgZXJyb3I9ZXJyb3IpCiAg
ICBpZiB2ZXJib3NlOgogICAgICAgIHByaW50KGZvcm1hdF9vdXRwdXRfYW5kX2Vycm9yKHJldCkp
CiAgICByZXR1cm4gcmV0CgoKZGVmIGNvbXBsZXhfanNvbl9vdXRwdXRfc2ltcGxlKHN0cmluZyk6
CiAgICAnJycKICAgIEV4dHJhY3QganNvbiBvdXRwdXQgZnJvbSBzdGRvdXQgKHN0cmluZyBwYXJz
ZSB2YXJpYW50KQoKICAgIGlmIHN0YXRlcyBnYXJibGVkIHRoZSBzdGRvdXQsIGJ1dCB3ZSBzdGls
bCBoYXZlIGEgcmVzdWx0IGxpa2U6OgoKICAgICAgICAuLi5jb21tYW5kIGdhcmdhZ2Ugb3V0cHV0
Li4uCiAgICAgICAgeyJsb2NhbCI6IHRydWV9CgogICAgd2Ugd2lsbCB0cnkgdG8gcmVtb3ZlIHRo
ZSBzdGFydGluZyBvdXRwdXQgYW5kIHNvIGV4dHJhY3QKICAgIHRoZSByZXN1bHQgZnJvbSB0aGUg
b3V0cHV0CiAgICAnJycKICAgIGlmIG5vdCBpc2luc3RhbmNlKHN0cmluZywgc2l4LnN0cmluZ190
eXBlcyk6CiAgICAgICAgcmV0dXJuIHN0cmluZwogICAgcmV0ID0gX21hcmtlcgogICAgZm9yIHBv
cywgaSBpbiBlbnVtZXJhdGUoc3RyaW5nKToKICAgICAgICBpZiBpID09ICd7JzoKICAgICAgICAg
ICAgdHJ5OgogICAgICAgICAgICAgICAgcmV0ID0ganNvbi5sb2FkcyhzdHJpbmdbcG9zOl0pCiAg
ICAgICAgICAgICAgICBicmVhawogICAgICAgICAgICBleGNlcHQgVmFsdWVFcnJvcjoKICAgICAg
ICAgICAgICAgIHBhc3MKICAgIGlmIHJldCBpcyBfbWFya2VyOgogICAgICAgIHJhaXNlIFZhbHVl
RXJyb3IoJ0NhbnQgZXh0cmFjdCBqc29uIG91dHB1dCcpCiAgICByZXR1cm4gcmV0CgoKZGVmIGNv
bXBsZXhfanNvbl9vdXRwdXRfbXVsdGlsaW5lcyhzdHJpbmcpOgogICAgJycnCiAgICBFeHRyYWN0
IGpzb24gb3V0cHV0IGZyb20gc3Rkb3V0IChsaW5lcyBwYXJzZSB2YXJpYW50KQoKICAgIGlmIHN0
YXRlcyBnYXJibGVkIHRoZSBzdGRvdXQsIGJ1dCB3ZSBzdGlsbCBoYXZlIGEgcmVzdWx0IGxpa2U6
OgoKICAgICAgICAuLi5jb21tYW5kIGdhcmdhZ2Ugb3V0cHV0Li4uCiAgICAgICAgeyJsb2NhbCI6
IHRydWV9CgogICAgd2Ugd2lsbCB0cnkgdG8gcmVtb3ZlIHRoZSBzdGFydGluZyBvdXRwdXQgYW5k
IHNvIGV4dHJhY3QKICAgIHRoZSByZXN1bHQgZnJvbSB0aGUgb3V0cHV0CiAgICAnJycKICAgIGlm
IG5vdCBpc2luc3RhbmNlKHN0cmluZywgc2l4LnN0cmluZ190eXBlcyk6CiAgICAgICAgcmV0dXJu
IHN0cmluZwogICAgcmV0ID0gX21hcmtlcgogICAgbGluZXMgPSBzdHJpbmcuc3BsaXRsaW5lcygp
CiAgICBmb3IgcG9zLCBsaW5lIGluIGVudW1lcmF0ZShsaW5lcyk6CiAgICAgICAgc2xpbmUgPSBt
YWdpY3N0cmluZyhsaW5lLnN0cmlwKCkpCiAgICAgICAgaWYgc2xpbmUuc3RhcnRzd2l0aCgneycp
OgogICAgICAgICAgICB0cnk6CiAgICAgICAgICAgICAgICByZXQgPSBqc29uLmxvYWRzKCcnLmpv
aW4oW21hZ2ljc3RyaW5nKGEpCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgIGZvciBhIGluIGxpbmVzW3BvczpdXSkpCiAgICAgICAgICAgICAgICBicmVhawogICAgICAg
ICAgICBleGNlcHQgVmFsdWVFcnJvcjoKICAgICAgICAgICAgICAgIHBhc3MKICAgIGlmIHJldCBp
cyBfbWFya2VyOgogICAgICAgIHJhaXNlIFZhbHVlRXJyb3IoJ0NhbnQgZXh0cmFjdCBqc29uIG91
dHB1dCcpCiAgICByZXR1cm4gcmV0CgoKZGVmIGNhbGwoZnVuYywKICAgICAgICAgZXhlY3V0YWJs
ZT1Ob25lLAogICAgICAgICBhcmdzPU5vbmUsCiAgICAgICAgIGxvZ2xldmVsPU5vbmUsCiAgICAg
ICAgIGNvbmZpZ19kaXI9Tm9uZSwKICAgICAgICAgc3RkaW49Tm9uZSwKICAgICAgICAgc3Rkb3V0
PU5vbmUsCiAgICAgICAgIHN0ZGVycj1Ob25lLAogICAgICAgICB0aW1lb3V0PU5vbmUsCiAgICAg
ICAgIG91dHB1dF9xdWV1ZT1Ob25lLAogICAgICAgICB2YWxpZGF0ZV9zdGF0ZXM9Tm9uZSwKICAg
ICAgICAgcmV0Y29kZV9wYXNzdGhyb3VnaD1Ob25lLAogICAgICAgICBub19yZXRjb2RlX3Bhc3N0
aHJvdWdoPU5vbmUsCiAgICAgICAgIG5vX3F1b3RlPU5vbmUsCiAgICAgICAgIHNsZWVwX2ludGVy
dmFsPU5vbmUsCiAgICAgICAgIGxvY2FsPUZhbHNlLAogICAgICAgICBvdXQ9Tm9uZSwKICAgICAg
ICAgbm9fb3V0PU5PX1JFVFVSTiwKICAgICAgICAgbm9fZGlzcGxheV9yZXQ9Tm9uZSwKICAgICAg
ICAgcmV0X2Zvcm1hdD1Ob25lLAogICAgICAgICB2ZXJib3NlPU5vbmUsCiAgICAgICAgIGVudj1O
b25lKToKICAgIGlmIGFyZ3MgaXMgTm9uZToKICAgICAgICBhcmdzID0gW10KICAgIGlmIGlzaW5z
dGFuY2UoYXJncywgc2l4LnN0cmluZ190eXBlcyk6CiAgICAgICAgYXJncyA9IHNobGV4LnNwbGl0
KGFyZ3MpCiAgICBpZiBvdXQgaXMgTm9uZToKICAgICAgICBvdXQgPSAnanNvbicKICAgIGlmIHJl
dF9mb3JtYXQgaXMgTm9uZToKICAgICAgICByZXRfZm9ybWF0ID0gJ2pzb24nCiAgICBpZiB2ZXJi
b3NlIGlzIE5vbmU6CiAgICAgICAgdmVyYm9zZSA9IEZhbHNlCiAgICBpZiBub3QgZXhlY3V0YWJs
ZToKICAgICAgICBleGVjdXRhYmxlID0gJ3NhbHQtY2FsbCcKICAgIGlmIHJldGNvZGVfcGFzc3Ro
cm91Z2ggaXMgTm9uZToKICAgICAgICByZXRjb2RlX3Bhc3N0aHJvdWdoID0gVHJ1ZQogICAgaWYg
bm9fcmV0Y29kZV9wYXNzdGhyb3VnaCBpcyBOb25lOgogICAgICAgIG5vX3JldGNvZGVfcGFzc3Ro
cm91Z2ggPSBGYWxzZQogICAgZWFyZ3MgPSBbXQogICAgaWYgbm9fcmV0Y29kZV9wYXNzdGhyb3Vn
aDoKICAgICAgICByZXRjb2RlX3Bhc3N0aHJvdWdoID0gRmFsc2UKICAgIGZvciB0ZXN0LCBhcmdw
YXJ0IGluIFsKICAgICAgICAoVHJ1ZSwgW2V4ZWN1dGFibGVdKSwKICAgICAgICAobG9jYWwsIFsn
LS1sb2NhbCddKSwKICAgICAgICAocmV0Y29kZV9wYXNzdGhyb3VnaCwgWyctLXJldGNvZGUtcGFz
c3Rocm91Z2gnXSksCiAgICAgICAgKGNvbmZpZ19kaXIsIFsnLWMnLCBjb25maWdfZGlyXSksCiAg
ICAgICAgKGxvZ2xldmVsLCBbJy1sJywgbG9nbGV2ZWxdKSwKICAgICAgICAob3V0LCBbJy0tb3V0
Jywgb3V0XSksCiAgICAgICAgKFRydWUsIFtmdW5jXSArIGFyZ3MpCiAgICBdOgogICAgICAgIGlm
IHRlc3Q6CiAgICAgICAgICAgIGVhcmdzLmV4dGVuZChhcmdwYXJ0KQogICAgcmV0ID0gY21kKGFy
Z3M9ZWFyZ3MsIGVudj1lbnYsIHRpbWVvdXQ9dGltZW91dCwKICAgICAgICAgICAgICB2ZXJib3Nl
PXZlcmJvc2UsCiAgICAgICAgICAgICAgbm9fcXVvdGU9bm9fcXVvdGUsIHNsZWVwX2ludGVydmFs
PXNsZWVwX2ludGVydmFsLAogICAgICAgICAgICAgIHN0ZGluPXN0ZGluLCBzdGRlcnI9c3RkZXJy
LCBzdGRvdXQ9c3Rkb3V0KQogICAgZGVjb2RlcnMgPSB7J2pzb24nOiBqc29uX2xvYWR9CiAgICBl
bmNvZGVycyA9IHsnanNvbic6IChsYW1iZGEgeDoganNvbl9kdW1wKHgsIHByZXR0eT1UcnVlKSl9
CiAgICByZXRbJ3NhbHRfZnVuJ10gPSBmdW5jCiAgICByZXRbJ3NhbHRfYXJncyddID0gYXJncwog
ICAgcmV0WydzYWx0X291dCddID0gTm9uZQogICAgaWYgb3V0IGFuZCBvdXQgaW4gZGVjb2RlcnMg
YW5kIHJldC5nZXQoJ3N0ZG91dCcsICcnKToKICAgICAgICB0cnk6CiAgICAgICAgICAgIGRvdXQg
PSBOb25lCiAgICAgICAgICAgIHRyeToKICAgICAgICAgICAgICAgIGRvdXQgPSBkZWNvZGVyc1tv
dXRdKHJldFsnc3Rkb3V0J10pCiAgICAgICAgICAgIGV4Y2VwdCAoS2V5RXJyb3IsIFZhbHVlRXJy
b3IpOgogICAgICAgICAgICAgICAgaWYgb3V0ID09ICdqc29uJzoKICAgICAgICAgICAgICAgICAg
ICB0cnk6CiAgICAgICAgICAgICAgICAgICAgICAgIGRvdXQgPSBjb21wbGV4X2pzb25fb3V0cHV0
X211bHRpbGluZXMoCiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXRbJ3N0ZG91dCddKQog
ICAgICAgICAgICAgICAgICAgIGV4Y2VwdCAoS2V5RXJyb3IsIFZhbHVlRXJyb3IpOgogICAgICAg
ICAgICAgICAgICAgICAgICBkb3V0ID0gY29tcGxleF9qc29uX291dHB1dF9zaW1wbGUoCiAgICAg
ICAgICAgICAgICAgICAgICAgICAgICByZXRbJ3N0ZG91dCddKQogICAgICAgICAgICAgICAgaWYg
ZG91dCBpcyBOb25lOgogICAgICAgICAgICAgICAgICAgIHJhaXNlCiAgICAgICAgICAgIGlmIGlz
aW5zdGFuY2UoZG91dCwgZGljdCk6CiAgICAgICAgICAgICAgICBpZiAoCiAgICAgICAgICAgICAg
ICAgICAgdmFsaWRhdGVfc3RhdGVzIGlzIG5vdCBGYWxzZSBhbmQKICAgICAgICAgICAgICAgICAg
ICBmdW5jIGluIFsnc3RhdGUuaGlnaHN0YXRlJywgJ3N0YXRlLnNscyddCiAgICAgICAgICAgICAg
ICApOgogICAgICAgICAgICAgICAgICAgIHNyYyA9IGRvX3ZhbGlkYXRlX3N0YXRlcyhkb3V0LAog
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXRjb2RlX3Bhc3N0
aHJvdWdoPXJldGNvZGVfcGFzc3Rocm91Z2gsCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAg
ICAgICAgICAgICAgICAgIHJldGNvZGU9cmV0WydyZXRjb2RlJ10pCiAgICAgICAgICAgICAgICAg
ICAgaWYgc3JjICE9IDAgYW5kIChyZXRbJ3JldGNvZGUnXSA9PSAwKToKICAgICAgICAgICAgICAg
ICAgICAgICAgcmV0WydyZXRjb2RlJ10gPSBzcmMKICAgICAgICAgICAgICAgIGlmIFthIGZvciBh
IGluIGRvdXRdID09IFsnbG9jYWwnXToKICAgICAgICAgICAgICAgICAgICBkb3V0ID0gZG91dFsn
bG9jYWwnXQogICAgICAgICAgICByZXRbJ3NhbHRfb3V0J10gPSBkb3V0CiAgICAgICAgZXhjZXB0
IChLZXlFcnJvciwgVmFsdWVFcnJvcik6CiAgICAgICAgICAgICMgbm8ganNvbiBvdXRwdXQgaXMg
ZXF1aXZhbGVudCBhcyBhIGZhaWxlZCBjYWxsCiAgICAgICAgICAgIHJldFsncmV0Y29kZSddID0g
Tk9SRVRVUk5fUkVUQ09ERQogICAgICAgICAgICBpZiBub3QgcmV0WydlcnJvciddOgogICAgICAg
ICAgICAgICAgcmV0WydlcnJvciddID0gJycKICAgICAgICAgICAgcmV0WydlcnJvciddICs9ICdc
bmZhaWxlZCB0byBkZWNvZGUgcGF5bG9hZCcKICAgIHRyeToKICAgICAgICByZXRjb2RlID0gaW50
KHJldFsncmV0Y29kZSddKQogICAgZXhjZXB0IFZhbHVlRXJyb3I6CiAgICAgICAgcmV0Y29kZSA9
IDY2NgogICAgcmV0WydyZXRjb2RlJ10gPSByZXRjb2RlCiAgICBpZiBvdXRwdXRfcXVldWU6CiAg
ICAgICAgb3V0cHV0X3F1ZXVlLnB1dChyZXQpCiAgICBwaWQgPSBvcy5nZXRwaWQoKQogICAgaWYg
bm90IG5vX2Rpc3BsYXlfcmV0OgogICAgICAgIGVyZXQgPSByZXQKICAgICAgICBpZiByZXRfZm9y
bWF0IGluIGVuY29kZXJzOgogICAgICAgICAgICBlcmV0ID0gZW5jb2RlcnNbcmV0X2Zvcm1hdF0o
ZXJldCkKICAgICAgICBwcmludCgiX19TQUxUQ0FMTEVSX1JFVFVSTl97MH0iLmZvcm1hdChwaWQp
KQogICAgICAgIHByaW50KGVyZXQpCiAgICAgICAgcHJpbnQoIl9fU0FMVENBTExFUl9FTkRfUkVU
VVJOX3swfSIuZm9ybWF0KHBpZCkpCiAgICByZXR1cm4gcmV0CgoKZGVmIG1haW4oKToKICAgIHBh
cnNlciA9IGFyZ3BhcnNlLkFyZ3VtZW50UGFyc2VyKCkKICAgIHBhcnNlci5hZGRfYXJndW1lbnQo
J2Z1bmMnLCBuYXJncz0xLAogICAgICAgICAgICAgICAgICAgICAgICBoZWxwPSdzYWx0IGZ1bmN0
aW9uIHRvIGNhbGwnKQogICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnYXJncycsCiAgICAgICAgICAg
ICAgICAgICAgICAgIG5hcmdzPWFyZ3BhcnNlLlJFTUFJTkRFUiwKICAgICAgICAgICAgICAgICAg
ICAgICAgaGVscD0oJ2Z1bmN0aW9uIGFyZ3VtZW50cyBhcyB5b3Ugd291bGQgdXNlJwogICAgICAg
ICAgICAgICAgICAgICAgICAgICAgICAnIG9uIGNsaSB0byBjYWxsIHNhbHQtY2FsbCcpKQogICAg
cGFyc2VyLmFkZF9hcmd1bWVudCgnLS12YWxpZGF0ZS1zdGF0ZXMnLAogICAgICAgICAgICAgICAg
ICAgICAgICBoZWxwPSgnZm9yIHN0YXRlcyBmdW5jdGlvbiAoc2xzLCBoaWdoc3RhdGUpLCcKICAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgJyBleGlzdCB3aXRoIG5vbi0wIHN0YXR1cyBpbiBj
YXNlIG9mIGVycm9ycycpLAogICAgICAgICAgICAgICAgICAgICAgICBkZWZhdWx0PUZhbHNlLCBh
Y3Rpb249J3N0b3JlX3RydWUnKQogICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnLS1leGVjdXRhYmxl
JykKICAgIHBhcnNlci5hZGRfYXJndW1lbnQoJy1jJywgJy0tY29uZmlnLWRpcicpCiAgICBwYXJz
ZXIuYWRkX2FyZ3VtZW50KCctLXJldC1mb3JtYXQnKQogICAgcGFyc2VyLmFkZF9hcmd1bWVudCgn
LS1sb2NhbCcsCiAgICAgICAgICAgICAgICAgICAgICAgIGhlbHA9J3VzZSAtLWxvY2FsIHdoZW4g
Y2FsbGluZyBzYWx0LWNhbGwnLAogICAgICAgICAgICAgICAgICAgICAgICBhY3Rpb249J3N0b3Jl
X3RydWUnKQogICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnLS1yZXRjb2RlLXBhc3N0aHJvdWdoJywg
ZGVmYXVsdD1Ob25lLAogICAgICAgICAgICAgICAgICAgICAgICBhY3Rpb249J3N0b3JlX3RydWUn
KQogICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnLS1uby1yZXRjb2RlLXBhc3N0aHJvdWdoJywgZGVm
YXVsdD1Ob25lLAogICAgICAgICAgICAgICAgICAgICAgICBhY3Rpb249J3N0b3JlX3RydWUnKQog
ICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnLS1vdXQnLCBkZWZhdWx0PU5vbmUpCiAgICBwYXJzZXIu
YWRkX2FyZ3VtZW50KCctbCcsICctLWxvZ2xldmVsJykKICAgIHBhcnNlci5hZGRfYXJndW1lbnQo
Jy0tdGltZW91dCcsIGRlZmF1bHQ9Tm9uZSwgdHlwZT1pbnQpCiAgICBwYXJzZXIuYWRkX2FyZ3Vt
ZW50KCctLW5vLXF1b3RlJywgYWN0aW9uPSdzdG9yZV90cnVlJywgZGVmYXVsdD1GYWxzZSkKICAg
IHBhcnNlci5hZGRfYXJndW1lbnQoJy12JywgJy0tdmVyYm9zZScsIGFjdGlvbj0nc3RvcmVfdHJ1
ZScsCiAgICAgICAgICAgICAgICAgICAgICAgIGhlbHA9KCdpZiBzZXQsIGRpc3BsYXkgY29tbWFu
ZCBvdXRwdXQgb24gY29uc29sZScpLAogICAgICAgICAgICAgICAgICAgICAgICBkZWZhdWx0PUZh
bHNlKQogICAgcGFyc2VyLmFkZF9hcmd1bWVudCgnLS1uby1kaXNwbGF5LXJldCcsCiAgICAgICAg
ICAgICAgICAgICAgICAgIGhlbHA9KCdEbyBub3QgZGlzcGxheSB0aGUgZnVsbCByZXR1cm4nCiAg
ICAgICAgICAgICAgICAgICAgICAgICAgICAgICcgZnJvbSBwcm9jZXNzIGEgSlNPTiBtZXRhZGF0
YXMnKSwKICAgICAgICAgICAgICAgICAgICAgICAgYWN0aW9uPSdzdG9yZV90cnVlJywgZGVmYXVs
dD1GYWxzZSkKICAgIGFyZ3MgPSBwYXJzZXIucGFyc2VfYXJncygpCiAgICB2b3B0cyA9IHZhcnMo
YXJncykKICAgIHZvcHRzWydmdW5jJ10gPSB2b3B0c1snZnVuYyddWzBdCiAgICByZXR1cm4gY2Fs
bCgqKnZvcHRzKQoKCmlmIF9fbmFtZV9fID09ICdfX21haW5fXycgYW5kIG5vdCBvcy5lbnZpcm9u
LmdldCgnTk9fUFlFWEVDJyk6CiAgICBzeXMuZXhpdChtYWluKClbJ3JldGNvZGUnXSkKCg==
"""


def main():
    changed = False
    executable = None
    for i in ['/srv/makina-states/bin/salt-call']:
        if os.path.exists(i):
            executable = i
            break
    msg = ''
    module = AnsibleModule(
        argument_spec=dict(
            loglevel=dict(required=False, default=None, type='str'),
            function=dict(required=True, default=None, type='str'),
            executable=dict(required=False, default=executable, type='str'),
            local=dict(required=False, default=None, type='bool'),
            args=dict(required=False, default=None, type='str'),
            verbose=dict(required=False, default=False, type='bool'),
            timeout=dict(required=False, default=None, type='int'),
            config_dir=dict(required=False, default=None, type='str'),
        )
    )
    sc = SALTCALLER.decode('base64')
    mod = {}
    if sys.hexversion > 0x03000000:
        exec(compile(sc, '<saltcaller_mod>', 'exec'), mod)
    else:
        exec(compile(sc, '<saltcaller_mod>', 'exec')) in mod
    verbose = module.params.get('verbose')
    function = module.params.get('function')
    fkwargs = {'no_display_ret': True,
               'loglevel': module.params.get('loglevel'),
               'timeout': module.params.get('timeout'),
               'local': module.params.get('local'),
               'executable': module.params.get('executable'),
               'config_dir': module.params.get('config_dir'),
               'args': module.params.get('args')}
    for i in [a for a in fkwargs]:
        if fkwargs[i] is None:
            fkwargs.pop(i, None)
    ret = mod['call'](function, **fkwargs)
    if ret.get('salt_out', None) and not verbose:
        ret['stdout'] = '<TRIMMED>'
        if ret['retcode'] == 0:
            ret['stderr'] = '<TRIMMED>'
    if ret['retcode'] == 0:
        module.exit_json(changed=changed, result=ret)
    else:
        module.fail_json(msg={'msg': 'saltcallerror', 'result': ret})


if __name__ == '__main__':
    main()
# vim:set et sts=4 ts=4 tw=80:
