"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ScrollArea } from "@/components/ui/scroll-area"
import {
  FileText,
  ImageIcon,
  Video,
  Globe,
  Download,
  Eye,
  Search,
  RefreshCw,
  AlertCircle,
  CheckCircle,
} from "lucide-react"
import { BollywoodDataProcessor } from "@/lib/data-processor"

interface ProcessedFile {
  name: string
  path: string
  size: number
  lastModified: string
  content?: string
}

interface GitHubStatus {
  available: boolean
  rateLimit: {
    remaining: number
    total: number
  }
}

export default function DataExplorerPage() {
  const [scriptsData, setScriptsData] = useState<ProcessedFile[]>([])
  const [wikipediaData, setWikipediaData] = useState<ProcessedFile[]>([])
  const [trailersData, setTrailersData] = useState<ProcessedFile[]>([])
  const [imagesData, setImagesData] = useState<ProcessedFile[]>([])
  const [selectedFile, setSelectedFile] = useState<ProcessedFile | null>(null)
  const [fileContent, setFileContent] = useState<string>("")
  const [loading, setLoading] = useState(true)
  const [contentLoading, setContentLoading] = useState(false)
  const [githubStatus, setGithubStatus] = useState<GitHubStatus>({
    available: false,
    rateLimit: { remaining: 0, total: 60 },
  })
  const [usingMockData, setUsingMockData] = useState(false)

  const processor = new BollywoodDataProcessor()

  useEffect(() => {
    loadAllData()
    checkGitHubStatus()
  }, [])

  const checkGitHubStatus = async () => {
    try {
      const response = await fetch("https://api.github.com/rate_limit")
      if (response.ok) {
        const data = await response.json()
        setGithubStatus({
          available: true,
          rateLimit: {
            remaining: data.rate.remaining,
            total: data.rate.limit,
          },
        })
      } else {
        setGithubStatus({
          available: false,
          rateLimit: { remaining: 0, total: 60 },
        })
      }
    } catch (error) {
      console.error("Error checking GitHub status:", error)
      setGithubStatus({
        available: false,
        rateLimit: { remaining: 0, total: 60 },
      })
    }
  }

  const loadAllData = async () => {
    setLoading(true)
    try {
      console.log("Loading all dataset categories...")

      const [scripts, wikipedia, trailers, images] = await Promise.all([
        processor.getScriptsData(),
        processor.getWikipediaData(),
        processor.getTrailersData(),
        processor.getImagesData(),
      ])

      console.log("Data loaded:", {
        scripts: scripts.length,
        wikipedia: wikipedia.length,
        trailers: trailers.length,
        images: images.length,
      })

      setScriptsData(scripts)
      setWikipediaData(wikipedia)
      setTrailersData(trailers)
      setImagesData(images)

      // Check if we're using mock data
      const totalFiles = scripts.length + wikipedia.length + trailers.length + images.length
      setUsingMockData(totalFiles > 0)
    } catch (error) {
      console.error("Error loading data:", error)
      // Ensure we always have some data to show
      setScriptsData(processor.getMockScriptsData())
      setWikipediaData(processor.getMockWikipediaData())
      setTrailersData(processor.getMockTrailersData())
      setImagesData(processor.getMockImagesData())
      setUsingMockData(true)
    } finally {
      setLoading(false)
    }
  }

  const handleFileSelect = async (file: ProcessedFile) => {
    setSelectedFile(file)
    setContentLoading(true)

    try {
      const content = await processor.getFileContent(file.path)
      setFileContent(content)
    } catch (error) {
      console.error("Error loading file content:", error)
      setFileContent("Error loading file content. Please try again.")
    } finally {
      setContentLoading(false)
    }
  }

  const analyzeFileForBias = () => {
    if (selectedFile) {
      // Navigate to analyze page with the file content
      const params = new URLSearchParams({
        fileName: selectedFile.name,
        content: fileContent,
      })
      window.open(`/analyze?${params.toString()}`, "_blank")
    }
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return "0 Bytes"
    const k = 1024
    const sizes = ["Bytes", "KB", "MB", "GB"]
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Number.parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i]
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }

  const getFileIcon = (fileName: string) => {
    if (fileName.includes("trailer") || fileName.includes("video")) return Video
    if (fileName.match(/\.(jpg|jpeg|png|gif)$/i)) return ImageIcon
    if (fileName.includes("plot") || fileName.includes("wiki")) return Globe
    return FileText
  }

  const FileList = ({ files, category }: { files: ProcessedFile[]; category: string }) => (
    <div className="space-y-2">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold flex items-center gap-2">
          {category === "Scripts" && <FileText className="h-5 w-5" />}
          {category === "Wikipedia" && <Globe className="h-5 w-5" />}
          {category === "Trailers" && <Video className="h-5 w-5" />}
          {category === "Images" && <ImageIcon className="h-5 w-5" />}
          {category}
          {usingMockData && <Badge variant="secondary">Mock Data</Badge>}
        </h3>
        <Badge variant="outline">{files.length} files available</Badge>
      </div>

      {files.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <AlertCircle className="h-8 w-8 mx-auto mb-2" />
          <p>No files available in this category</p>
        </div>
      ) : (
        <div className="grid gap-2">
          {files.map((file, index) => {
            const IconComponent = getFileIcon(file.name)
            return (
              <div
                key={index}
                className={`p-3 border rounded-lg cursor-pointer transition-all hover:shadow-md ${
                  selectedFile?.path === file.path
                    ? "border-blue-500 bg-blue-50"
                    : "border-gray-200 hover:border-gray-300"
                }`}
                onClick={() => handleFileSelect(file)}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <IconComponent className="h-4 w-4 text-gray-600" />
                    <div>
                      <div className="font-medium text-sm">{file.name}</div>
                      <div className="text-xs text-gray-500">
                        {formatFileSize(file.size)} • {formatDate(file.lastModified)}
                      </div>
                    </div>
                  </div>
                  <Button variant="ghost" size="sm">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading Bollywood dataset...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold text-gray-900 mb-2">Dataset Explorer</h1>
              <p className="text-gray-600">
                Browse and analyze the comprehensive Bollywood dataset for gender bias patterns.
              </p>
            </div>
            <Button onClick={loadAllData} variant="outline">
              <RefreshCw className="h-4 w-4 mr-2" />
              Refresh Data
            </Button>
          </div>

          {/* Status Cards */}
          <div className="grid md:grid-cols-2 gap-4 mb-6">
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  {githubStatus.available ? (
                    <CheckCircle className="h-5 w-5 text-green-600" />
                  ) : (
                    <AlertCircle className="h-5 w-5 text-red-600" />
                  )}
                  <div>
                    <div className="font-medium">
                      GitHub API Status: {githubStatus.available ? "Available" : "Unavailable"}
                    </div>
                    <div className="text-sm text-gray-600">
                      Rate limit: {githubStatus.rateLimit.remaining}/{githubStatus.rateLimit.total}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <Globe className="h-5 w-5 text-blue-600" />
                  <div>
                    <div className="font-medium">Source: BollywoodData/Bollywood-Data GitHub Repository</div>
                    <div className="text-sm text-gray-600">Comprehensive dataset of Hindi films from 1970-2017</div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {usingMockData && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
              <div className="flex items-center gap-2">
                <AlertCircle className="h-5 w-5 text-yellow-600" />
                <span className="font-medium text-yellow-800">
                  Currently showing sample data due to GitHub API limitations
                </span>
              </div>
            </div>
          )}
        </div>

        <div className="grid lg:grid-cols-3 gap-8">
          {/* File Browser */}
          <div className="lg:col-span-1">
            <Card>
              <CardHeader>
                <CardTitle>Browse Files</CardTitle>
                <CardDescription>Select a file to view its content and analyze for bias</CardDescription>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="scripts" className="w-full">
                  <TabsList className="grid w-full grid-cols-4">
                    <TabsTrigger value="scripts">Scripts</TabsTrigger>
                    <TabsTrigger value="wikipedia">Wikipedia</TabsTrigger>
                    <TabsTrigger value="trailers">Trailers</TabsTrigger>
                    <TabsTrigger value="images">Images</TabsTrigger>
                  </TabsList>

                  <TabsContent value="scripts" className="mt-4">
                    <FileList files={scriptsData} category="Scripts" />
                  </TabsContent>

                  <TabsContent value="wikipedia" className="mt-4">
                    <FileList files={wikipediaData} category="Wikipedia" />
                  </TabsContent>

                  <TabsContent value="trailers" className="mt-4">
                    <FileList files={trailersData} category="Trailers" />
                  </TabsContent>

                  <TabsContent value="images" className="mt-4">
                    <FileList files={imagesData} category="Images" />
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>
          </div>

          {/* File Content Viewer */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>File Content Viewer</CardTitle>
                    <CardDescription>
                      {selectedFile ? `Viewing: ${selectedFile.name}` : "Select a file to view its content"}
                    </CardDescription>
                  </div>
                  {selectedFile && (
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm" onClick={analyzeFileForBias}>
                        <Search className="h-4 w-4 mr-1" />
                        Analyze This File for Bias
                      </Button>
                      <Button variant="outline" size="sm">
                        <Download className="h-4 w-4 mr-1" />
                        Download
                      </Button>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent>
                {!selectedFile ? (
                  <div className="text-center py-12 text-gray-500">
                    <FileText className="h-12 w-12 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Select a File</h3>
                    <p>Choose a file from the browser to view its content and analyze for gender bias patterns.</p>
                  </div>
                ) : contentLoading ? (
                  <div className="text-center py-12">
                    <RefreshCw className="h-8 w-8 animate-spin mx-auto mb-4" />
                    <p className="text-gray-600">Loading file content...</p>
                  </div>
                ) : (
                  <div>
                    <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                      <div className="flex items-center justify-between text-sm">
                        <span>
                          <strong>File:</strong> {selectedFile.name}
                        </span>
                        <span>
                          <strong>Size:</strong> {formatFileSize(selectedFile.size)}
                        </span>
                      </div>
                      <div className="flex items-center justify-between text-sm mt-1">
                        <span>
                          <strong>Path:</strong> {selectedFile.path}
                        </span>
                        <span>
                          <strong>Modified:</strong> {formatDate(selectedFile.lastModified)}
                        </span>
                      </div>
                    </div>

                    <ScrollArea className="h-96 w-full border rounded-lg p-4">
                      <pre className="text-sm whitespace-pre-wrap font-mono">{fileContent}</pre>
                    </ScrollArea>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
