import { type NextRequest, NextResponse } from "next/server"
import { BollywoodDataProcessor } from "@/lib/data-processor"

const processor = new BollywoodDataProcessor()

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const type = searchParams.get("type")
  const filePath = searchParams.get("file")

  try {
    // If requesting specific file content
    if (filePath) {
      const content = await processor.fetchFileContent(filePath)
      return NextResponse.json({ content })
    }

    // If requesting dataset structure or specific type
    switch (type) {
      case "scripts":
        const scripts = await processor.fetchScriptsData()
        return NextResponse.json({ files: scripts })

      case "wikipedia":
        const wikipedia = await processor.fetchWikipediaData()
        return NextResponse.json({ files: wikipedia })

      case "trailers":
        const trailers = await processor.fetchTrailerData()
        return NextResponse.json({ files: trailers })

      case "images":
        const images = await processor.fetchImageData()
        return NextResponse.json({ files: images })

      case "structure":
      default:
        const structure = await processor.fetchDatasetStructure()
        return NextResponse.json({ structure })
    }
  } catch (error) {
    console.error("Dataset API error:", error)
    return NextResponse.json({ error: "Failed to fetch dataset" }, { status: 500 })
  }
}

export async function POST(request: NextRequest) {
  try {
    const { filePath, movieTitle, year } = await request.json()

    if (!filePath) {
      return NextResponse.json({ error: "File path is required" }, { status: 400 })
    }

    // Fetch file content and analyze for bias
    const content = await processor.fetchFileContent(filePath)
    if (!content) {
      return NextResponse.json({ error: "Failed to fetch file content" }, { status: 404 })
    }

    // Process the content for bias analysis
    const analysis = processor.processScriptForBias(
      content,
      movieTitle || filePath.split("/").pop()?.replace(".txt", "") || "Unknown",
      year || 2000,
    )

    return NextResponse.json({ analysis })
  } catch (error) {
    console.error("Bias analysis error:", error)
    return NextResponse.json({ error: "Failed to analyze file for bias" }, { status: 500 })
  }
}
