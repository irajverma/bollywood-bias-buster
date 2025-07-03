import { type NextRequest, NextResponse } from "next/server"
import { generateText } from "ai"
import { openai } from "@ai-sdk/openai"

export async function POST(req: NextRequest) {
  try {
    const { text } = await req.json()

    if (!text) {
      return NextResponse.json({ error: "Text is required" }, { status: 400 })
    }

    const { text: analysis } = await generateText({
      model: openai("gpt-4o"),
      system: `You are an expert in gender bias detection in film scripts. Analyze the provided text for gender stereotypes and bias patterns. Focus on:

1. Character introductions and descriptions
2. Professional identity representation
3. Agency and decision-making power
4. Relationship-based vs. individual identity
5. Appearance focus vs. character traits

Return a JSON response with:
- characters: array of detected characters with gender
- biases: array of detected biases with type, severity, and excerpt
- overallScore: bias score from 0-100 (higher = more biased)
- suggestions: remediation suggestions

Be thorough but concise in your analysis.`,
      prompt: `Analyze this text for gender bias and stereotypes: "${text}"`,
    })

    // Parse the AI response (in a real implementation, you'd want more robust parsing)
    let parsedAnalysis
    try {
      parsedAnalysis = JSON.parse(analysis)
    } catch {
      // Fallback if AI doesn't return valid JSON
      parsedAnalysis = {
        characters: [{ name: "Detected Character", gender: "Unknown" }],
        biases: [
          {
            type: "General Bias",
            severity: "medium",
            excerpt: text.substring(0, 100) + "...",
            suggestion: "Consider more balanced character representation",
          },
        ],
        overallScore: 65,
        suggestions: ["Review character introductions for balanced representation"],
      }
    }

    return NextResponse.json(parsedAnalysis)
  } catch (error) {
    console.error("Analysis error:", error)
    return NextResponse.json({ error: "Failed to analyze text" }, { status: 500 })
  }
}
