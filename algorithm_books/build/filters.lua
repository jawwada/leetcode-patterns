-- Pictures (```text blocks) become framed verbatim boxes; "#41" in prose links to entry 41.

function CodeBlock(el)
  if el.classes[1] == "text" then
    return pandoc.RawBlock("latex",
      "\\begin{PictureVerb}\n" .. el.text .. "\n\\end{PictureVerb}")
  end
end

function Span(el)
  if el.classes[1] == "meta" then
    local out = {pandoc.RawInline("latex", "{\\sffamily\\small\\color{muted}")}
    for _, x in ipairs(el.content) do
      table.insert(out, x)
    end
    table.insert(out, pandoc.RawInline("latex", "}"))
    return out
  end
end

-- A literal backtick in prose would become an opening quote through TeX ligatures.
local function plain(text)
  if not text:find("`", 1, true) then
    return {pandoc.Str(text)}
  end
  local out = {}
  for piece, tick in text:gmatch("([^`]*)(`?)") do
    if piece ~= "" then
      table.insert(out, pandoc.Str(piece))
    end
    if tick ~= "" then
      table.insert(out, pandoc.RawInline("latex", "\\textasciigrave{}"))
    end
  end
  return out
end

function Str(el)
  local pre, num, post = el.text:match("^(.-)#(%d+)(.*)$")
  if num then
    local n = tonumber(num)
    if n >= 1 and n <= 150 then
      local out = plain(pre)
      table.insert(out, pandoc.Link(pandoc.Str("#" .. num), "#a" .. num))
      for _, x in ipairs(plain(post)) do
        table.insert(out, x)
      end
      return out
    end
  end
  if el.text:find("`", 1, true) then
    return plain(el.text)
  end
end
