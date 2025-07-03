interface GitHubFile {
  name: string
  path: string
  sha: string
  size: number
  url: string
  html_url: string
  git_url: string
  download_url: string
  type: string
}

interface ProcessedFile {
  name: string
  path: string
  size: number
  lastModified: string
  content?: string
}

export class BollywoodDataProcessor {
  private baseUrl = "https://api.github.com/repos/BollywoodData/Bollywood-Data/contents"
  private token = process.env.GITHUB_TOKEN

  private getHeaders() {
    const headers: Record<string, string> = {
      Accept: "application/vnd.github.v3+json",
      "User-Agent": "Bollywood-Bias-Buster",
    }

    if (this.token) {
      headers["Authorization"] = `token ${this.token}`
    }

    return headers
  }

  async getScriptsData(): Promise<ProcessedFile[]> {
    try {
      console.log("Fetching scripts data from GitHub...")
      const response = await fetch(`${this.baseUrl}/Scripts`, {
        headers: this.getHeaders(),
      })

      if (!response.ok) {
        console.warn(`GitHub API failed: ${response.status}. Using mock data.`)
        return this.getMockScriptsData()
      }

      const files: GitHubFile[] = await response.json()

      if (!Array.isArray(files) || files.length === 0) {
        console.warn("No scripts found in GitHub. Using mock data.")
        return this.getMockScriptsData()
      }

      const processedFiles = files
        .filter((file) => file.type === "file" && file.name.endsWith(".txt"))
        .map((file) => ({
          name: file.name,
          path: file.path,
          size: file.size,
          lastModified: new Date().toISOString(),
          downloadUrl: file.download_url,
        }))

      console.log(`Found ${processedFiles.length} script files`)
      return processedFiles.length > 0 ? processedFiles : this.getMockScriptsData()
    } catch (error) {
      console.error("Error fetching scripts:", error)
      return this.getMockScriptsData()
    }
  }

  async getWikipediaData(): Promise<ProcessedFile[]> {
    try {
      console.log("Fetching Wikipedia data from GitHub...")
      const response = await fetch(`${this.baseUrl}/Wikipedia`, {
        headers: this.getHeaders(),
      })

      if (!response.ok) {
        console.warn(`GitHub API failed: ${response.status}. Using mock data.`)
        return this.getMockWikipediaData()
      }

      const files: GitHubFile[] = await response.json()

      if (!Array.isArray(files) || files.length === 0) {
        console.warn("No Wikipedia files found. Using mock data.")
        return this.getMockWikipediaData()
      }

      const processedFiles = files
        .filter((file) => file.type === "file")
        .map((file) => ({
          name: file.name,
          path: file.path,
          size: file.size,
          lastModified: new Date().toISOString(),
          downloadUrl: file.download_url,
        }))

      console.log(`Found ${processedFiles.length} Wikipedia files`)
      return processedFiles.length > 0 ? processedFiles : this.getMockWikipediaData()
    } catch (error) {
      console.error("Error fetching Wikipedia data:", error)
      return this.getMockWikipediaData()
    }
  }

  async getTrailersData(): Promise<ProcessedFile[]> {
    try {
      console.log("Fetching trailers data from GitHub...")
      const response = await fetch(`${this.baseUrl}/Trailers`, {
        headers: this.getHeaders(),
      })

      if (!response.ok) {
        console.warn(`GitHub API failed: ${response.status}. Using mock data.`)
        return this.getMockTrailersData()
      }

      const files: GitHubFile[] = await response.json()

      if (!Array.isArray(files) || files.length === 0) {
        console.warn("No trailer files found. Using mock data.")
        return this.getMockTrailersData()
      }

      const processedFiles = files
        .filter((file) => file.type === "file")
        .map((file) => ({
          name: file.name,
          path: file.path,
          size: file.size,
          lastModified: new Date().toISOString(),
          downloadUrl: file.download_url,
        }))

      console.log(`Found ${processedFiles.length} trailer files`)
      return processedFiles.length > 0 ? processedFiles : this.getMockTrailersData()
    } catch (error) {
      console.error("Error fetching trailers data:", error)
      return this.getMockTrailersData()
    }
  }

  async getImagesData(): Promise<ProcessedFile[]> {
    try {
      console.log("Fetching images data from GitHub...")
      const response = await fetch(`${this.baseUrl}/Images`, {
        headers: this.getHeaders(),
      })

      if (!response.ok) {
        console.warn(`GitHub API failed: ${response.status}. Using mock data.`)
        return this.getMockImagesData()
      }

      const files: GitHubFile[] = await response.json()

      if (!Array.isArray(files) || files.length === 0) {
        console.warn("No image files found. Using mock data.")
        return this.getMockImagesData()
      }

      const processedFiles = files
        .filter((file) => file.type === "file" && /\.(jpg|jpeg|png|gif)$/i.test(file.name))
        .map((file) => ({
          name: file.name,
          path: file.path,
          size: file.size,
          lastModified: new Date().toISOString(),
          downloadUrl: file.download_url,
        }))

      console.log(`Found ${processedFiles.length} image files`)
      return processedFiles.length > 0 ? processedFiles : this.getMockImagesData()
    } catch (error) {
      console.error("Error fetching images data:", error)
      return this.getMockImagesData()
    }
  }

  async getFileContent(path: string): Promise<string> {
    try {
      console.log(`Fetching content for: ${path}`)
      const response = await fetch(`${this.baseUrl}/${path}`, {
        headers: this.getHeaders(),
      })

      if (!response.ok) {
        console.warn(`Failed to fetch file content: ${response.status}`)
        return this.getMockFileContent(path)
      }

      const data = await response.json()

      if (data.content) {
        // GitHub returns base64 encoded content
        const content = atob(data.content.replace(/\n/g, ""))
        console.log(`Successfully fetched content for ${path}`)
        return content
      }

      return this.getMockFileContent(path)
    } catch (error) {
      console.error(`Error fetching file content for ${path}:`, error)
      return this.getMockFileContent(path)
    }
  }

  // Mock data methods
  getMockScriptsData(): ProcessedFile[] {
    console.log("Using mock scripts data")
    return [
      {
        name: "Dilwale_Dulhania_Le_Jayenge.txt",
        path: "Scripts/Dilwale_Dulhania_Le_Jayenge.txt",
        size: 45000,
        lastModified: "2024-01-15T10:30:00Z",
      },
      {
        name: "Kuch_Kuch_Hota_Hai.txt",
        path: "Scripts/Kuch_Kuch_Hota_Hai.txt",
        size: 42000,
        lastModified: "2024-01-14T09:15:00Z",
      },
      {
        name: "Queen.txt",
        path: "Scripts/Queen.txt",
        size: 38000,
        lastModified: "2024-01-13T14:20:00Z",
      },
      {
        name: "Dangal.txt",
        path: "Scripts/Dangal.txt",
        size: 41000,
        lastModified: "2024-01-12T16:45:00Z",
      },
      {
        name: "Pink.txt",
        path: "Scripts/Pink.txt",
        size: 39000,
        lastModified: "2024-01-11T11:30:00Z",
      },
    ]
  }

  getMockWikipediaData(): ProcessedFile[] {
    console.log("Using mock Wikipedia data")
    return [
      {
        name: "DDLJ_plot.txt",
        path: "Wikipedia/DDLJ_plot.txt",
        size: 5200,
        lastModified: "2024-01-15T08:00:00Z",
      },
      {
        name: "Queen_plot.txt",
        path: "Wikipedia/Queen_plot.txt",
        size: 4800,
        lastModified: "2024-01-14T12:30:00Z",
      },
      {
        name: "Dangal_plot.txt",
        path: "Wikipedia/Dangal_plot.txt",
        size: 5100,
        lastModified: "2024-01-13T15:45:00Z",
      },
    ]
  }

  getMockTrailersData(): ProcessedFile[] {
    console.log("Using mock trailers data")
    return [
      {
        name: "Queen_trailer_transcript.txt",
        path: "Trailers/Queen_trailer_transcript.txt",
        size: 2400,
        lastModified: "2024-01-12T10:15:00Z",
      },
      {
        name: "Dangal_trailer_transcript.txt",
        path: "Trailers/Dangal_trailer_transcript.txt",
        size: 2600,
        lastModified: "2024-01-11T13:20:00Z",
      },
    ]
  }

  getMockImagesData(): ProcessedFile[] {
    console.log("Using mock images data")
    return [
      {
        name: "DDLJ_poster.jpg",
        path: "Images/DDLJ_poster.jpg",
        size: 156000,
        lastModified: "2024-01-15T07:30:00Z",
      },
      {
        name: "Queen_poster.jpg",
        path: "Images/Queen_poster.jpg",
        size: 142000,
        lastModified: "2024-01-14T11:45:00Z",
      },
      {
        name: "Dangal_poster.jpg",
        path: "Images/Dangal_poster.jpg",
        size: 168000,
        lastModified: "2024-01-13T16:20:00Z",
      },
    ]
  }

  getMockFileContent(path: string): string {
    console.log(`Using mock content for: ${path}`)

    if (path.includes("Dilwale_Dulhania_Le_Jayenge")) {
      return `DILWALE DULHANIA LE JAYENGE - Script Excerpt

FADE IN:

EXT. LONDON STREET - DAY

RAJ MALHOTRA (22), a carefree young man, walks down the street with his friends. He's charming but irresponsible.

RAJ
(to his friends)
Life is all about having fun, yaar. No tensions, no worries.

CUT TO:

INT. SIMRAN'S HOUSE - DAY

SIMRAN SINGH (20), a traditional Indian girl living in London, helps her mother in the kitchen. She dreams of seeing the world but is bound by family traditions.

SIMRAN
(to her mother)
Mama, I wish I could travel and see different places.

MOTHER
Beta, a girl's place is with her family. Soon you'll be married and settled.

This script shows traditional gender roles where the male character is portrayed as carefree and independent, while the female character is shown in domestic settings with limited agency and dreams constrained by family expectations.`
    }

    if (path.includes("Queen")) {
      return `QUEEN - Script Excerpt

FADE IN:

INT. RANI'S BEDROOM - NIGHT

RANI MEHRA (24), a shy Delhi girl, sits on her bed looking at her wedding dress. Tomorrow is her wedding day.

RANI
(to herself)
Tomorrow I'll be Mrs. Vijay Dhingra. My life will finally begin.

CUT TO:

EXT. WEDDING VENUE - DAY

The wedding preparations are in full swing. VIJAY (26), the groom, arrives looking uncomfortable.

VIJAY
(to Rani, privately)
Rani, I can't do this. I'm not ready for marriage. I'm calling off the wedding.

RANI is devastated but later decides to go on her honeymoon alone to Paris.

This script shows a female character who initially conforms to traditional expectations but later demonstrates agency by choosing to travel alone and discover her independence.`
    }

    if (path.includes("plot")) {
      return `Plot Summary:

This is a comprehensive plot summary from Wikipedia, detailing the story arc, character development, and key themes of the movie. The summary provides context for understanding gender representation and character dynamics throughout the narrative.

Key themes include family relationships, personal growth, and societal expectations. The plot analysis helps identify patterns in how male and female characters are portrayed and their respective agency in driving the story forward.`
    }

    if (path.includes("trailer")) {
      return `Trailer Transcript:

[MUSIC SWELLS]

NARRATOR (V.O.)
In a world where dreams meet reality...

[QUICK CUTS OF SCENES]

CHARACTER 1
This is our chance to make a difference.

CHARACTER 2
But are we ready for what comes next?

[DRAMATIC MUSIC]

NARRATOR (V.O.)
Some stories change everything.

This trailer transcript captures the key dialogue and promotional messaging, which often reflects how characters are marketed and their roles emphasized to audiences.`
    }

    return `Sample file content for: ${path}

This is mock content used when the actual GitHub repository data is not accessible. In a real implementation, this would contain the actual script, plot summary, or other content from the Bollywood dataset.

The content would be analyzed for gender bias patterns including:
- Character introductions and descriptions
- Dialogue distribution
- Professional roles and agency
- Relationship dynamics
- Screen time and importance to plot

This mock data helps demonstrate the bias analysis functionality while the actual dataset integration is being developed.`
  }
}
