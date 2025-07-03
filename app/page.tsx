import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, BarChart3, FileText, Zap } from "lucide-react"
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-pink-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">Bollywood Bias Buster</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            AI-powered application to identify gender stereotypes in Bollywood films, quantify bias, and generate
            inclusive alternatives for scripts and posters.
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Upload className="h-8 w-8 text-purple-600 mb-2" />
              <CardTitle className="text-lg">Script Analysis</CardTitle>
              <CardDescription>Upload and analyze movie scripts for gender stereotypes</CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/analyze">
                <Button className="w-full">Start Analysis</Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <BarChart3 className="h-8 w-8 text-blue-600 mb-2" />
              <CardTitle className="text-lg">Bias Dashboard</CardTitle>
              <CardDescription>View bias trends across decades, genres, and directors</CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/dashboard">
                <Button variant="outline" className="w-full bg-transparent">
                  View Dashboard
                </Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <Zap className="h-8 w-8 text-green-600 mb-2" />
              <CardTitle className="text-lg">AI Rewrites</CardTitle>
              <CardDescription>Generate bias-free alternatives while preserving narrative</CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/rewrite">
                <Button variant="outline" className="w-full bg-transparent">
                  Generate Rewrites
                </Button>
              </Link>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <FileText className="h-8 w-8 text-orange-600 mb-2" />
              <CardTitle className="text-lg">Bias Reports</CardTitle>
              <CardDescription>Generate comprehensive feedback reports for filmmakers</CardDescription>
            </CardHeader>
            <CardContent>
              <Link href="/reports">
                <Button variant="outline" className="w-full bg-transparent">
                  View Reports
                </Button>
              </Link>
            </CardContent>
          </Card>
        </div>

        {/* Problem Statement */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="text-2xl">Problem Statement</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <p className="text-gray-700">
              Gender stereotypes are prevalent in Indian cinema, often manifesting in how characters are introduced and
              portrayed. Our AI system addresses this by:
            </p>
            <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-400">
              <p className="font-medium text-yellow-800 mb-2">Example from "Kaho Naa... Pyaar Hai":</p>
              <p className="text-yellow-700 italic">
                "Rohit is an aspiring singer who works as a salesman in a car showroom run by Malik. One day he meets
                Sonia Saxena, daughter of Mr Saxena..."
              </p>
              <p className="text-yellow-700 mt-2">
                <strong>Issue:</strong> Men are introduced with profession and aspirations; women only as "daughter of"
                - an "occupation gap" stereotype.
              </p>
            </div>
            <div className="grid md:grid-cols-2 gap-4 mt-6">
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Detection Capabilities:</h4>
                <ul className="text-gray-700 space-y-1">
                  <li>• Character gender identification</li>
                  <li>• Role attribute analysis</li>
                  <li>• Stereotype categorization</li>
                  <li>• Visual bias detection</li>
                </ul>
              </div>
              <div>
                <h4 className="font-semibold text-gray-900 mb-2">Output Features:</h4>
                <ul className="text-gray-700 space-y-1">
                  <li>• Bias quantification scores</li>
                  <li>• Trend visualizations</li>
                  <li>• Remediation suggestions</li>
                  <li>• Comprehensive reports</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Dataset Info */}
        <Card>
          <CardHeader>
            <CardTitle>Real Dataset Integration</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-700 mb-4">
              Using the comprehensive Bollywood dataset from GitHub (1970-2017) including:
            </p>
            <div className="grid md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-lg font-bold text-blue-600">Scripts</div>
                <div className="text-sm text-blue-700">Movie Scripts Data</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-lg font-bold text-green-600">Wikipedia</div>
                <div className="text-sm text-green-700">Plot Synopses</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-lg font-bold text-purple-600">Trailers</div>
                <div className="text-sm text-purple-700">Trailer Transcripts</div>
              </div>
              <div className="text-center p-4 bg-orange-50 rounded-lg">
                <div className="text-lg font-bold text-orange-600">Images</div>
                <div className="text-sm text-orange-700">Movie Posters</div>
              </div>
            </div>
            <div className="mt-4 p-3 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-600">
                <strong>Source:</strong>
                <a
                  href="https://github.com/BollywoodData/Bollywood-Data"
                  className="text-blue-600 hover:underline ml-1"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  github.com/BollywoodData/Bollywood-Data
                </a>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
