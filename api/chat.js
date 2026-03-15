import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { message } = req.body;
  if (!message) return res.status(400).json({ error: 'No message provided' });

  try {
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini",
      max_tokens: 500,
      messages: [
        {
          role: "system",
          content: `You are a highly persuasive AI sales assistant specialized in dental practice growth. Your goal is to close prospects by highlighting how missed calls, low patient acquisition, and inefficient marketing are costing the practice revenue. You must:
- Identify pain points in the conversation
- Show lost revenue and opportunity
- Handle objections confidently
- Suggest solutions like missed call recovery systems
- Always guide the prospect to take action (schedule a demo, consultation, or trial)
- Speak professionally, persuasively, and friendly`
        },
        { role: "user", content: message },
      ],
    });
    res.status(200).json({ reply: completion.choices[0].message.content });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}
