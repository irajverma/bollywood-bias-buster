# 🎬 Bollywood Bias Buster

[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0-38B2AC)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB)](https://www.python.org/)


> **Analyzing and eliminating gender bias in Bollywood cinema through AI-powered script analysis**

A comprehensive web application that uses machine learning and natural language processing to detect, analyze, and provide solutions for gender bias in Bollywood movie scripts, plots, and dialogues.
**Live Link**: [Link](https://bollywood-bias-buster.vercel.app/)
## 🌟 Features

### 🔍 **Script Analysis**
- **Real-time bias detection** in movie scripts and dialogues
- **Gender stereotype identification** with detailed explanations
- **Character role analysis** and representation metrics
- **Interactive bias scoring** with visual indicators

### 📊 **Data Visualization**
- **Comprehensive dashboard** with bias trends over time
- **Interactive charts** showing gender representation statistics
- **Movie comparison tools** for bias analysis
- **Export capabilities** for research and reporting

### ✍️ **Content Rewriting**
- **AI-powered script rewriting** to eliminate detected bias
- **Alternative dialogue suggestions** with context preservation
- **Character development recommendations**
- **Before/after comparison views**

### 📈 **Reporting & Analytics**
- **Detailed bias reports** with actionable insights
- **PDF export functionality** for sharing and documentation
- **Email sharing capabilities** for collaboration
- **Historical trend analysis** across Bollywood cinema

### 🗃️ **Dataset Explorer**
- **Browse comprehensive Bollywood dataset** (1970-2017)
- **Search and filter** movies by various criteria
- **View movie scripts, plots, and metadata**
- **Real-time GitHub integration** with fallback mock data

## 🛠️ Tech Stack

### **Frontend**
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Modern component library
- **Recharts** - Data visualization
- **Lucide React** - Icon library

### **Backend**
- **Next.js API Routes** - Serverless functions
- **Python** - Data processing and ML models
- **Pandas & NumPy** - Data manipulation
- **Scikit-learn** - Machine learning
- **NLTK** - Natural language processing

### **Data & APIs**
- **GitHub API** - Dataset integration
- **Bollywood Dataset** - Comprehensive movie database
- **Mock Data Fallback** - Ensures functionality without API limits

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.8+
- Git

### Installation

1. **Clone the repository**
bash
git clone https://github.com/yourusername/bollywood-bias-buster.git
cd bollywood-bias-buster

2. **Install dependencies**

# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt

3. **Set up environment variables**
# Create .env.local file
cp .env.example .env.local

# Add your GitHub token (optional, for dataset access)
GITHUB_TOKEN=your_github_token_here


4. **Run the development server**
npm run dev


5. **Open your browser**
Navigate to [http://localhost:3000](http://localhost:3000)

## 📖 Usage Guide

### 🎯 **Analyzing Scripts**
1. Go to the **Analyze** page
2. Paste your script or dialogue text
3. Click **"Analyze for Bias"**
4. Review the detailed bias report with scores and explanations

### 📊 **Exploring Data**
1. Visit the **Data Explorer** page
2. Browse through movie scripts, plots, and trailers
3. Click on any file to view its content
4. Use the **"Analyze This File"** button for bias analysis

### ✏️ **Rewriting Content**
1. Navigate to the **Rewrite** page
2. Input biased text that needs improvement
3. Click **"Generate Bias-Free Version"**
4. Compare original vs. rewritten content

### 📈 **Viewing Reports**
1. Access the **Reports** page
2. Review comprehensive bias analysis
3. Download PDF reports or share via email
4. Track improvements over time

## 🔧 API Endpoints

### **POST /api/analyze**
Analyze text for gender bias
javascript
const response = await fetch('/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Your script text here' })
});


### **POST /api/rewrite**
Generate bias-free alternatives
javascript
const response = await fetch('/api/rewrite', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ text: 'Biased text to rewrite' })
});


### **GET /api/dataset**
Access Bollywood dataset
javascript
const response = await fetch('/api/dataset?category=scripts&limit=10');




## 🧪 Testing

### **Run Python Tests**
# Run bias detection tests
python test_samples/quick_test_runner.py

# Run step-by-step analysis
python test_samples/step_by_step_test.py

### **Run Frontend Tests**

# Run Next.js development server
npm run dev

# Test all pages and functionality
npm run test


## 📊 Dataset Information

### **Bollywood Dataset (1970-2017)**
- **5,000+ movies** with comprehensive metadata
- **Movie scripts** and dialogue transcripts
- **Plot summaries** from Wikipedia
- **Trailer transcripts** and promotional content
- **Cast and crew information**
- **Box office and rating data**

### **Data Sources**
- GitHub: `BollywoodData/Bollywood-Data`
- Wikipedia plot summaries
- IMDb metadata
- Trailer transcriptions

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### **Development Guidelines**
- Follow TypeScript best practices
- Use Tailwind CSS for styling
- Write comprehensive tests
- Update documentation as needed

## 🚧 Known Limitations

- **GitHub API rate limits** may affect dataset access
- **Mock data fallback** ensures functionality during limits
- **AI analysis** requires internet connection
- **Large datasets** may take time to process

## 🗺️ Roadmap

### **Phase 1: Core Features** ✅
- [x] Basic bias detection
- [x] Script analysis interface
- [x] Data visualization dashboard
- [x] Content rewriting functionality

### **Phase 2: Advanced Analytics** 🚧
- [ ] Machine learning model improvements
- [ ] Real-time collaboration features
- [ ] Advanced reporting capabilities
- [ ] Mobile app development

### **Phase 3: Community Features** 📋
- [ ] User authentication and profiles
- [ ] Community script sharing
- [ ] Collaborative bias detection
- [ ] Educational resources and tutorials



## 🙏 Acknowledgments

- **Bollywood Dataset** contributors for comprehensive movie data
- **shadcn/ui** for beautiful component library
- **Next.js team** for the amazing framework
- **Open source community** for tools and libraries

## 📞 Support

- **Email**: i.rajverma8423@gmail.com.com
- **Linkedin**: [Linkedin](https://www.linkedin.com/in/raj-verma-459320232/)

---

**Made with ❤️ for a more inclusive Bollywood**

*Empowering filmmakers to create bias-free content through AI-powered analysis*
