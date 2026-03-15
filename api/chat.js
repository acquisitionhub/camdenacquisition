import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {

  // Only allow POST
  if (req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  try {
    // Safely parse body
    const body = typeof req.body === "string" ? JSON.parse(req.body) : req.body;
    const message = body?.message;

    // Check message exists
    if (!message || message.trim() === "") {
      return res.status(400).json({ reply: "I didn't receive your message. Please try again." });
    }

    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      max_tokens: 500,
      temperature: 0.7,
      messages: [
        {
          role: "system",
          content: `You are a highly persuasive AI sales assistant for Patient Acquisition Hub, a UK dental practice growth system based in London.

Your goal is to help UK dental practice owners understand how they are losing patients and revenue, and guide them towards booking a free demo.

You must:
- Identify pain points around missed calls, low bookings, and inefficient marketing
- Show the cost of inaction — e.g. a missed call = £500–£3,000 lost lifetime value
- Handle objections confidently and professionally
- Highlight key services: missed call recovery, automated SMS follow-up, patient acquisition, enquiry management
- Always guide the prospect to book a free demo at: https://calendly.com/patientacquisitionhub/30min
- Keep answers concise, friendly, and persuasive
- Never mention competitor products
- Always respond in English`
        },
        {
          role: "user",
          content: message
        }
      ],
    });

    const reply = completion?.choices?.[0]?.message?.content;

    if (!reply) {
      return res.status(500).json({ reply: "I couldn't generate a response. Please try again." });
    }

    return res.status(200).json({ reply });

  } catch (error) {
    console.error("OpenAI Error:", error);
    return res.status(500).json({ 
      reply: "Something went wrong. Please email us at Julien@patientacquisitionhub.com or book a demo at https://calendly.com/patientacquisitionhub/30min" 
    });
  }
}
