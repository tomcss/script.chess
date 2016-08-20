#!/usr/bin/ruby

filename = "resources/language/English/strings.po"

value = 0
key = ""

f = open(filename)
f.readlines.each do |line|
  matches = /^msgctxt\s+"#(.*)"\s+#(.*)$/.match( line)
  if not matches.nil? then
    value = matches[1]
    key = "\"#{matches[2]}\"".ljust( 12)
    puts "        #{key}:#{value},"
  end
end
f.close

