import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from collections import defaultdict
import numpy as np

@dataclass
class Character:
    name: str
    gender: str
    professions: List[str]
    relationships: List[str]
    agency_level: int
    appearance_descriptions: List[str]
    dialogue_count: int
    screen_time: float

@dataclass
class BiasScores:
    occupation_gap: float
    agency_gap: float
    appearance_focus: float
    relationship_defining: float
    dialogue_imbalance: float
    screen_time_imbalance: float
    overall: float

class ComprehensiveGenderBiasDetector:
    def __init__(self):
        self.female_names = {
            'priya', 'simran', 'rani', 'meera', 'sonia', 'kavya', 'anjali', 
            'pooja', 'neha', 'ritu', 'deepika', 'kareena', 'aishwarya'
        }
        self.male_names = {
            'raj', 'rohit', 'vijay', 'arjun', 'rahul', 'amit', 'suresh', 
            'ravi', 'kumar', 'dev', 'shah', 'khan', 'sharma'
        }
        
        self.professions = [
            'doctor', 'engineer', 'teacher', 'lawyer', 'businessman', 
            'scientist', 'artist', 'writer', 'director', 'manager',
            'housewife', 'student', 'nurse', 'secretary'
        ]
        
        self.appearance_words = [
            'beautiful', 'pretty', 'gorgeous', 'stunning', 'attractive',
            'handsome', 'charming', 'elegant', 'lovely', 'cute'
        ]
        
        self.relationship_indicators = [
            'daughter of', 'son of', 'wife of', 'husband of', 
            'mother of', 'father of', 'girlfriend', 'boyfriend',
            'sister of', 'brother of'
        ]

    def extract_characters_advanced(self, text: str) -> List[Character]:
        """Extract characters with comprehensive analysis"""
        characters = []
        
        # Find character names (capitalized words that appear multiple times)
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        name_counts = defaultdict(int)
        for word in words:
            name_counts[word] += 1
        
        # Filter for likely character names (appear 2+ times, not common words)
        common_words = {'The', 'And', 'But', 'For', 'With', 'From', 'This', 'That'}
        potential_names = [name for name, count in name_counts.items() 
                          if count >= 2 and name not in common_words]
        
        for name in potential_names[:10]:  # Limit to top 10 characters
            character = self._analyze_character(name, text)
            if character:
                characters.append(character)
        
        return characters

    def _analyze_character(self, name: str, text: str) -> Optional[Character]:
        """Analyze individual character"""
        # Get all sentences mentioning this character
        sentences = re.split(r'[.!?]+', text)
        character_sentences = [s for s in sentences if name.lower() in s.lower()]
        
        if not character_sentences:
            return None
        
        character_text = ' '.join(character_sentences)
        
        return Character(
            name=name,
            gender=self._detect_gender(name, character_text),
            professions=self._find_professions(character_text),
            relationships=self._find_relationships(character_text),
            agency_level=self._calculate_agency_level(character_text),
            appearance_descriptions=self._find_appearance_descriptions(character_text),
            dialogue_count=self._count_dialogue(name, text),
            screen_time=self._estimate_screen_time(name, text)
        )

    def _detect_gender(self, name: str, context: str) -> str:
        """Detect character gender"""
        name_lower = name.lower()
        
        # Check against known names
        if any(fn in name_lower for fn in self.female_names):
            return 'female'
        if any(mn in name_lower for mn in self.male_names):
            return 'male'
        
        # Check pronouns in context
        context_lower = context.lower()
        female_pronouns = context_lower.count('she') + context_lower.count('her')
        male_pronouns = context_lower.count('he') + context_lower.count('him')
        
        if female_pronouns > male_pronouns:
            return 'female'
        elif male_pronouns > female_pronouns:
            return 'male'
        
        return 'unknown'

    def _find_professions(self, text: str) -> List[str]:
        """Find character professions"""
        found_professions = []
        text_lower = text.lower()
        
        for profession in self.professions:
            if profession in text_lower:
                found_professions.append(profession)
        
        return found_professions

    def _find_relationships(self, text: str) -> List[str]:
        """Find character relationships"""
        relationships = []
        text_lower = text.lower()
        
        for indicator in self.relationship_indicators:
            if indicator in text_lower:
                relationships.append(indicator)
        
        return relationships

    def _calculate_agency_level(self, text: str) -> int:
        """Calculate character agency level (1-10)"""
        text_lower = text.lower()
        agency_score = 5  # Default middle score
        
        # Active verbs increase agency
        active_verbs = ['decides', 'chooses', 'leads', 'creates', 'builds', 'fights', 'runs', 'manages']
        for verb in active_verbs:
            if verb in text_lower:
                agency_score += 1
        
        # Passive indicators decrease agency
        passive_indicators = ['waits for', 'depends on', 'needs permission', 'asks for help']
        for indicator in passive_indicators:
            if indicator in text_lower:
                agency_score -= 1
        
        return max(1, min(10, agency_score))

    def _find_appearance_descriptions(self, text: str) -> List[str]:
        """Find appearance-related descriptions"""
        appearances = []
        text_lower = text.lower()
        
        for word in self.appearance_words:
            if word in text_lower:
                appearances.append(word)
        
        return appearances

    def _count_dialogue(self, name: str, text: str) -> int:
        """Count dialogue lines for character"""
        # Simple heuristic: count lines that start with character name
        lines = text.split('\n')
        dialogue_count = 0
        
        for line in lines:
            if line.strip().upper().startswith(name.upper()):
                dialogue_count += 1
        
        return dialogue_count

    def _estimate_screen_time(self, name: str, text: str) -> float:
        """Estimate relative screen time"""
        # Count mentions as proxy for screen time
        mentions = text.lower().count(name.lower())
        total_words = len(text.split())
        
        return (mentions / max(total_words, 1)) * 100

    def calculate_comprehensive_bias_scores(self, characters: List[Character]) -> BiasScores:
        """Calculate comprehensive bias scores"""
        if not characters:
            return BiasScores(0, 0, 0, 0, 0, 0, 0)
        
        female_chars = [c for c in characters if c.gender == 'female']
        male_chars = [c for c in characters if c.gender == 'male']
        
        # Occupation Gap
        occupation_gap = self._calculate_occupation_gap(female_chars, male_chars)
        
        # Agency Gap
        agency_gap = self._calculate_agency_gap(female_chars, male_chars)
        
        # Appearance Focus
        appearance_focus = self._calculate_appearance_focus(female_chars, male_chars)
        
        # Relationship Defining
        relationship_defining = self._calculate_relationship_defining(female_chars)
        
        # Dialogue Imbalance
        dialogue_imbalance = self._calculate_dialogue_imbalance(female_chars, male_chars)
        
        # Screen Time Imbalance
        screen_time_imbalance = self._calculate_screen_time_imbalance(female_chars, male_chars)
        
        # Overall Score
        overall = np.mean([
            occupation_gap, agency_gap, appearance_focus, 
            relationship_defining, dialogue_imbalance, screen_time_imbalance
        ])
        
        return BiasScores(
            occupation_gap=occupation_gap,
            agency_gap=agency_gap,
            appearance_focus=appearance_focus,
            relationship_defining=relationship_defining,
            dialogue_imbalance=dialogue_imbalance,
            screen_time_imbalance=screen_time_imbalance,
            overall=overall
        )

    def _calculate_occupation_gap(self, female_chars: List[Character], male_chars: List[Character]) -> float:
        """Calculate occupation representation gap"""
        if not female_chars:
            return 0
        
        female_with_prof = sum(1 for c in female_chars if c.professions)
        male_with_prof = sum(1 for c in male_chars if c.professions)
        
        female_prof_rate = female_with_prof / len(female_chars)
        male_prof_rate = male_with_prof / max(len(male_chars), 1)
        
        return max(0, (male_prof_rate - female_prof_rate) * 100)

    def _calculate_agency_gap(self, female_chars: List[Character], male_chars: List[Character]) -> float:
        """Calculate agency level gap"""
        if not female_chars:
            return 0
        
        avg_female_agency = np.mean([c.agency_level for c in female_chars])
        avg_male_agency = np.mean([c.agency_level for c in male_chars]) if male_chars else 5
        
        return max(0, (avg_male_agency - avg_female_agency) * 10)

    def _calculate_appearance_focus(self, female_chars: List[Character], male_chars: List[Character]) -> float:
        """Calculate appearance focus bias"""
        if not female_chars:
            return 0
        
        female_appearance = np.mean([len(c.appearance_descriptions) for c in female_chars])
        male_appearance = np.mean([len(c.appearance_descriptions) for c in male_chars]) if male_chars else 0
        
        return max(0, (female_appearance - male_appearance) * 25)

    def _calculate_relationship_defining(self, female_chars: List[Character]) -> float:
        """Calculate relationship-defining bias"""
        if not female_chars:
            return 0
        
        relationship_focused = sum(1 for c in female_chars 
                                 if c.relationships and not c.professions)
        
        return (relationship_focused / len(female_chars)) * 100

    def _calculate_dialogue_imbalance(self, female_chars: List[Character], male_chars: List[Character]) -> float:
        """Calculate dialogue distribution imbalance"""
        if not female_chars or not male_chars:
            return 0
        
        total_female_dialogue = sum(c.dialogue_count for c in female_chars)
        total_male_dialogue = sum(c.dialogue_count for c in male_chars)
        
        total_dialogue = total_female_dialogue + total_male_dialogue
        if total_dialogue == 0:
            return 0
        
        female_dialogue_ratio = total_female_dialogue / total_dialogue
        expected_ratio = len(female_chars) / (len(female_chars) + len(male_chars))
        
        return max(0, (expected_ratio - female_dialogue_ratio) * 100)

    def _calculate_screen_time_imbalance(self, female_chars: List[Character], male_chars: List[Character]) -> float:
        """Calculate screen time imbalance"""
        if not female_chars or not male_chars:
            return 0
        
        avg_female_screen_time = np.mean([c.screen_time for c in female_chars])
        avg_male_screen_time = np.mean([c.screen_time for c in male_chars])
        
        return max(0, (avg_male_screen_time - avg_female_screen_time) * 2)

    def analyze_movie_script(self, script_text: str, movie_title: str = "Unknown") -> Dict[str, Any]:
        """Complete movie script analysis"""
        characters = self.extract_characters_advanced(script_text)
        bias_scores = self.calculate_comprehensive_bias_scores(characters)
        
        return {
            'movie_title': movie_title,
            'characters': [
                {
                    'name': c.name,
                    'gender': c.gender,
                    'professions': c.professions,
                    'relationships': c.relationships,
                    'agency_level': c.agency_level,
                    'appearance_descriptions': c.appearance_descriptions,
                    'dialogue_count': c.dialogue_count,
                    'screen_time': c.screen_time
                }
                for c in characters
            ],
            'bias_scores': {
                'occupation_gap': bias_scores.occupation_gap,
                'agency_gap': bias_scores.agency_gap,
                'appearance_focus': bias_scores.appearance_focus,
                'relationship_defining': bias_scores.relationship_defining,
                'dialogue_imbalance': bias_scores.dialogue_imbalance,
                'screen_time_imbalance': bias_scores.screen_time_imbalance,
                'overall': bias_scores.overall
            },
            'summary': {
                'total_characters': len(characters),
                'female_characters': len([c for c in characters if c.gender == 'female']),
                'male_characters': len([c for c in characters if c.gender == 'male']),
                'bias_level': 'high' if bias_scores.overall > 60 else 'medium' if bias_scores.overall > 30 else 'low'
            }
        }

# Example usage and testing
if __name__ == "__main__":
    detector = ComprehensiveGenderBiasDetector()
    
    # Test with sample text
    sample_text = """
    Priya Sharma, daughter of businessman Mr. Sharma, is beautiful and waits for her father's decision about her marriage.
    Rohit is an engineer who leads the project team and makes important decisions for the company.
    """
    
    result = detector.analyze_movie_script(sample_text, "Test Movie")
    print(json.dumps(result, indent=2))
