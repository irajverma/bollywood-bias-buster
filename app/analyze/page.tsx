"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Upload, AlertTriangle, CheckCircle, XCircle } from "lucide-react"

interface BiasDetection {
  character: string
  gender: string
  stereotype: string
  severity: "low" | "medium" | "high"
  category: string
  excerpt: string
  suggestion: string
}

export default function AnalyzePage() {
  const [text, setText] = useState("")
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [results, setResults] = useState<BiasDetection[]>([])
  const [overallScore, setOverallScore] = useState<number | null>(null)

  const analyzeText = async () => {
    if (!text.trim()) return

    setIsAnalyzing(true)

    // Simulate AI analysis with realistic results
    setTimeout(() => {
      const mockResults: BiasDetection[] = [
        {
          character: "Sonia Saxena",
          gender: "Female",
          stereotype: "Occupation Gap",
          severity: "high",
          category: "Professional Identity",
          excerpt: "Sonia Saxena, daughter of Mr Saxena",
          suggestion: "Sonia Saxena, a marketing executive and daughter of Mr Saxena",
        },
        {
          character: "Rohit",
          gender: "Male",
          stereotype: "Agency Emphasis",
          severity: "medium",
          category: "Character Agency",
          excerpt: "Rohit is an aspiring singer who works as a salesman",
          suggestion: "Current description shows balanced professional and personal attributes",
        },
      ]

      setResults(mockResults)
      setOverallScore(72) // Bias score out of 100
      setIsAnalyzing(false)
    }, 3000)
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return "bg-red-100 text-red-800 border-red-200"
      case "medium":
        return "bg-yellow-100 text-yellow-800 border-yellow-200"
      case "low":
        return "bg-green-100 text-green-800 border-green-200"
      default:
        return "bg-gray-100 text-gray-800 border-gray-200"
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "high":
        return <XCircle className="h-4 w-4" />
      case "medium":
        return <AlertTriangle className="h-4 w-4" />
      case "low":
        return <CheckCircle className="h-4 w-4" />
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Script Analysis</h1>
          <p className="text-gray-600">
            Upload or paste your script text to identify gender stereotypes and bias patterns.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="h-5 w-5" />
                Script Input
              </CardTitle>
              <CardDescription>Paste your script text or character descriptions below</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Example: Rohit is an aspiring singer who works as a salesman in a car showroom run by Malik. One day he meets Sonia Saxena, daughter of Mr Saxena, when he goes to deliver a car to her as a birthday present..."
                value={text}
                onChange={(e) => setText(e.target.value)}
                className="min-h-[200px]"
              />
              <Button onClick={analyzeText} disabled={!text.trim() || isAnalyzing} className="w-full">
                {isAnalyzing ? "Analyzing..." : "Analyze for Bias"}
              </Button>

              {isAnalyzing && (
                <div className="space-y-2">
                  <div className="text-sm text-gray-600">Analyzing script...</div>
                  <Progress value={33} className="w-full" />
                  <div className="text-xs text-gray-500">Detecting character genders and role attributes...</div>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Results Section */}
          <Card>
            <CardHeader>
              <CardTitle>Analysis Results</CardTitle>
              {overallScore !== null && (
                <div className="flex items-center gap-4">
                  <div className="text-sm text-gray-600">Bias Score:</div>
                  <div className="flex items-center gap-2">
                    <Progress value={overallScore} className="w-24" />
                    <span
                      className={`text-sm font-medium ${
                        overallScore > 80 ? "text-red-600" : overallScore > 60 ? "text-yellow-600" : "text-green-600"
                      }`}
                    >
                      {overallScore}/100
                    </span>
                  </div>
                </div>
              )}
            </CardHeader>
            <CardContent>
              {results.length === 0 && !isAnalyzing && (
                <div className="text-center py-8 text-gray-500">
                  No analysis results yet. Enter text above to begin.
                </div>
              )}

              <div className="space-y-4">
                {results.map((result, index) => (
                  <Alert key={index} className="border-l-4">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Badge variant="outline" className={getSeverityColor(result.severity)}>
                            {getSeverityIcon(result.severity)}
                            {result.severity.toUpperCase()}
                          </Badge>
                          <Badge variant="secondary">{result.category}</Badge>
                        </div>
                        <AlertDescription className="space-y-2">
                          <div>
                            <strong>Character:</strong> {result.character} ({result.gender})
                          </div>
                          <div>
                            <strong>Stereotype:</strong> {result.stereotype}
                          </div>
                          <div className="bg-gray-50 p-2 rounded text-sm italic">"{result.excerpt}"</div>
                          <div className="text-sm text-green-700">
                            <strong>Suggestion:</strong> {result.suggestion}
                          </div>
                        </AlertDescription>
                      </div>
                    </div>
                  </Alert>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Sample Analysis */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Try Sample Analysis</CardTitle>
            <CardDescription>Click below to analyze the example from "Kaho Naa... Pyaar Hai"</CardDescription>
          </CardHeader>
          <CardContent>
            <Button
              variant="outline"
              onClick={() => {
                setText(
                  "Rohit is an aspiring singer who works as a salesman in a car showroom run by Malik. One day he meets Sonia Saxena, daughter of Mr Saxena, when he goes to deliver a car to her as a birthday present. Sonia is beautiful and comes from a wealthy family. Meanwhile, Rohit dreams of becoming a successful musician while supporting his family.",
                )
              }}
            >
              Load Sample Text
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
