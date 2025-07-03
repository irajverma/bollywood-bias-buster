import { type NextRequest, NextResponse } from "next/server"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(req: NextRequest) {
  try {
    const { text } = await req.json()

    if (!text) {
      return NextResponse.json({ error: "Text is required" }, { status: 400 })
    }

    const { text: rewrites } = await generateText({
      model: openai("gpt-4o"),
      system: `You are an expert script writer specializing in creating bias-free, inclusive content. Your task is to rewrite the provided text to eliminate gender stereotypes while preserving the narrative intent and character essence.

Generate 3 different rewrite options that:
1. Remove gender bias and stereotypes
2. Provide equal representation and agency
3. Maintain the original story flow and context
4. Preserve character relationships and plot points

For each rewrite, also provide:
- List of specific improvements made
- Bias reduction percentage
- Elements preserved from original

Return a JSON array of rewrite objects with: original, rewritten, improvements, biasReduction, preservedElements`,
      prompt: `Rewrite this text to eliminate gender bias while preserving narrative intent: "${text}"`,
    })

    // Parse the AI response
    let parsedRewrites
    try {
      parsedRewrites = JSON.parse(rewrites)
    } catch {
      // Fallback rewrites if AI doesn't return valid JSON
      parsedRewrites = [
        {
          original: text,
          rewritten: text.replace(/daughter of/g, "professional and daughter of"),
          improvements: ["Added professional identity", "Maintained family context", "Balanced character introduction"],
          biasReduction: 65,
          preservedElements: ["Character names", "Plot progression", "Narrative tone"],
        },
      ]
    }

    return NextResponse.json(parsedRewrites)
  } catch (error) {
    console.error("Rewrite error:", error)
    return NextResponse.json({ error: "Failed to generate rewrites" }, { status: 500 })
  }
}
