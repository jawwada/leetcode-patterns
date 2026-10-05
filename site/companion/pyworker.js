// Python console worker: loads Pyodide from the files published next to the page and runs snippets off the main thread.
const base = self.location.href.replace(/[^/]*$/, "");
let ready = null;

function post(type, text){ self.postMessage({type, text}); }

async function init(){
  importScripts(base + "pyodide.js");
  // the stdlib zip is published as .wasm because the artifact host serves no .zip files; the loader only reads its bytes
  const py = await self.loadPyodide({indexURL: base, stdLibURL: base + "python_stdlib.wasm"});
  py.setStdout({batched: s => post("out", s + "\n")});
  py.setStderr({batched: s => post("err", s + "\n")});
  // the usual interview imports, ready without typing them
  await py.runPythonAsync("import collections, heapq, bisect, itertools, math, functools, random, string\nfrom collections import deque, defaultdict, Counter, OrderedDict\nfrom typing import List, Optional");
  return py;
}

self.onmessage = async e => {
  const m = e.data;
  if (m.type === "init"){
    ready = init();
    try{ await ready; post("ready", "Python " + (await (await ready).runPythonAsync("import sys; sys.version.split()[0]"))); }
    catch(err){ post("fail", String(err && err.message || err)); }
    return;
  }
  if (m.type === "run"){
    let py;
    try{ py = await ready; }catch(err){ post("fail", String(err && err.message || err)); return; }
    try{
      const r = await py.runPythonAsync(m.code);
      if (r !== undefined && r !== null){
        let s; try{ s = typeof r.toString === "function" ? r.toString() : String(r); }catch(_){ s = String(r); }
        if (r && typeof r.destroy === "function") { try{ r.destroy(); }catch(_){} }
        post("out", s + "\n");
      }
    }catch(err){
      post("err", String(err && err.message || err));
    }
    post("done", "");
  }
};
