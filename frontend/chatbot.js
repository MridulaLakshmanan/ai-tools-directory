/**
 * frontend/chatbot.js  —  RAG Edition (Secure)
 * ----------------------------------------------
 * REPLACE your existing frontend/chatbot.js
 *
 * Security fix: Groq API key removed from frontend entirely.
 * All LLM calls go through a Supabase Edge Function proxy.
 * The key lives server-side as a Supabase secret — never visible in browser.
 *
 * HOW IT WORKS:
 *   Browser → Supabase Edge Function (key lives here) → Groq API
 *
 * Only the Supabase anon key remains here — that's intentional and safe.
 * It's designed to be public and has no write permissions to your data.
 *
 * SETUP (one time):
 *   1. Go to Supabase Dashboard → Edge Functions → ai-advisor → Secrets
 *   2. Add secret:  GROQ_API_KEY = your_groq_key_here
 *   That's it — no keys in any frontend file.
 */

(function () {

  // ── Config — safe to commit, no secrets here ───────────────────────────────
  const SUPABASE_URL  = "https://pjxrjytcurqrmbuhgyoi.supabase.co";
  const SUPABASE_KEY  = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBqeHJqeXRjdXJxcm1idWhneW9pIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjExMjYxNTcsImV4cCI6MjA3NjcwMjE1N30.H5xP2ZlKFl_-h41I_ZjCcGmt0NLK64eOwO8Ipr2sfZQ";

  // Edge Function URL — Groq key lives here as a server-side secret
  const EDGE_FN_URL   = `${SUPABASE_URL}/functions/v1/ai-advisor`;

  const CATEGORIES = [
    "AI Assistants","Image Generation","Video Generation","Development & Code",
    "Writing & Content","Research","Design & Creativity","Audio & Voice",
    "Productivity","Marketing & Social","Learning & Resources",
    "Customer Support & Chat","Document & PDF","Career & HR","Other"
  ];

  // ── State ───────────────────────────────────────────────────────────────────
  let isOpen     = false;
  let isTyping   = false;
  let msgHistory = [];

  // ── CSS ─────────────────────────────────────────────────────────────────────
  const css = `
    #ainai-chat-btn {
      position:fixed; bottom:28px; right:28px;
      width:58px; height:58px; border-radius:50%;
      background:linear-gradient(135deg,#00ffff,#8b5cf6);
      border:none; cursor:pointer; z-index:9998;
      display:flex; align-items:center; justify-content:center; font-size:24px;
      box-shadow:0 4px 20px rgba(0,255,255,0.4);
      animation:ainai-pulse 2.5s ease-in-out infinite;
      transition:transform .2s;
    }
    #ainai-chat-btn:hover{transform:scale(1.1)}
    @keyframes ainai-pulse{
      0%,100%{box-shadow:0 4px 20px rgba(0,255,255,0.4),0 0 0 0 rgba(0,255,255,0.25)}
      50%{box-shadow:0 4px 20px rgba(0,255,255,0.4),0 0 0 12px rgba(0,255,255,0)}
    }
    .ainai-badge{
      position:absolute; top:-3px; right:-3px;
      background:#f472b6; color:#fff; font-size:9px; font-weight:700;
      width:18px; height:18px; border-radius:50%;
      display:flex; align-items:center; justify-content:center;
      border:2px solid #0a0a0a;
    }
    #ainai-win{
      position:fixed; bottom:100px; right:28px;
      width:400px; max-width:calc(100vw - 36px);
      height:580px; max-height:calc(100vh - 130px);
      background:linear-gradient(160deg,#09090f,#0e0e1c);
      border:1px solid rgba(0,255,255,0.2); border-radius:20px;
      display:flex; flex-direction:column; z-index:9999; overflow:hidden;
      box-shadow:0 20px 60px rgba(0,0,0,0.75),0 0 0 1px rgba(0,255,255,0.07);
      transform:scale(0.88) translateY(16px); opacity:0; pointer-events:none;
      transition:all .3s cubic-bezier(0.34,1.56,0.64,1);
    }
    #ainai-win.open{transform:scale(1) translateY(0);opacity:1;pointer-events:all}
    .ainai-hdr{
      padding:14px 18px;
      background:linear-gradient(90deg,rgba(0,255,255,0.07),rgba(139,92,246,0.07));
      border-bottom:1px solid rgba(0,255,255,0.1);
      display:flex; align-items:center; gap:10px; flex-shrink:0;
    }
    .ainai-hdr-av{
      width:36px; height:36px; border-radius:50%;
      background:rgba(0,255,255,0.1); border:1px solid rgba(0,255,255,0.25);
      display:flex; align-items:center; justify-content:center; font-size:16px;
    }
    .ainai-hdr-info{flex:1}
    .ainai-hdr-info h4{margin:0;color:#00ffff;font-size:13px;font-weight:600}
    .ainai-hdr-info p{margin:0;font-size:11px;color:rgba(255,255,255,0.4)}
    .ainai-dot{width:7px;height:7px;background:#10b981;border-radius:50%;
      display:inline-block;margin-right:4px;animation:ainai-blink 2s infinite}
    @keyframes ainai-blink{0%,100%{opacity:1}50%{opacity:0.3}}
    .ainai-x{background:none;border:none;color:rgba(255,255,255,0.4);
      cursor:pointer;font-size:16px;padding:4px 6px;border-radius:6px;transition:all .2s}
    .ainai-x:hover{color:#fff;background:rgba(255,255,255,0.08)}
    .ainai-msgs{
      flex:1; overflow-y:auto; padding:14px;
      display:flex; flex-direction:column; gap:10px;
      scrollbar-width:thin; scrollbar-color:rgba(0,255,255,0.15) transparent;
    }
    .ainai-msgs::-webkit-scrollbar{width:3px}
    .ainai-msgs::-webkit-scrollbar-thumb{background:rgba(0,255,255,0.15);border-radius:3px}
    .ainai-msg{display:flex;gap:8px;align-items:flex-start;animation:ainai-pop .25s ease-out}
    .ainai-msg.u{flex-direction:row-reverse}
    @keyframes ainai-pop{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
    .ainai-av{
      width:26px;height:26px;border-radius:50%;flex-shrink:0;
      display:flex;align-items:center;justify-content:center;font-size:12px;
    }
    .ainai-msg.b .ainai-av{background:rgba(0,255,255,0.08);border:1px solid rgba(0,255,255,0.2)}
    .ainai-msg.u .ainai-av{background:linear-gradient(135deg,#8b5cf6,#f472b6)}
    .ainai-bub{
      max-width:82%;padding:10px 13px;border-radius:14px;
      font-size:13px;line-height:1.55;color:rgba(255,255,255,0.88);
    }
    .ainai-msg.b .ainai-bub{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.07);border-bottom-left-radius:4px}
    .ainai-msg.u .ainai-bub{background:linear-gradient(135deg,rgba(0,255,255,0.1),rgba(139,92,246,0.1));border:1px solid rgba(0,255,255,0.18);border-bottom-right-radius:4px}
    .ainai-rag-tag{display:inline-flex;align-items:center;gap:4px;font-size:10px;color:rgba(0,255,255,0.45);margin-bottom:6px}
    .ainai-cat{
      display:inline-flex;align-items:center;gap:5px;
      background:rgba(139,92,246,0.12);border:1px solid rgba(139,92,246,0.28);
      border-radius:20px;padding:4px 11px;font-size:11px;color:#a78bfa;
      cursor:pointer;margin:6px 0 4px;transition:all .2s;
    }
    .ainai-cat:hover{background:rgba(139,92,246,0.25);transform:translateY(-1px)}
    .ainai-card{
      background:rgba(255,255,255,0.04);border:1px solid rgba(0,255,255,0.12);
      border-radius:10px;padding:10px 12px;margin-top:6px;
      cursor:pointer;transition:all .2s;
    }
    .ainai-card:hover{background:rgba(0,255,255,0.08);border-color:rgba(0,255,255,0.3);transform:translateX(3px)}
    .ainai-card-name{font-weight:600;color:#00ffff;font-size:13px;margin-bottom:3px;display:flex;align-items:center;gap:6px}
    .ainai-card-why{font-size:12px;color:rgba(255,255,255,0.58);line-height:1.4}
    .ainai-card-cat{display:inline-block;margin-top:5px;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600;background:rgba(0,255,255,0.08);color:rgba(0,255,255,0.7);border:1px solid rgba(0,255,255,0.15)}
    .ainai-card-url{font-size:10px;color:#8b5cf6;margin-top:3px;display:inline-block}
    .ainai-go{
      display:flex;align-items:center;justify-content:center;gap:6px;
      width:100%;margin-top:8px;padding:7px;
      background:linear-gradient(90deg,rgba(0,255,255,0.07),rgba(139,92,246,0.07));
      border:1px solid rgba(0,255,255,0.18);border-radius:8px;
      color:#00ffff;font-size:12px;cursor:pointer;transition:all .2s;
    }
    .ainai-go:hover{background:linear-gradient(90deg,rgba(0,255,255,0.14),rgba(139,92,246,0.14))}
    .ainai-fq{font-size:11px;color:rgba(0,255,255,0.45);margin-top:7px;font-style:italic;padding-top:7px;border-top:1px solid rgba(255,255,255,0.05)}
    .ainai-typing{display:flex;gap:4px;padding:10px 13px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.07);border-radius:14px;border-bottom-left-radius:4px;width:fit-content}
    .ainai-td{width:5px;height:5px;background:rgba(0,255,255,0.5);border-radius:50%;animation:ainai-tda 1.2s ease-in-out infinite}
    .ainai-td:nth-child(2){animation-delay:.2s}.ainai-td:nth-child(3){animation-delay:.4s}
    @keyframes ainai-tda{0%,100%{transform:translateY(0);opacity:.3}50%{transform:translateY(-5px);opacity:1}}
    .ainai-qwrap{display:flex;flex-wrap:wrap;gap:6px;padding:0 14px 10px;flex-shrink:0}
    .ainai-qbtn{background:rgba(0,255,255,0.05);border:1px solid rgba(0,255,255,0.18);border-radius:20px;padding:5px 11px;font-size:11px;color:rgba(255,255,255,0.65);cursor:pointer;white-space:nowrap;transition:all .2s}
    .ainai-qbtn:hover{background:rgba(0,255,255,0.12);color:#fff}
    .ainai-inp-area{padding:10px 14px;border-top:1px solid rgba(255,255,255,0.06);display:flex;gap:8px;align-items:flex-end;flex-shrink:0}
    .ainai-inp{flex:1;background:rgba(255,255,255,0.05);border:1px solid rgba(0,255,255,0.18);border-radius:12px;padding:9px 13px;color:#fff;font-size:13px;resize:none;outline:none;max-height:90px;min-height:40px;font-family:inherit;line-height:1.4;transition:border-color .2s}
    .ainai-inp::placeholder{color:rgba(255,255,255,0.28)}
    .ainai-inp:focus{border-color:rgba(0,255,255,0.45)}
    .ainai-send{width:38px;height:38px;border-radius:10px;flex-shrink:0;background:linear-gradient(135deg,#00ffff,#8b5cf6);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:15px;transition:all .2s}
    .ainai-send:hover{transform:scale(1.08)}
    .ainai-send:disabled{opacity:.35;cursor:not-allowed;transform:none}
    .ainai-fetching{font-size:11px;color:rgba(0,255,255,0.5);display:flex;align-items:center;gap:6px;padding:8px 13px}
    .ainai-spin{animation:ainai-rotate 1s linear infinite;display:inline-block}
    @keyframes ainai-rotate{to{transform:rotate(360deg)}}
    @media(max-width:480px){#ainai-win{right:10px;bottom:86px;width:calc(100vw - 20px)}#ainai-chat-btn{right:14px;bottom:16px}}
  `;
  const styleEl = document.createElement("style");
  styleEl.textContent = css;
  document.head.appendChild(styleEl);

  // ── HTML ────────────────────────────────────────────────────────────────────
  document.body.insertAdjacentHTML("beforeend", `
    <button id="ainai-chat-btn" onclick="ainaiToggle()" title="AI Tool Advisor">
      <span id="ainai-icon">🤖</span>
      <span class="ainai-badge" id="ainai-badge">AI</span>
    </button>
    <div id="ainai-win">
      <div class="ainai-hdr">
        <div class="ainai-hdr-av">🤖</div>
        <div class="ainai-hdr-info">
          <h4>AI Tool Advisor</h4>
          <p><span class="ainai-dot"></span>Searches your directory · Llama 3.3</p>
        </div>
        <button class="ainai-x" onclick="ainaiToggle()">✕</button>
      </div>
      <div class="ainai-msgs" id="ainai-msgs"></div>
      <div class="ainai-qwrap" id="ainai-qwrap">
        <button class="ainai-qbtn" onclick="ainaiQuick(this)">Edit videos with AI</button>
        <button class="ainai-qbtn" onclick="ainaiQuick(this)">Write better content</button>
        <button class="ainai-qbtn" onclick="ainaiQuick(this)">Build a chatbot</button>
        <button class="ainai-qbtn" onclick="ainaiQuick(this)">Generate AI images</button>
        <button class="ainai-qbtn" onclick="ainaiQuick(this)">Automate my workflow</button>
        <button class="ainai-qbtn" onclick="ainaiQuick(this)">Summarize documents</button>
        <button class="ainai-qbtn" onclick="ainaiQuick(this)">Code faster</button>
        <button class="ainai-qbtn" onclick="ainaiQuick(this)">Grow on social media</button>
      </div>
      <div class="ainai-inp-area">
        <textarea id="ainai-inp" class="ainai-inp" rows="1"
          placeholder="What do you want to build or do?"
          onkeydown="ainaiKey(event)" oninput="ainaiResize(this)"></textarea>
        <button class="ainai-send" id="ainai-send-btn" onclick="ainaiSend()">➤</button>
      </div>
    </div>
  `);

  // ── Welcome ─────────────────────────────────────────────────────────────────
  setTimeout(() => {
    addBotMsg({
      message: "Hi! 👋 I'm your AI tool advisor. Tell me what you want to build, automate, or improve — I'll search our directory of 700+ real AI tools and recommend the best ones for you.",
      category: null, tools: [], follow_up: "What are you working on today?"
    });
  }, 350);

  // ── Toggle ──────────────────────────────────────────────────────────────────
  window.ainaiToggle = function () {
    isOpen = !isOpen;
    document.getElementById("ainai-win").classList.toggle("open", isOpen);
    document.getElementById("ainai-icon").textContent    = isOpen ? "✕" : "🤖";
    document.getElementById("ainai-badge").style.display = isOpen ? "none" : "flex";
    if (isOpen) document.getElementById("ainai-inp").focus();
  };
  window.ainaiQuick  = function (btn) {
    document.getElementById("ainai-qwrap").style.display = "none";
    ainaiProcess(btn.textContent.trim());
  };
  window.ainaiKey    = function (e) { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); ainaiSend(); } };
  window.ainaiResize = function (el) { el.style.height = "auto"; el.style.height = Math.min(el.scrollHeight, 90) + "px"; };
  window.ainaiSend   = function () {
    const inp  = document.getElementById("ainai-inp");
    const text = inp.value.trim();
    if (!text || isTyping) return;
    inp.value = ""; inp.style.height = "auto";
    document.getElementById("ainai-qwrap").style.display = "none";
    ainaiProcess(text);
  };

  // ── RAG Pipeline ────────────────────────────────────────────────────────────
  async function ainaiProcess(query) {
    addUserMsg(query);
    msgHistory.push({ role: "user", content: query });
    isTyping = true;
    document.getElementById("ainai-send-btn").disabled = true;

    // Step 1 — Fetch real tools from Supabase
    const fetchId = addFetchingMsg("🔍 Searching your directory...");
    let dbTools = [];
    try {
      dbTools = await fetchToolsFromDB(query);
      if (dbTools.length === 0) dbTools = await fetchToolsFromDB(query, true);
    } catch (e) {
      console.warn("DB fetch failed:", e);
    }
    removeFetchingMsg(fetchId);

    // Step 2 — Send to Edge Function (Groq key stays server-side)
    const typingId = addTyping();
    try {
      const result   = await callEdgeFunction(query, dbTools);
      removeTyping(typingId);
      const enriched = enrichWithDBData(result, dbTools);
      addBotMsg(enriched, dbTools.length);
      msgHistory.push({ role: "assistant", content: result.message || "" });
    } catch (e) {
      removeTyping(typingId);
      addBotMsg({
        message: "Sorry, I had trouble connecting. Make sure GROQ_API_KEY is set in Supabase Dashboard → Edge Functions → ai-advisor → Secrets.",
        category: null, tools: [], follow_up: null
      });
    }

    isTyping = false;
    document.getElementById("ainai-send-btn").disabled = false;
  }

  // ── Fetch tools from Supabase DB ────────────────────────────────────────────
  async function fetchToolsFromDB(query, broad = false) {
    const cat = detectCategory(query);
    if (!broad) {
      const res = await fetch(`${SUPABASE_URL}/rest/v1/rpc/search_tools`, {
        method: "POST",
        headers: {
          "Content-Type":  "application/json",
          "apikey":        SUPABASE_KEY,
          "Authorization": `Bearer ${SUPABASE_KEY}`,
        },
        body: JSON.stringify({ search_query: query, result_limit: 15 })
      });
      if (!res.ok) throw new Error("Search failed");
      const data = await res.json();
      return Array.isArray(data) ? data : [];
    } else {
      const catFilter = cat ? `&category=eq.${encodeURIComponent(cat)}` : "";
      const res = await fetch(
        `${SUPABASE_URL}/rest/v1/ai_tools?select=id,name,description,category,website,url,rating,pricing&approved=eq.true${catFilter}&limit=15`,
        { headers: { "apikey": SUPABASE_KEY, "Authorization": `Bearer ${SUPABASE_KEY}` } }
      );
      if (!res.ok) throw new Error("Fetch failed");
      return await res.json();
    }
  }

  // ── Detect category from query keywords ─────────────────────────────────────
  function detectCategory(query) {
    const q   = query.toLowerCase();
    const map = [
      [["video","film","clip","youtube","reel","animation"],           "Video Generation"],
      [["image","photo","picture","art","illustration","logo"],        "Image Generation"],
      [["code","coding","programming","developer","software","debug"], "Development & Code"],
      [["write","writing","blog","copy","content","email","article"],  "Writing & Content"],
      [["voice","speech","audio","podcast","music","sound"],           "Audio & Voice"],
      [["chat","chatbot","customer","support","assistant","bot"],      "Customer Support & Chat"],
      [["research","paper","study","academic","summarize"],            "Research"],
      [["productivity","task","workflow","automate","notion"],         "Productivity"],
      [["marketing","social","instagram","twitter","linkedin","seo"],  "Marketing & Social"],
      [["learn","course","education","tutorial"],                      "Learning & Resources"],
      [["pdf","document","doc","excel","spreadsheet","resume"],        "Document & PDF"],
      [["hire","job","career","interview","hr","recruit"],             "Career & HR"],
      [["design","ui","ux","figma","creative","graphic"],              "Design & Creativity"],
      [["ai","llm","gpt","model","claude","gemini"],                   "AI Assistants"],
    ];
    for (const [kws, cat] of map) {
      if (kws.some(k => q.includes(k))) return cat;
    }
    return null;
  }

  // ── Call Edge Function (no Groq key in browser) ─────────────────────────────
  async function callEdgeFunction(query, dbTools) {
    const toolContext = dbTools.length > 0
      ? dbTools.map((t, i) =>
          `${i+1}. ${t.name} (${t.category || "Other"})\n   ${(t.description || "").slice(0, 150)}\n   URL: ${t.website || t.url || "N/A"} | Rating: ${t.rating || "N/A"} | Pricing: ${t.pricing || "N/A"}`
        ).join("\n\n")
      : "No specific matches found — suggest the most relevant general AI tools.";

    const systemPrompt = `You are an AI tool advisor for "All I Need AI" — a directory of 700+ AI tools.

The user asked: "${query}"

Here are REAL tools from our database that match their query:
${toolContext}

Pick the TOP 3 tools from the list that best fit what the user wants to do.
Respond in this EXACT JSON format (pure JSON only, no markdown):
{
  "message": "2-3 sentence enthusiastic response about their use case",
  "category": "one of: ${CATEGORIES.join(", ")}",
  "tools": [
    { "name": "exact name from list", "reason": "why it fits in 10-15 words" },
    { "name": "exact name from list", "reason": "why it fits in 10-15 words" },
    { "name": "exact name from list", "reason": "why it fits in 10-15 words" }
  ],
  "follow_up": "one short question to refine recommendations"
}
IMPORTANT: Only use tool names that appear in the list above.`;

    const messages = [
      { role: "system", content: systemPrompt },
      ...msgHistory.slice(-4),
      { role: "user", content: query }
    ];

    // ✅ Call goes to Edge Function — Groq key never in browser
    const res = await fetch(EDGE_FN_URL, {
      method: "POST",
      headers: {
        "Content-Type":  "application/json",
        "Authorization": `Bearer ${SUPABASE_KEY}`,
      },
      body: JSON.stringify({ messages, temperature: 0.5, max_tokens: 700 })
    });

    if (!res.ok) throw new Error(await res.text());
    const d   = await res.json();
    let   raw = d.choices[0].message.content.trim();
    if (raw.includes("```")) {
      raw = raw.split("```")[1] || raw;
      if (raw.startsWith("json")) raw = raw.slice(4);
    }
    try { return JSON.parse(raw.trim()); }
    catch { return { message: raw, category: null, tools: [], follow_up: null }; }
  }

  // ── Enrich LLM picks with real DB data ──────────────────────────────────────
  function enrichWithDBData(llmResult, dbTools) {
    if (!llmResult.tools || !dbTools.length) return llmResult;
    const enriched = llmResult.tools.map(pick => {
      const match = dbTools.find(t =>
        t.name?.toLowerCase().trim() === pick.name?.toLowerCase().trim() ||
        t.name?.toLowerCase().includes(pick.name?.toLowerCase()) ||
        pick.name?.toLowerCase().includes(t.name?.toLowerCase())
      );
      return match ? {
        ...pick,
        id:       match.id,
        name:     match.name,
        website:  match.website || match.url || "",
        category: match.category || "",
        rating:   match.rating,
        pricing:  match.pricing,
      } : pick;
    });
    return { ...llmResult, tools: enriched };
  }

  // ── Render functions ─────────────────────────────────────────────────────────
  function addUserMsg(text) {
    append(`<div class="ainai-msg u"><div class="ainai-av">👤</div><div class="ainai-bub">${esc(text)}</div></div>`);
  }

  function addBotMsg(d, dbCount) {
    const ragTag   = dbCount > 0 ? `<div class="ainai-rag-tag">⚡ Searched ${dbCount} real tools from your directory</div>` : "";
    const catHtml  = d.category  ? `<div class="ainai-cat" onclick="ainaiCat('${esc(d.category)}')">📂 Browse ${esc(d.category)} →</div>` : "";
    const toolsHtml = (d.tools||[]).map(t => `
      <div class="ainai-card" onclick="ainaiOpen('${esc(t.id||"")}','${esc(t.name||"")}','${esc(t.website||"")}')">
        <div class="ainai-card-name">🔧 ${esc(t.name)}${t.rating?` <span style="font-size:10px;color:rgba(255,255,255,0.4);font-weight:400">⭐${t.rating}</span>`:""}</div>
        <div class="ainai-card-why">${esc(t.reason)}</div>
        <div style="display:flex;align-items:center;gap:8px;margin-top:4px;flex-wrap:wrap">
          ${t.category?`<span class="ainai-card-cat">${esc(t.category)}</span>`:""}
          ${t.pricing ?`<span style="font-size:10px;color:rgba(255,255,255,0.35)">${esc(t.pricing)}</span>`:""}
          ${t.website ?`<span class="ainai-card-url">↗ Visit</span>`:""}
        </div>
      </div>`).join("");
    const goHtml  = d.tools?.length ? `<button class="ainai-go" onclick="ainaiSearch('${esc(d.tools[0]?.name||d.category||"")}')">🔍 View all matching tools in directory</button>` : "";
    const fqHtml  = d.follow_up     ? `<div class="ainai-fq">💬 ${esc(d.follow_up)}</div>` : "";
    append(`<div class="ainai-msg b"><div class="ainai-av">🤖</div><div class="ainai-bub">${ragTag}<div>${esc(d.message)}</div>${catHtml}${toolsHtml}${goHtml}${fqHtml}</div></div>`);
  }

  function addFetchingMsg(text) {
    const id = "ainai-f-" + Date.now();
    append(`<div class="ainai-msg b" id="${id}"><div class="ainai-av">🤖</div><div class="ainai-fetching"><span class="ainai-spin">⟳</span> ${esc(text)}</div></div>`);
    return id;
  }
  function removeFetchingMsg(id) { document.getElementById(id)?.remove(); }

  function addTyping() {
    const id = "ainai-t-" + Date.now();
    append(`<div class="ainai-msg b" id="${id}"><div class="ainai-av">🤖</div><div class="ainai-typing"><div class="ainai-td"></div><div class="ainai-td"></div><div class="ainai-td"></div></div></div>`);
    return id;
  }
  function removeTyping(id) { document.getElementById(id)?.remove(); }

  function append(html) {
    const el = document.getElementById("ainai-msgs");
    el.insertAdjacentHTML("beforeend", html);
    el.scrollTop = el.scrollHeight;
  }

  // ── Bridge to main app ───────────────────────────────────────────────────────
  window.ainaiOpen = function (id, name, url) {
    if (id && typeof openToolModal === "function") { openToolModal(id); ainaiToggle(); return; }
    if (url && url.startsWith("http")) { window.open(url, "_blank"); return; }
    ainaiSearch(name);
  };
  window.ainaiCat = function (cat) {
    if (typeof handleCategoryFilter === "function") handleCategoryFilter(cat);
    ainaiToggle();
    setTimeout(() => document.getElementById("tools-grid")?.scrollIntoView({ behavior: "smooth" }), 300);
  };
  window.ainaiSearch = function (q) {
    const inp = document.getElementById("search-input");
    if (inp && q) { inp.value = q; if (typeof handleSearch === "function") handleSearch({ target: inp }); }
    ainaiToggle();
  };

  function esc(s) {
    return String(s||"").replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#039;");
  }

})();