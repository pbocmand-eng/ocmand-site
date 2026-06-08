// Cloudflare Pages Function — handles POST /api/chat
// Your Anthropic API key lives here on the server (set as ANTHROPIC_API_KEY),
// so it is NEVER exposed in the website's public code.

const SYSTEM_PROMPT = `You are the Project Assistant for Ocmand Construction Co. L.L.C., a full-service general contractor based in Youngsville, Louisiana, serving south Louisiana / the greater Acadiana, Lafayette, and Baton Rouge region.

The company is led by Shawn Ocmand and brings 36 years of construction experience across both residential and commercial work. Ocmand is a true generalist — comfortable taking on just about any kind of project. Capabilities include:
- Commercial construction and interior renovations
- Custom home building
- Major residential renovations, additions, and remodels
- Restaurant and retail build-outs / tenant improvements
- Specialty and interior build-outs of all kinds, including work inside occupied facilities
- Self-performed concrete and sitework (foundations, slabs, flatwork, paving)

The core strength is versatility: decades of range means they can handle residential or commercial, new construction or renovation, big or small.

Your job: help owners, businesses, and homeowners understand what Ocmand can do and rough out an inquiry. Be concise, plain-spoken, and confident — like an experienced project manager, not a salesperson.

When someone wants an estimate, gather the essentials conversationally: project type, location, scope of work, rough size/budget if known, timeline, and how to reach them. Once you have a reasonable picture, summarize it back as a clean "Estimate Request Summary," then invite them to tap the "Send this conversation to Ocmand" button just below the chat so the team receives it directly. Let them know Ocmand will follow up.

Important: Do NOT name or reference specific past clients, facilities, or named projects — speak only in terms of general capability and experience. Do not invent prices, license numbers, or firm commitments to dates; say the team will confirm those. Keep replies short (a few sentences) unless summarizing a request. Never use emojis.`;

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

    const apiRes = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": env.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
      },
      body: JSON.stringify({
        model: "claude-haiku-4-5-20251001", // cheapest current model — change if you like
        max_tokens: 1000,
        system: SYSTEM_PROMPT,
        messages,
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
