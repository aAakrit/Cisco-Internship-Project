Value INTERFACE (\S+)
Value STATUS (\w+)
Value DESCRIPTION (.+)

Start
  ^${INTERFACE}\s+is\s+${STATUS}\s*,\s*line\s+protocol\s+is\s+.* -> StartRecord

StartRecord
  ^\s+Description:\s+\"${DESCRIPTION}\" -> StartRecord
  ^\s+.* -> StartRecord
