"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { TrendingUp, Users, Film } from "lucide-react"

export default function DashboardPage() {
  // Mock data for visualization
  const biasMetrics = {
    overallBias: 68,
    occupationGap: 75,
    agencyGap: 62,
    appearanceFocus: 71,
    relationshipDefining: 69,
  }

  const decadeTrends = [
    { decade: "1970s", bias: 82, films: 156 },
    { decade: "1980s", bias: 79, films: 203 },
    { decade: "1990s", bias: 74, films: 287 },
    { decade: "2000s", bias: 69, films: 342 },
    { decade: "2010s", bias: 58, films: 398 },
  ]

  const topDirectors = [
    { name: "Yash Chopra", films: 23, avgBias: 72 },
    { name: "Karan Johar", films: 18, avgBias: 69 },
    { name: "Sanjay Leela Bhansali", films: 15, avgBias: 74 },
    { name: "Rajkumar Hirani", films: 12, avgBias: 45 },
    { name: "Zoya Akhtar", films: 8, avgBias: 38 },
  ]

  const genreAnalysis = [
    { genre: "Romance", bias: 78, count: 245 },
    { genre: "Drama", bias: 65, count: 189 },
    { genre: "Action", bias: 71, count: 167 },
    { genre: "Comedy", bias: 59, count: 134 },
    { genre: "Thriller", bias: 62, count: 98 },
  ]

  const getBiasColor = (score: number) => {
    if (score > 70) return "text-red-600"
    if (score > 50) return "text-yellow-600"
    return "text-green-600"
  }

  const getBiasLabel = (score: number) => {
    if (score > 70) return "High Bias"
    if (score > 50) return "Moderate Bias"
    return "Low Bias"
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Bias Dashboard</h1>
          <p className="text-gray-600">
            Comprehensive analysis of gender bias trends across Bollywood cinema (1970-2017)
          </p>
        </div>

        {/* Overall Metrics */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Overall Bias Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="text-2xl font-bold text-gray-900">{biasMetrics.overallBias}/100</div>
                <Badge variant="secondary" className={getBiasColor(biasMetrics.overallBias)}>
                  {getBiasLabel(biasMetrics.overallBias)}
                </Badge>
              </div>
              <Progress value={biasMetrics.overallBias} className="mt-2" />
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Films Analyzed</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <Film className="h-5 w-5 text-blue-600" />
                <div className="text-2xl font-bold text-gray-900">1,247</div>
              </div>
              <div className="text-sm text-gray-500 mt-1">Across 47 years</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Characters Analyzed</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <Users className="h-5 w-5 text-green-600" />
                <div className="text-2xl font-bold text-gray-900">15,432</div>
              </div>
              <div className="text-sm text-gray-500 mt-1">Male: 8,901 | Female: 6,531</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">Improvement Trend</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-purple-600" />
                <div className="text-2xl font-bold text-gray-900">-24%</div>
              </div>
              <div className="text-sm text-gray-500 mt-1">Bias reduction since 1970s</div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 mb-8">
          {/* Bias Categories */}
          <Card>
            <CardHeader>
              <CardTitle>Bias Categories</CardTitle>
              <CardDescription>Breakdown by stereotype type</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Occupation Gap</span>
                    <span className={getBiasColor(biasMetrics.occupationGap)}>{biasMetrics.occupationGap}%</span>
                  </div>
                  <Progress value={biasMetrics.occupationGap} />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Appearance Focus</span>
                    <span className={getBiasColor(biasMetrics.appearanceFocus)}>{biasMetrics.appearanceFocus}%</span>
                  </div>
                  <Progress value={biasMetrics.appearanceFocus} />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Relationship Defining</span>
                    <span className={getBiasColor(biasMetrics.relationshipDefining)}>
                      {biasMetrics.relationshipDefining}%
                    </span>
                  </div>
                  <Progress value={biasMetrics.relationshipDefining} />
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span>Agency Gap</span>
                    <span className={getBiasColor(biasMetrics.agencyGap)}>{biasMetrics.agencyGap}%</span>
                  </div>
                  <Progress value={biasMetrics.agencyGap} />
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Decade Trends */}
          <Card>
            <CardHeader>
              <CardTitle>Decade-wise Trends</CardTitle>
              <CardDescription>Bias evolution over time</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {decadeTrends.map((decade) => (
                  <div key={decade.decade} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-16 text-sm font-medium">{decade.decade}</div>
                      <div className="flex-1">
                        <Progress value={decade.bias} className="w-32" />
                      </div>
                    </div>
                    <div className="flex items-center gap-4 text-sm">
                      <span className={getBiasColor(decade.bias)}>{decade.bias}%</span>
                      <span className="text-gray-500">{decade.films} films</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Director Analysis */}
          <Card>
            <CardHeader>
              <CardTitle>Director Analysis</CardTitle>
              <CardDescription>Bias scores by prominent directors</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topDirectors.map((director, index) => (
                  <div key={director.name} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <div className="font-medium">{director.name}</div>
                      <div className="text-sm text-gray-500">{director.films} films analyzed</div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Progress value={director.avgBias} className="w-20" />
                      <span className={`text-sm font-medium ${getBiasColor(director.avgBias)}`}>
                        {director.avgBias}%
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Genre Analysis */}
          <Card>
            <CardHeader>
              <CardTitle>Genre Analysis</CardTitle>
              <CardDescription>Bias patterns across film genres</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {genreAnalysis.map((genre) => (
                  <div key={genre.genre} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div>
                      <div className="font-medium">{genre.genre}</div>
                      <div className="text-sm text-gray-500">{genre.count} films</div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Progress value={genre.bias} className="w-20" />
                      <span className={`text-sm font-medium ${getBiasColor(genre.bias)}`}>{genre.bias}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
