-- Pictures (```text) become framed verbatim boxes, diagrams are centred,
-- "Chapter 12" links to that design, and a literal backtick stays a backtick.

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

function Para(el)
  if #el.content == 1 and el.content[1].t == "Image" then
    return {pandoc.RawBlock("latex", "\\begin{center}"), el, pandoc.RawBlock("latex", "\\end{center}")}
  end
end

function Str(el)
  if el.text:find("`", 1, true) then
    local out = {}
    for piece, tick in el.text:gmatch("([^`]*)(`?)") do
      if piece ~= "" then
        table.insert(out, pandoc.Str(piece))
      end
      if tick ~= "" then
        table.insert(out, pandoc.RawInline("latex", "\\textasciigrave{}"))
      end
    end
    return out
  end
end

function Inlines(inlines)
  local i = 1
  while i <= #inlines - 2 do
    local a, b, c = inlines[i], inlines[i + 1], inlines[i + 2]
    if a.t == "Str" and a.text:match("Chapters?$") and b.t == "Space" and c.t == "Str" then
      local num, rest = c.text:match("^(%d+)(.*)$")
      if num and tonumber(num) >= 1 and tonumber(num) <= 50 then
        inlines[i + 2] = pandoc.Link(pandoc.Str(num), "#d" .. num)
        if rest ~= "" then
          table.insert(inlines, i + 3, pandoc.Str(rest))
        end
      end
    end
    i = i + 1
  end
  return inlines
end
