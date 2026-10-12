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

function Str(el)
  local pre, num, post = el.text:match("^(.-)#(%d+)(.*)$")
  if num then
    local n = tonumber(num)
    if n >= 1 and n <= 100 then
      return {pandoc.Str(pre), pandoc.Link(pandoc.Str("#" .. num), "#a" .. num), pandoc.Str(post)}
    end
  end
end
