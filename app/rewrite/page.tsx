"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Wand2, Copy, ThumbsUp, ThumbsDown, RefreshCw } from "lucide-react"

interface RewriteSuggestion {
  original: string
  rewritten: string
  improvements: string[]
  biasReduction: number
  preservedElements: string[]
}

export default function RewritePage() {
  const [inputText, setInputText] = useState("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [suggestions, setSuggestions] = useState<RewriteSuggestion[]>([])
  const [selectedSuggestion, setSelectedSuggestion] = useState<number | null>(null)

  const generateRewrites = async () => {
    if (!inputText.trim()) return

    setIsGenerating(true)

    // Simulate AI rewrite generation
    setTimeout(() => {
      const mockSuggestions: RewriteSuggestion[] = [
        {
          original: inputText,
          rewritten:
            "Rohit is an aspiring singer who works as a salesman in a car showroom run by Malik. One day he meets Sonia Saxena, a marketing executive and daughter of Mr Saxena, when he goes to deliver a car to her as a birthday present.",
          improvements: [
            "Added professional identity for female character",
            "Maintained family relationship context",
            "Balanced character introductions",
          ],
          biasReduction: 65,
          preservedElements: [
            "Character names and relationships",
            "Plot progression and context",
            "Narrative flow and tone",
          ],
        },
        {
          original: inputText,
          rewritten:
            "Rohit, an aspiring singer working as a car salesman, meets Sonia Saxena, a successful entrepreneur, when delivering her birthday gift. Both share dreams of making their mark in their respective fields.",
          improvements: [
            "Equal emphasis on both characters' aspirations",
            "Removed dependency-based introduction",
            "Added mutual professional respect",
          ],
          biasReduction: 78,
          preservedElements: ["Core meeting scenario", "Birthday context", "Character essence"],
        },
        {
          original: inputText,
          rewritten:
            "When car salesman and aspiring singer Rohit delivers a birthday present to Sonia Saxena, a finance professional, their chance encounter sparks an unexpected connection between two ambitious individuals.",
          improvements: [
            "Neutral character introductions",
            "Focus on individual achievements",
            "Emphasized mutual agency",
          ],
          biasReduction: 72,
          preservedElements: ["Meeting circumstances", "Character professions", "Romantic potential"],
        },
      ]

      setSuggestions(mockSuggestions)
      setIsGenerating(false)
    }, 2500)
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  const loadSampleText = () => {
    setInputText(
      "Rohit is an aspiring singer who works as a salesman in a car showroom run by Malik. One day he meets Sonia Saxena, daughter of Mr Saxena, when he goes to deliver a car to her as a birthday present.",
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">AI Rewrite Generator</h1>
          <p className="text-gray-600">
            Generate bias-free alternatives that preserve narrative intent and character essence.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Input Section */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Wand2 className="h-5 w-5" />
                Original Text
              </CardTitle>
              <CardDescription>Enter the text you want to rewrite for bias reduction</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                placeholder="Enter your script text or character descriptions here..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                className="min-h-[150px]"
              />

              <div className="flex gap-2">
                <Button onClick={generateRewrites} disabled={!inputText.trim() || isGenerating} className="flex-1">
                  {isGenerating ? (
                    <>
                      <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Wand2 className="h-4 w-4 mr-2" />
                      Generate Rewrites
                    </>
                  )}
                </Button>
                <Button variant="outline" onClick={loadSampleText}>
                  Load Sample
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Suggestions Overview */}
          <Card>
            <CardHeader>
              <CardTitle>Rewrite Suggestions</CardTitle>
              <CardDescription>
                {suggestions.length > 0
                  ? `${suggestions.length} bias-free alternatives generated`
                  : "AI-generated alternatives will appear here"}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {suggestions.length === 0 && !isGenerating && (
                <div className="text-center py-8 text-gray-500">
                  No suggestions yet. Enter text and click "Generate Rewrites" to begin.
                </div>
              )}

              {isGenerating && (
                <div className="text-center py-8">
                  <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4 text-blue-600" />
                  <div className="text-gray-600">Generating bias-free alternatives...</div>
                </div>
              )}

              {suggestions.length > 0 && (
                <div className="space-y-3">
                  {suggestions.map((suggestion, index) => (
                    <div
                      key={index}
                      className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                        selectedSuggestion === index
                          ? "border-blue-500 bg-blue-50"
                          : "border-gray-200 hover:border-gray-300"
                      }`}
                      onClick={() => setSelectedSuggestion(index)}
                    >
                      <div className="flex items-center justify-between mb-2">
                        <Badge variant="secondary">Option {index + 1}</Badge>
                        <Badge variant="outline" className="text-green-700 border-green-200 bg-green-50">
                          -{suggestion.biasReduction}% bias
                        </Badge>
                      </div>
                      <p className="text-sm text-gray-700 line-clamp-3">{suggestion.rewritten}</p>
                    </div>
                  ))}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Detailed View */}
        {selectedSuggestion !== null && suggestions[selectedSuggestion] && (
          <Card className="mt-8">
            <CardHeader>
              <CardTitle>Detailed Analysis - Option {selectedSuggestion + 1}</CardTitle>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="rewrite" className="w-full">
                <TabsList className="grid w-full grid-cols-4">
                  <TabsTrigger value="rewrite">Rewritten Text</TabsTrigger>
                  <TabsTrigger value="improvements">Improvements</TabsTrigger>
                  <TabsTrigger value="preserved">Preserved Elements</TabsTrigger>
                  <TabsTrigger value="comparison">Comparison</TabsTrigger>
                </TabsList>

                <TabsContent value="rewrite" className="space-y-4">
                  <Alert>
                    <AlertDescription>
                      <div className="flex justify-between items-start mb-3">
                        <div className="font-medium">Bias-Free Version:</div>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => copyToClipboard(suggestions[selectedSuggestion].rewritten)}
                        >
                          <Copy className="h-4 w-4 mr-1" />
                          Copy
                        </Button>
                      </div>
                      <p className="text-gray-700 leading-relaxed">{suggestions[selectedSuggestion].rewritten}</p>
                    </AlertDescription>
                  </Alert>

                  <div className="flex items-center gap-4">
                    <Badge variant="outline" className="text-green-700 border-green-200 bg-green-50">
                      Bias Reduction: {suggestions[selectedSuggestion].biasReduction}%
                    </Badge>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm">
                        <ThumbsUp className="h-4 w-4 mr-1" />
                        Helpful
                      </Button>
                      <Button variant="outline" size="sm">
                        <ThumbsDown className="h-4 w-4 mr-1" />
                        Not Helpful
                      </Button>
                    </div>
                  </div>
                </TabsContent>

                <TabsContent value="improvements" className="space-y-3">
                  {suggestions[selectedSuggestion].improvements.map((improvement, index) => (
                    <Alert key={index}>
                      <AlertDescription>
                        <div className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-green-500 rounded-full mt-2 flex-shrink-0"></div>
                          <span>{improvement}</span>
                        </div>
                      </AlertDescription>
                    </Alert>
                  ))}
                </TabsContent>

                <TabsContent value="preserved" className="space-y-3">
                  {suggestions[selectedSuggestion].preservedElements.map((element, index) => (
                    <Alert key={index}>
                      <AlertDescription>
                        <div className="flex items-start gap-2">
                          <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>
                          <span>{element}</span>
                        </div>
                      </AlertDescription>
                    </Alert>
                  ))}
                </TabsContent>

                <TabsContent value="comparison" className="space-y-4">
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Original Text:</h4>
                    <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                      <p className="text-gray-700">{suggestions[selectedSuggestion].original}</p>
                    </div>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-900 mb-2">Rewritten Text:</h4>
                    <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                      <p className="text-gray-700">{suggestions[selectedSuggestion].rewritten}</p>
                    </div>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
