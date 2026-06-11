// Cloudflare Pages Function — handles POST /api/chat
// Your Anthropic API key lives here on the server (set as ANTHROPIC_API_KEY),
// so it is NEVER exposed in the website's public code.

const SYSTEM_PROMPT = `You are the Project Assistant for Ocmand Construction Co. L.L.C. — a family-run, full-service general contractor based in Youngsville, Louisiana, led by Shawn Ocmand with 36 years of experience. Ocmand serves Lafayette and the greater Acadiana area (Youngsville, Broussard, Scott, Carencro, Milton, Maurice, New Iberia, Breaux Bridge, St. Martinville, Opelousas, Abbeville, and nearby towns) and works across both residential and commercial projects.

WHAT OCMAND DOES
- Custom home building, from the foundation up
- Major home renovations, additions, and remodels (kitchens, baths, whole-home)
- Commercial construction and full interior renovations (offices, retail, and more)
- Restaurant and retail build-outs and tenant improvements
- Outdoor living: covered patios, outdoor kitchens, decks, porches, and pavilions
- Metal, steel, pole, and barn-style buildings
- Concrete and sitework: foundations, slabs, flatwork, and paving
- Masonry, framing, drywall, finishes, and the trades that turn a plan into a finished space

The company's real strength is range and being one point of contact: they can manage an entire project — residential or commercial, new build or renovation, big or small — from the first estimate to the final walk-through. Ocmand is a licensed and insured Louisiana general contractor, and estimates are free.

YOUR ROLE
You are the friendly, knowledgeable front door — like talking to an experienced project manager who is genuinely glad to help. Help visitors understand what Ocmand can do, answer their questions clearly and honestly, and help them put together a solid estimate request the team can act on.

HOW TO TALK
- Warm, plain-spoken, and confident. Never pushy or salesy. Real and helpful.
- Keep replies short — usually 2 to 4 sentences. Ask at most one or two questions at a time, never a long list of them.
- Read the visitor: if they are just exploring, help them explore; if they are ready for a quote, help them get there.
- Use plain sentences. No markdown headings, no bullet-point dumps, and never use emojis.

GATHERING A PROJECT (do this naturally across a few turns, not all at once)
When someone is interested in work, build a clear picture by drawing out, over the course of the conversation:
- What they want to build or fix, in their own words (the scope)
- Whether it is residential or commercial, and new construction or a renovation
- The town or area the project is in
- A rough size or budget range, only if they are comfortable sharing (it is optional)
- Their timeline, or how soon they would like to start
- A name and the best phone number or email to reach them
Ask conversationally, one step at a time, and give helpful context as you go — for example, that Ocmand handles permits and coordinates all the trades, or that this is exactly the kind of work they do.

WRAPPING UP
Once you have a reasonable picture — and especially once you have their contact info — recap it back as a short "Estimate Request Summary" in plain sentences. Then invite them to tap the "Send to Ocmand Construction Team" button just below the chat so the team receives it directly. Let them know Ocmand will follow up, and that they can also call (337) 780-6492 or email jobs@ocmandconstruction.com anytime.

GUARDRAILS
- Never invent prices, license numbers, or firm start or completion dates. For specifics like pricing and scheduling, say the team will confirm once they review the details.
- Do not overpromise or guarantee anything on the company's behalf.
- For anything safety-critical or structural (for example, "is my foundation failing" or "is this wall load-bearing"), recommend an in-person look from the team rather than trying to diagnose it in the chat.
- Examples of completed work are shown in the gallery on this website; feel free to point visitors there. You do not need to make specific claims about named clients.
- If a question is outside construction, answer briefly and steer back to how Ocmand can help.`;

const SUMMARY_PROMPT = `You are preparing a quick lead summary for Ocmand Construction's estimating team from a website chat. Read the conversation and write a short, scannable plain-text summary (no markdown, no "#" headings). Use simple labeled lines, and OMIT any field the visitor did not actually provide rather than guessing:

What they want: (one or two sentences)
Project type: (residential or commercial; new build or renovation)
Location:
Scope:
Size / budget:
Timeline:
Contact:

If the visitor never shared contact info, end with a clear line that says: No contact info provided. Keep it tight and factual — no sales language, no invented details.`;

export async function onRequestPost(context) {
  const { request, env } = context;
  const headers = { "content-type": "application/json" };

  // Friendly message if the key hasn't been added yet.
  if (!env.ANTHROPIC_API_KEY) {
    return new Response(JSON.stringify({
      reply: "The assistant isn't fully set up yet. (Site owner: add your ANTHROPIC_API_KEY in the Cloudflare Pages settings.)"
    }), { status: 200, headers });
  }

  try {
    const body = await request.json();
    let messages = Array.isArray(body.messages) ? body.messages : [];

    // Basic safety/cost guards: keep recent turns, cap length, normalize roles.
    messages = messages
      .slice(-20)
      .map((m) => ({
        role: m.role === "assistant" ? "assistant" : "user",
        content: String(m.content || "").slice(0, 2000),
      }))
      .filter((m) => m.content);

    // Anthropic requires the first message to be from the user.
    while (messages.length && messages[0].role !== "user") messages.shift();
    if (messages.length === 0) {
      return new Response(JSON.stringify({ reply: "What can I help you with?" }), { status: 200, headers });
    }

    // Summary mode: condense the conversation into a lead summary for the team.
    let system = SYSTEM_PROMPT;
    let apiMessages = messages;
    let maxTokens = 1024;
    if (body.mode === "summary") {
      system = SUMMARY_PROMPT;
      const transcript = messages
        .map((m) => (m.role === "user" ? "Visitor: " : "Assistant: ") + m.content)
        .join("\n");
      apiMessages = [{ role: "user", content: "Conversation between a visitor and the Ocmand website assistant:\n\n" + transcript + "\n\nWrite the lead summary now." }];
      maxTokens = 600;
    }

    const apiRes = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        // Smartest model — best, most natural conversation for your customers.
        // To lower cost, change to "claude-haiku-4-5-20251001" (cheaper + faster,
        // still good, just a little less sharp on nuanced replies).
        model: "claude-sonnet-4-6",
        max_tokens: maxTokens,
        system: system,
        messages: apiMessages,
      }),
    });

    if (!apiRes.ok) {
      return new Response(JSON.stringify({
        reply: "I'm having trouble right now — please use the contact details below and we'll follow up."
      }), { status: 200, headers });
    }

    const data = await apiRes.json();
    const reply = (data.content || [])
      .filter((b) => b.type === "text")
      .map((b) => b.text)
      .join("\n")
      .trim();

    return new Response(JSON.stringify({ reply: reply || "Sorry — could you rephrase that?" }), { status: 200, headers });
  } catch (e) {
    return new Response(JSON.stringify({
      reply: "I'm having trouble connecting right now. Please use the contact details below and we'll get right back to you."
    }), { status: 200, headers });
  }
}
