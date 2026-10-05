// Python console worker: runs snippets off the main thread in Pyodide.
// It uses the runtime files published next to the page when they exist (the claude.ai artifact, whose
// sandbox blocks other hosts) and otherwise loads the same version from the public Pyodide CDN (the website).
const base = self.location.href.replace(/[^/]*$/, "");
const CDN = "https://cdn.jsdelivr.net/pyodide/v0.26.4/full/";
let ready = null;

function post(type, text){ self.postMessage({type, text}); }

async function runtimeLocation(){
  try{
    const r = await fetch(base + "pyodide-lock.json");
    // the stdlib zip is published as .wasm next to the page because the artifact host serves no .zip files
    if (r.ok) return {indexURL: base, stdLibURL: base + "python_stdlib.wasm"};
  }catch(err){ /* no local runtime: fall through to the CDN */ }
  return {indexURL: CDN};
}

async function init(){
  const where = await runtimeLocation();
  importScripts(where.indexURL + "pyodide.js");
  const py = await self.loadPyodide(where);
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
