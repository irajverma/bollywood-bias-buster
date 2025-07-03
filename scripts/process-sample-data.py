import pandas as pd
import json
import re
from typing import Dict, List, Any

# Sample Bollywood movie data for testing when GitHub access fails
SAMPLE_DATA = [
    {
        "title": "Kaho Naa Pyaar Hai",
        "year": 2000,
        "script_excerpt": """
        Rohit is an aspiring singer who works as a salesman in a car showroom run by Malik. 
        One day he meets Sonia Saxena, daughter of Mr Saxena, when he goes to deliver a car 
        to her as a birthday present. Sonia is beautiful and comes from a wealthy family.
        """,
        "director": "Rakesh Roshan"
    },
    {
        "title": "Dilwale Dulhania Le Jayenge",
        "year": 1995,
        "script_excerpt": """
        Raj is a fun-loving, carefree young man who lives in London with his father. 
        Simran is the daughter of Baldev Singh, a strict Punjabi man. She is obedient 
        and follows her father's wishes. Simran is engaged to marry her father's friend's son.
        """,
        "director": "Aditya Chopra"
    },
    {
        "title": "Queen",
        "year": 2013,
        "script_excerpt": """
        Rani is a shy, traditional girl from Delhi who works in her family's sweet shop. 
        After her fiancé calls off their wedding, she decides to go on her honeymoon alone. 
        Rani transforms from a dependent girl to an independent woman during her journey.
        """,
        "director": "Vikas Bahl"
    },
    {
        "title": "Dangal",
        "year": 2016,
        "script_excerpt": """
        Mahavir Singh Phogat is a former wrestler who trains his daughters Geeta and Babita 
        to become world-class wrestlers. Geeta becomes the first Indian female wrestler to 
        win gold at the Commonwealth Games. Both daughters break stereotypes in sports.
        """,
        "director": "Nitesh Tiwari"
    },
    {
        "title": "Mughal-E-Azam",
        "year": 1960,
        "script_excerpt": """
        Prince Salim is the heir to the Mughal throne and falls in love with Anarkali, 
        a court dancer. Anarkali is a talented performer who captures the prince's heart. 
        Emperor Akbar opposes their love due to class differences.
        """,
        "director": "K. Asif"
    }
]

class SampleBiasAnalyzer:
    """Analyze sample Bollywood data for gender bias patterns"""
    
    def __init__(self):
        self.male_indicators = ['he', 'his', 'him', 'son', 'brother', 'father', 'husband', 'prince', 'man', 'boy']
        self.female_indicators = ['she', 'her', 'hers', 'daughter', 'sister', 'mother', 'wife', 'princess', 'woman', 'girl']
        
    def extract_characters(self, text: str) -> List[Dict[str, Any]]:
        """Extract character information from text"""
        characters = []
        
        # Character patterns
        patterns = [
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:a|an)\s+([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+works?\s+(?:as|in)\s+([^.!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+(?:the\s+)?daughter\s+of\s+([^,!?]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),?\s+(?:the\s+)?son\s+of\s+([^,!?]+)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match.group(1).strip()
                description = match.group(2).strip() if len(match.groups()) > 1 else ""
                
                gender = self.detect_gender(name, description, text)
                
                characters.append({
                    'name': name,
                    'description': description,
                    'gender': gender,
                    'introduction_context': match.group(0)
                })
        
        return characters
    
    def detect_gender(self, name: str, description: str, full_text: str) -> str:
        """Detect character gender"""
        context = (name + " " + description + " " + full_text).lower()
        
        male_count = sum(context.count(indicator) for indicator in self.male_indicators)
        female_count = sum(context.count(indicator) for indicator in self.female_indicators)
        
        if male_count > female_count:
            return 'male'
        elif female_count > male_count:
            return 'female'
        else:
            return 'unknown'
    
    def calculate_bias_scores(self, characters: List[Dict], text: str) -> Dict[str, float]:
        """Calculate bias scores"""
        male_chars = [c for c in characters if c['gender'] == 'male']
        female_chars = [c for c in characters if c['gender'] == 'female']
        
        scores = {
            'occupation_gap': self.calculate_occupation_gap(male_chars, female_chars),
            'agency_gap': self.calculate_agency_gap(male_chars, female_chars, text),
            'appearance_focus': self.calculate_appearance_focus(male_chars, female_chars, text),
            'relationship_defining': self.calculate_relationship_defining(male_chars, female_chars)
        }
        
        scores['overall'] = sum(scores.values()) / len(scores)
        return scores
    
    def calculate_occupation_gap(self, male_chars: List[Dict], female_chars: List[Dict]) -> float:
        """Calculate occupation gap score"""
        if not female_chars:
            return 0
        
        profession_keywords = ['works', 'job', 'career', 'profession', 'doctor', 'engineer', 'teacher', 'singer', 'dancer']
        
        male_with_profession = sum(1 for char in male_chars 
                                 if any(keyword in char['description'].lower() for keyword in profession_keywords))
        female_with_profession = sum(1 for char in female_chars 
                                   if any(keyword in char['description'].lower() for keyword in profession_keywords))
        
        male_ratio = male_with_profession / len(male_chars) if male_chars else 0
        female_ratio = female_with_profession / len(female_chars) if female_chars else 0
        
        return max(0, (male_ratio - female_ratio) * 100)
    
    def calculate_agency_gap(self, male_chars: List[Dict], female_chars: List[Dict], text: str) -> float:
        """Calculate agency gap score"""
        active_verbs = ['decides', 'chooses', 'leads', 'creates', 'fights', 'wins', 'transforms', 'becomes']
        passive_verbs = ['receives', 'gets', 'is given', 'waits', 'follows', 'obeys']
        
        text_lower = text.lower()
        
        male_agency = sum(text_lower.count(f"{char['name'].lower()} {verb}") for char in male_chars for verb in active_verbs)
        female_agency = sum(text_lower.count(f"{char['name'].lower()} {verb}") for char in female_chars for verb in active_verbs)
        
        male_passive = sum(text_lower.count(f"{char['name'].lower()} {verb}") for char in male_chars for verb in passive_verbs)
        female_passive = sum(text_lower.count(f"{char['name'].lower()} {verb}") for char in female_chars for verb in passive_verbs)
        
        male_score = (male_agency - male_passive) / len(male_chars) if male_chars else 0
        female_score = (female_agency - female_passive) / len(female_chars) if female_chars else 0
        
        return max(0, (male_score - female_score) * 20)
    
    def calculate_appearance_focus(self, male_chars: List[Dict], female_chars: List[Dict], text: str) -> float:
        """Calculate appearance focus bias"""
        appearance_words = ['beautiful', 'pretty', 'gorgeous', 'attractive', 'stunning', 'lovely', 'handsome']
        
        text_lower = text.lower()
        
        male_appearance = sum(text_lower.count(f"{char['name'].lower()} is {word}") for char in male_chars for word in appearance_words)
        female_appearance = sum(text_lower.count(f"{char['name'].lower()} is {word}") for char in female_chars for word in appearance_words)
        
        male_ratio = male_appearance / len(male_chars) if male_chars else 0
        female_ratio = female_appearance / len(female_chars) if female_chars else 0
        
        return max(0, (female_ratio - male_ratio) * 50)
    
    def calculate_relationship_defining(self, male_chars: List[Dict], female_chars: List[Dict]) -> float:
        """Calculate relationship defining bias"""
        relationship_words = ['daughter', 'wife', 'girlfriend', 'sister', 'mother', 'son', 'husband', 'boyfriend', 'brother', 'father']
        
        male_relationship = sum(1 for char in male_chars 
                              if any(word in char['description'].lower() for word in relationship_words))
        female_relationship = sum(1 for char in female_chars 
                                if any(word in char['description'].lower() for word in relationship_words))
        
        male_ratio = male_relationship / len(male_chars) if male_chars else 0
        female_ratio = female_relationship / len(female_chars) if female_chars else 0
        
        return max(0, (female_ratio - male_ratio) * 100)
    
    def analyze_movie(self, movie_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a single movie for bias"""
        characters = self.extract_characters(movie_data['script_excerpt'])
        bias_scores = self.calculate_bias_scores(characters, movie_data['script_excerpt'])
        
        return {
            'title': movie_data['title'],
            'year': movie_data['year'],
            'director': movie_data['director'],
            'characters': characters,
            'character_count': len(characters),
            'male_characters': len([c for c in characters if c['gender'] == 'male']),
            'female_characters': len([c for c in characters if c['gender'] == 'female']),
            'bias_scores': bias_scores,
            'sample_excerpts': self.extract_bias_examples(characters, movie_data['script_excerpt'])
        }
    
    def extract_bias_examples(self, characters: List[Dict], text: str) -> List[Dict[str, str]]:
        """Extract examples of bias from the text"""
        examples = []
        
        for char in characters:
            if 'daughter of' in char['introduction_context'].lower():
                examples.append({
                    'type': 'Occupation Gap',
                    'character': char['name'],
                    'excerpt': char['introduction_context'],
                    'issue': 'Character introduced only through family relationship'
                })
            
            if char['gender'] == 'female' and 'beautiful' in char['description'].lower():
                examples.append({
                    'type': 'Appearance Focus',
                    'character': char['name'],
                    'excerpt': char['introduction_context'],
                    'issue': 'Female character described primarily by appearance'
                })
        
        return examples

def main():
    """Main function to process sample data"""
    print("=== BOLLYWOOD BIAS ANALYSIS - SAMPLE DATA ===\n")
    
    analyzer = SampleBiasAnalyzer()
    results = []
    
    print("Processing sample movies...")
    for movie in SAMPLE_DATA:
        print(f"Analyzing: {movie['title']} ({movie['year']})")
        analysis = analyzer.analyze_movie(movie)
        results.append(analysis)
    
    # Create summary report
    total_characters = sum(r['character_count'] for r in results)
    total_male = sum(r['male_characters'] for r in results)
    total_female = sum(r['female_characters'] for r in results)
    
    avg_bias_scores = {
        'occupation_gap': sum(r['bias_scores']['occupation_gap'] for r in results) / len(results),
        'agency_gap': sum(r['bias_scores']['agency_gap'] for r in results) / len(results),
        'appearance_focus': sum(r['bias_scores']['appearance_focus'] for r in results) / len(results),
        'relationship_defining': sum(r['bias_scores']['relationship_defining'] for r in results) / len(results),
        'overall': sum(r['bias_scores']['overall'] for r in results) / len(results)
    }
    
    report = {
        'summary': {
            'movies_analyzed': len(results),
            'total_characters': total_characters,
            'male_characters': total_male,
            'female_characters': total_female,
            'gender_ratio': f"{total_male}:{total_female}",
            'average_bias_scores': avg_bias_scores
        },
        'detailed_results': results,
        'decade_analysis': analyze_by_decade(results),
        'bias_examples': extract_all_bias_examples(results)
    }
    
    # Save results
    df = pd.DataFrame([{
        'title': r['title'],
        'year': r['year'],
        'director': r['director'],
        'character_count': r['character_count'],
        'male_characters': r['male_characters'],
        'female_characters': r['female_characters'],
        'occupation_gap': r['bias_scores']['occupation_gap'],
        'agency_gap': r['bias_scores']['agency_gap'],
        'appearance_focus': r['bias_scores']['appearance_focus'],
        'relationship_defining': r['bias_scores']['relationship_defining'],
        'overall_bias': r['bias_scores']['overall']
    } for r in results])
    
    df.to_csv('sample_bollywood_analysis.csv', index=False)
    
    with open('sample_bias_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    # Print summary
    print("\n" + "="*50)
    print("ANALYSIS SUMMARY")
    print("="*50)
    print(f"Movies analyzed: {len(results)}")
    print(f"Total characters: {total_characters}")
    print(f"Gender distribution: {total_male} male, {total_female} female")
    print(f"Gender ratio (M:F): {total_male}:{total_female}")
    
    print(f"\nAverage Bias Scores (0-100, higher = more biased):")
    for bias_type, score in avg_bias_scores.items():
        print(f"- {bias_type.replace('_', ' ').title()}: {score:.1f}")
    
    print(f"\nTop Biased Movies:")
    sorted_movies = sorted(results, key=lambda x: x['bias_scores']['overall'], reverse=True)
    for movie in sorted_movies[:3]:
        print(f"- {movie['title']} ({movie['year']}): {movie['bias_scores']['overall']:.1f}")
    
    print(f"\nLeast Biased Movies:")
    for movie in sorted_movies[-2:]:
        print(f"- {movie['title']} ({movie['year']}): {movie['bias_scores']['overall']:.1f}")
    
    print(f"\n✅ Analysis complete! Results saved to:")
    print("- sample_bollywood_analysis.csv")
    print("- sample_bias_report.json")

def analyze_by_decade(results: List[Dict]) -> Dict[str, Any]:
    """Analyze bias trends by decade"""
    decades = {}
    for result in results:
        decade = (result['year'] // 10) * 10
        decade_key = f"{decade}s"
        
        if decade_key not in decades:
            decades[decade_key] = []
        decades[decade_key].append(result)
    
    decade_analysis = {}
    for decade, movies in decades.items():
        avg_bias = sum(m['bias_scores']['overall'] for m in movies) / len(movies)
        decade_analysis[decade] = {
            'movie_count': len(movies),
            'average_bias': avg_bias,
            'movies': [m['title'] for m in movies]
        }
    
    return decade_analysis

def extract_all_bias_examples(results: List[Dict]) -> List[Dict]:
    """Extract all bias examples from results"""
    all_examples = []
    for result in results:
        for example in result['sample_excerpts']:
            example['movie'] = result['title']
            example['year'] = result['year']
            all_examples.append(example)
    return all_examples

if __name__ == "__main__":
    main()
