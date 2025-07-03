import re
import random
from typing import Dict, List, Tuple, Any, Optional
import openai
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class RewriteResult:
    """Result of bias-free rewriting"""
    original_text: str
    rewritten_text: str
    quality_score: float
    bias_reduction: float
    improvements: List[str]
    rewrite_type: str

class LLMBiasRewriter:
    """
    LLM-based bias-free rewriter with quality >= 4/5 target
    """
    
    def __init__(self, api_key: str = None):
        if api_key:
            openai.api_key = api_key
        
        # Professional titles and roles
        self.professional_titles = [
            'doctor', 'engineer', 'lawyer', 'teacher', 'scientist', 'researcher',
            'manager', 'director', 'consultant', 'entrepreneur', 'artist',
            'writer', 'journalist', 'designer', 'architect', 'analyst'
        ]
        
        # Appearance-focused words to replace
        self.appearance_replacements = {
            'beautiful': ['accomplished', 'talented', 'skilled', 'intelligent'],
            'pretty': ['capable', 'competent', 'experienced', 'knowledgeable'],
            'gorgeous': ['brilliant', 'innovative', 'creative', 'successful'],
            'stunning': ['impressive', 'remarkable', 'outstanding', 'exceptional'],
            'attractive': ['engaging', 'compelling', 'influential', 'respected'],
            'handsome': ['professional', 'accomplished', 'skilled', 'experienced'],
            'good-looking': ['well-regarded', 'respected', 'competent', 'capable']
        }
        
        # Agency-enhancing replacements
        self.agency_replacements = {
            'waits for': ['actively seeks', 'pursues', 'works towards', 'strives for'],
            'hopes for': ['works towards', 'actively pursues', 'strives to achieve'],
            'wishes for': ['actively seeks', 'works to obtain', 'pursues'],
            'dreams of': ['works towards', 'actively pursues', 'strives for'],
            'receives': ['earns', 'achieves', 'obtains', 'secures'],
            'is given': ['earns', 'achieves', 'secures', 'obtains'],
            'gets': ['earns', 'achieves', 'secures', 'obtains']
        }
        
        # Relationship-defining patterns to modify
        self.relationship_patterns = [
            (r'(\w+),?\s+daughter of ([^,]+)', r'\1, a professional and daughter of \2'),
            (r'(\w+),?\s+wife of ([^,]+)', r'\1, an accomplished professional and wife of \2'),
            (r'(\w+),?\s+sister of ([^,]+)', r'\1, an independent professional and sister of \2'),
            (r'(\w+)\s+belongs to', r'\1, a successful professional, belongs to')
        ]
        
        # Professional context additions
        self.profession_additions = [
            'a skilled professional',
            'an accomplished expert',
            'a talented specialist',
            'an experienced professional',
            'a successful entrepreneur',
            'a dedicated professional'
        ]
        
        # Rewriting templates and patterns
        self.rewrite_patterns = {
            'occupation_gap': {
                'patterns': [
                    (r'([A-Z][a-z]+),?\s+daughter of ([^,]+)', r'\1, a professional and daughter of \2'),
                    (r'([A-Z][a-z]+),?\s+wife of ([^,]+)', r'\1, a working professional and wife of \2'),
                    (r'([A-Z][a-z]+),?\s+sister of ([^,]+)', r'\1, a career woman and sister of \2'),
                    (r'([A-Z][a-z]+) belongs to ([^.]+)', r'\1 works professionally and belongs to \2'),
                ],
                'profession_additions': [
                    'doctor', 'engineer', 'teacher', 'lawyer', 'businesswoman',
                    'artist', 'writer', 'scientist', 'manager', 'consultant',
                    'designer', 'architect', 'journalist', 'researcher', 'entrepreneur'
                ]
            },
            'agency_gap': {
                'passive_to_active': [
                    (r'([A-Z][a-z]+) receives ([^.]+)', r'\1 chooses to accept \2'),
                    (r'([A-Z][a-z]+) waits for ([^.]+)', r'\1 actively seeks \2'),
                    (r'([A-Z][a-z]+) hopes for ([^.]+)', r'\1 works towards \2'),
                    (r'([A-Z][a-z]+) follows ([^.]+)', r'\1 collaborates with \2'),
                    (r'([A-Z][a-z]+) accepts ([^.]+)', r'\1 decides to embrace \2'),
                ],
                'agency_verbs': [
                    'decides', 'chooses', 'leads', 'creates', 'initiates',
                    'establishes', 'develops', 'manages', 'directs', 'controls'
                ]
            },
            'appearance_focus': {
                'appearance_to_trait': [
                    (r'beautiful ([A-Z][a-z]+)', r'intelligent \1'),
                    (r'pretty ([A-Z][a-z]+)', r'talented \1'),
                    (r'gorgeous ([A-Z][a-z]+)', r'skilled \1'),
                    (r'stunning ([A-Z][a-z]+)', r'accomplished \1'),
                    (r'attractive ([A-Z][a-z]+)', r'capable \1'),
                ],
                'trait_adjectives': [
                    'intelligent', 'talented', 'skilled', 'accomplished', 'capable',
                    'determined', 'creative', 'innovative', 'dedicated', 'ambitious'
                ]
            },
            'relationship_defining': {
                'add_independence': [
                    (r'([A-Z][a-z]+),?\s+daughter of ([^,]+)', r'\1, an independent woman and daughter of \2'),
                    (r'([A-Z][a-z]+),?\s+wife of ([^,]+)', r'\1, a self-reliant individual and wife of \2'),
                    (r'([A-Z][a-z]+) belongs to ([^.]+)', r'\1 has her own identity and belongs to \2'),
                ]
            }
        }
        
        # New profession alternatives for LLM-based approach
        self.profession_alternatives = {
            'daughter': ['scientist', 'engineer', 'doctor', 'teacher', 'artist', 'writer'],
            'wife': ['professional', 'colleague', 'partner'],
            'girlfriend': ['partner', 'colleague', 'friend']
        }
        
        # New active verbs for LLM-based approach
        self.active_verbs = {
            'waits for': 'actively seeks',
            'hopes for': 'works towards',
            'depends on': 'collaborates with',
            'needs permission': 'makes decisions about',
            'asks for': 'discusses'
        }
        
        # New appearance alternatives for LLM-based approach
        self.appearance_alternatives = {
            'beautiful': 'intelligent',
            'pretty': 'capable',
            'gorgeous': 'accomplished',
            'stunning': 'skilled'
        }
    
    def rewrite_text_rule_based(self, text: str, bias_types: List[str]) -> RewriteResult:
        """Rule-based rewriting for specific bias types"""
        original_text = text
        rewritten_text = text
        improvements = []
        preserved_elements = []
        suggestions = []
        
        # Track original elements to preserve
        original_names = re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', text)
        preserved_elements.extend([f"Character name: {name}" for name in original_names[:3]])
        
        # Apply rewriting patterns based on detected bias types
        for bias_type in bias_types:
            if bias_type in self.rewrite_patterns:
                patterns = self.rewrite_patterns[bias_type]
                
                if bias_type == 'occupation_gap':
                    # Apply occupation gap fixes
                    for pattern, replacement in patterns['patterns']:
                        if re.search(pattern, rewritten_text):
                            rewritten_text = re.sub(pattern, replacement, rewritten_text)
                            improvements.append(f"Added professional identity to character introduction")
                    
                    # Add random profession if no profession mentioned
                    if not any(prof in rewritten_text.lower() for prof in ['doctor', 'engineer', 'teacher', 'lawyer']):
                        profession = random.choice(patterns['profession_additions'])
                        # Find first female character and add profession
                        female_pattern = r'([A-Z][a-z]+)(?=.*\b(?:she|her|daughter|wife|sister)\b)'
                        match = re.search(female_pattern, rewritten_text)
                        if match:
                            name = match.group(1)
                            rewritten_text = rewritten_text.replace(
                                name, f"{name}, a {profession},", 1
                            )
                            improvements.append(f"Added profession ({profession}) to female character")
                
                elif bias_type == 'agency_gap':
                    # Apply agency gap fixes
                    for pattern, replacement in patterns['passive_to_active']:
                        if re.search(pattern, rewritten_text):
                            rewritten_text = re.sub(pattern, replacement, rewritten_text)
                            improvements.append("Converted passive action to active agency")
                
                elif bias_type == 'appearance_focus':
                    # Apply appearance focus fixes
                    for pattern, replacement in patterns['appearance_to_trait']:
                        if re.search(pattern, rewritten_text):
                            rewritten_text = re.sub(pattern, replacement, rewritten_text)
                            improvements.append("Replaced appearance description with character trait")
                
                elif bias_type == 'relationship_defining':
                    # Apply relationship defining fixes
                    for pattern, replacement in patterns['add_independence']:
                        if re.search(pattern, rewritten_text):
                            rewritten_text = re.sub(pattern, replacement, rewritten_text)
                            improvements.append("Added independent identity alongside relationship")
        
        # Address appearance focus bias
        if 'appearance_focus' in bias_types:
            rewritten_text, app_improvements = self._reduce_appearance_focus(rewritten_text)
            improvements.extend(app_improvements)
        
        # Address agency gap bias
        if 'agency_gap' in bias_types:
            rewritten_text, agency_improvements = self._increase_agency(rewritten_text)
            improvements.extend(agency_improvements)
        
        # Address occupation gap bias
        if 'occupation_gap' in bias_types:
            rewritten_text, occ_improvements = self._add_professional_identity(rewritten_text)
            improvements.extend(occ_improvements)
        
        # Address relationship defining bias
        if 'relationship_defining' in bias_types:
            rewritten_text, rel_improvements = self._reduce_relationship_dependency(rewritten_text)
            improvements.extend(rel_improvements)
        
        # Calculate quality and bias reduction scores
        quality_score = self._calculate_quality_score(original_text, rewritten_text, improvements)
        bias_reduction_score = self._calculate_bias_reduction(original_text, rewritten_text, bias_types)
        
        # Generate suggestions for further improvement
        suggestions = self._generate_suggestions(rewritten_text, bias_types)
        
        return RewriteResult(
            original_text=original_text,
            rewritten_text=rewritten_text,
            quality_score=quality_score,
            bias_reduction=bias_reduction_score,
            improvements=improvements,
            rewrite_type="rule_based"
        )
    
    def rewrite_text_llm(self, text: str, bias_types: List[str]) -> RewriteResult:
        """LLM-based rewriting using OpenAI API"""
        
        # Create bias-specific prompt
        bias_descriptions = {
            'occupation_gap': "female characters lack professional identity",
            'agency_gap': "female characters are passive rather than active",
            'appearance_focus': "female characters are described primarily by appearance",
            'relationship_defining': "female characters are defined only by relationships"
        }
        
        detected_biases = [bias_descriptions.get(bias, bias) for bias in bias_types]
        bias_list = ", ".join(detected_biases)
        
        prompt = f"""
        Rewrite the following text to eliminate gender bias while preserving the narrative flow and character relationships.
        
        Detected biases: {bias_list}
        
        Guidelines:
        1. Give female characters professional identities alongside family relationships
        2. Show female characters taking active decisions and actions
        3. Balance appearance descriptions with character traits and achievements
        4. Maintain all character names and core plot elements
        5. Keep the same tone and style
        
        Original text: "{text}"
        
        Rewritten text:
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert script writer specializing in gender-inclusive content."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            rewritten_text = response.choices[0].message.content.strip()
            
            # Analyze improvements
            improvements = self._analyze_llm_improvements(text, rewritten_text, bias_types)
            preserved_elements = self._identify_preserved_elements(text, rewritten_text)
            
            # Calculate scores
            bias_reduction_score = self._calculate_bias_reduction(text, rewritten_text, bias_types)
            quality_score = self._calculate_quality_score(text, rewritten_text, improvements)
            
            # Generate suggestions for further improvement
            suggestions = self._generate_suggestions(rewritten_text, bias_types)
            
            return RewriteResult(
                original_text=text,
                rewritten_text=rewritten_text,
                quality_score=quality_score,
                bias_reduction=bias_reduction_score,
                improvements=improvements,
                rewrite_type="llm_based"
            )
            
        except Exception as e:
            # Fallback to rule-based rewriting
            logger.error(f"LLM rewriting failed: {e}. Using rule-based approach.")
            return self.rewrite_text_rule_based(text, bias_types)
    
    def generate_multiple_rewrites(self, text: str, bias_types: List[str], count: int = 3) -> List[RewriteResult]:
        """Generate multiple rewrite options"""
        rewrites = []
        
        # Generate rule-based rewrite
        rule_based = self.rewrite_text_rule_based(text, bias_types)
        rewrites.append(rule_based)
        
        # Generate LLM-based rewrites with different approaches
        for i in range(count - 1):
            try:
                llm_rewrite = self.rewrite_text_llm(text, bias_types)
                rewrites.append(llm_rewrite)
            except:
                # Generate variations of rule-based approach
                variation = self._create_rule_based_variation(text, bias_types, i)
                rewrites.append(variation)
        
        # Sort by quality score
        rewrites.sort(key=lambda x: x.quality_score, reverse=True)
        
        return rewrites
    
    def rewrite_multiple_alternatives(self, text: str, bias_types: List[str], num_alternatives: int = 3) -> List[RewriteResult]:
        """Generate multiple rewrite alternatives"""
        alternatives = []
        
        for i in range(num_alternatives):
            # Vary the randomness for different alternatives
            random.seed(i)
            result = self.rewrite_text_rule_based(text, bias_types)
            alternatives.append(result)
        
        # Sort by quality score
        alternatives.sort(key=lambda x: x.quality_score, reverse=True)
        
        return alternatives
    
    def batch_rewrite(self, texts: List[str], bias_types: List[str]) -> List[RewriteResult]:
        """Batch rewrite multiple texts"""
        results = []
        
        for text in texts:
            result = self.rewrite_text_rule_based(text, bias_types)
            results.append(result)
        
        return results
    
    def _calculate_bias_reduction(self, original: str, rewritten: str, bias_types: List[str]) -> float:
        """Calculate bias reduction score"""
        
        # Count bias indicators in original vs rewritten
        bias_indicators = {
            'relationship_only': [r'daughter of', r'wife of', r'sister of', r'belongs to'],
            'passive_verbs': [r'receives', r'waits', r'hopes', r'follows', r'accepts'],
            'appearance_focus': [r'beautiful', r'pretty', r'gorgeous', r'stunning', r'attractive'],
            'no_profession': True  # Special case
        }
        
        original_bias_count = 0
        rewritten_bias_count = 0
        
        for bias_type, patterns in bias_indicators.items():
            if bias_type == 'no_profession':
                continue
                
            for pattern in patterns:
                original_bias_count += len(re.findall(pattern, original, re.IGNORECASE))
                rewritten_bias_count += len(re.findall(pattern, rewritten, re.IGNORECASE))
        
        # Check for profession additions
        profession_words = ['doctor', 'engineer', 'teacher', 'lawyer', 'professional', 'works', 'career']
        original_professions = sum(1 for word in profession_words if word in original.lower())
        rewritten_professions = sum(1 for word in profession_words if word in rewritten.lower())
        
        # Calculate reduction percentage
        if original_bias_count == 0:
            return 50.0  # Baseline if no bias detected
        
        bias_reduction = max(0, (original_bias_count - rewritten_bias_count) / original_bias_count * 100)
        profession_improvement = min(30, (rewritten_professions - original_professions) * 10)
        
        total_score = min(100, bias_reduction + profession_improvement)
        return total_score
    
    def _calculate_quality_score(self, original: str, rewritten: str, improvements: List[str]) -> float:
        """Calculate quality score (target >= 4/5 = 80%)"""
        
        quality_factors = {
            'length_preservation': 0,
            'name_preservation': 0,
            'narrative_flow': 0,
            'improvement_count': 0,
            'readability': 0
        }
        
        # Length preservation (should be similar length)
        length_ratio = len(rewritten) / len(original) if len(original) > 0 else 1
        if 0.8 <= length_ratio <= 1.5:
            quality_factors['length_preservation'] = 20
        elif 0.6 <= length_ratio <= 2.0:
            quality_factors['length_preservation'] = 10
        
        # Name preservation
        original_names = set(re.findall(r'[A-Z][a-z]+', original))
        rewritten_names = set(re.findall(r'[A-Z][a-z]+', rewritten))
        name_preservation_ratio = len(original_names.intersection(rewritten_names)) / len(original_names) if original_names else 1
        quality_factors['name_preservation'] = name_preservation_ratio * 20
        
        # Narrative flow (basic check for sentence structure)
        original_sentences = len(re.findall(r'[.!?]+', original))
        rewritten_sentences = len(re.findall(r'[.!?]+', rewritten))
        if abs(original_sentences - rewritten_sentences) <= 2:
            quality_factors['narrative_flow'] = 20
        elif abs(original_sentences - rewritten_sentences) <= 4:
            quality_factors['narrative_flow'] = 10
        
        # Improvement count
        quality_factors['improvement_count'] = min(20, len(improvements) * 5)
        
        # Readability (basic check)
        if rewritten and not re.search(r'[^\w\s.,!?;:-]', rewritten):
            quality_factors['readability'] = 20
        
        total_quality = sum(quality_factors.values())
        return total_quality  # Out of 100, convert to 5-point scale: total_quality / 20
    
    def _analyze_llm_improvements(self, original: str, rewritten: str, bias_types: List[str]) -> List[str]:
        """Analyze what improvements the LLM made"""
        improvements = []
        
        # Check for profession additions
        profession_words = ['doctor', 'engineer', 'teacher', 'lawyer', 'professional', 'works', 'career']
        original_professions = sum(1 for word in profession_words if word in original.lower())
        rewritten_professions = sum(1 for word in profession_words if word in rewritten.lower())
        
        if rewritten_professions > original_professions:
            improvements.append("Added professional identity to characters")
        
        # Check for agency improvements
        passive_words = ['receives', 'waits', 'hopes', 'follows', 'accepts']
        active_words = ['decides', 'chooses', 'leads', 'creates', 'initiates']
        
        original_passive = sum(1 for word in passive_words if word in original.lower())
        rewritten_passive = sum(1 for word in passive_words if word in rewritten.lower())
        original_active = sum(1 for word in active_words if word in original.lower())
        rewritten_active = sum(1 for word in active_words if word in rewritten.lower())
        
        if rewritten_active > original_active or rewritten_passive < original_passive:
            improvements.append("Improved character agency and active voice")
        
        # Check for appearance focus reduction
        appearance_words = ['beautiful', 'pretty', 'gorgeous', 'stunning', 'attractive']
        original_appearance = sum(1 for word in appearance_words if word in original.lower())
        rewritten_appearance = sum(1 for word in appearance_words if word in rewritten.lower())
        
        if rewritten_appearance < original_appearance:
            improvements.append("Reduced focus on physical appearance")
        
        # Check for relationship independence
        relationship_words = ['daughter of', 'wife of', 'sister of', 'belongs to']
        independence_words = ['independent', 'professional', 'career', 'self-reliant']
        
        rewritten_independence = sum(1 for word in independence_words if word in rewritten.lower())
        original_independence = sum(1 for word in independence_words if word in original.lower())
        
        if rewritten_independence > original_independence:
            improvements.append("Added independent identity alongside relationships")
        
        return improvements
    
    def _identify_preserved_elements(self, original: str, rewritten: str) -> List[str]:
        """Identify what elements were preserved in the rewrite"""
        preserved = []
        
        # Character names
        original_names = set(re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', original))
        rewritten_names = set(re.findall(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', rewritten))
        preserved_names = original_names.intersection(rewritten_names)
        
        for name in preserved_names:
            preserved.append(f"Character name: {name}")
        
        # Key plot elements (basic keyword matching)
        plot_keywords = ['meets', 'delivers', 'birthday', 'present', 'car', 'showroom', 'family']
        for keyword in plot_keywords:
            if keyword in original.lower() and keyword in rewritten.lower():
                preserved.append(f"Plot element: {keyword}")
        
        # Narrative structure
        if len(re.findall(r'[.!?]', original)) == len(re.findall(r'[.!?]', rewritten)):
            preserved.append("Sentence structure and flow")
        
        return preserved[:5]  # Limit to top 5 preserved elements
    
    def _create_rule_based_variation(self, text: str, bias_types: List[str], variation_index: int) -> RewriteResult:
        """Create variations of rule-based rewriting"""
        
        # Different profession sets for variations
        profession_sets = [
            ['doctor', 'engineer', 'teacher', 'lawyer', 'businesswoman'],
            ['artist', 'writer', 'scientist', 'manager', 'consultant'],
            ['designer', 'architect', 'journalist', 'researcher', 'entrepreneur']
        ]
        
        # Modify the profession list for this variation
        if variation_index < len(profession_sets):
            self.rewrite_patterns['occupation_gap']['profession_additions'] = profession_sets[variation_index]
        
        # Apply different intensity of changes
        result = self.rewrite_text_rule_based(text, bias_types)
        
        # Adjust quality score based on variation
        result.quality_score = max(60, result.quality_score - (variation_index * 5))
        
        return result
    
    def _reduce_appearance_focus(self, text: str) -> Tuple[str, List[str]]:
        """Reduce appearance-focused descriptions"""
        improvements = []
        
        for appearance_word, replacements in self.appearance_replacements.items():
            if appearance_word in text.lower():
                replacement = random.choice(replacements)
                # Case-sensitive replacement
                pattern = re.compile(re.escape(appearance_word), re.IGNORECASE)
                text = pattern.sub(replacement, text, count=1)
                improvements.append(f'Replaced appearance-focused "{appearance_word}" with "{replacement}"')
        
        return text, improvements
    
    def _increase_agency(self, text: str) -> Tuple[str, List[str]]:
        """Increase character agency"""
        improvements = []
        
        for passive_phrase, active_replacements in self.agency_replacements.items():
            if passive_phrase in text.lower():
                replacement = random.choice(active_replacements)
                # Case-sensitive replacement
                pattern = re.compile(re.escape(passive_phrase), re.IGNORECASE)
                text = pattern.sub(replacement, text, count=1)
                improvements.append(f'Converted passive action to active agency')
        
        return text, improvements
    
    def _add_professional_identity(self, text: str) -> Tuple[str, List[str]]:
        """Add professional identity to characters"""
        improvements = []
        
        # Look for female names without professional context
        female_indicators = ['she', 'her', 'daughter', 'wife', 'sister', 'mother']
        has_female_context = any(indicator in text.lower() for indicator in female_indicators)
        
        if has_female_context and not any(prof in text.lower() for prof in self.professional_titles):
            # Add professional context
            profession = random.choice(self.profession_additions)
            
            # Find insertion point (after name, before description)
            name_match = re.search(r'\b([A-Z][a-z]+)\b', text)
            if name_match:
                name = name_match.group(1)
                # Insert profession after name
                text = text.replace(name, f'{name}, {profession}', 1)
                improvements.append(f'Added professional identity to character introduction')
        
        # Specific profession additions
        if 'daughter of' in text.lower() and 'professional' not in text.lower():
            text = re.sub(r'(\w+),?\s+daughter of', r'\1, a scientist, daughter of', text, count=1)
            improvements.append('Added profession (scientist) to female character')
        
        return text, improvements
    
    def _reduce_relationship_dependency(self, text: str) -> Tuple[str, List[str]]:
        """Reduce relationship-dependent character definitions"""
        improvements = []
        
        for pattern, replacement in self.relationship_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                text = re.sub(pattern, replacement, text, count=1, flags=re.IGNORECASE)
                improvements.append('Added independent identity alongside family relationship')
        
        return text, improvements
    
    def _generate_suggestions(self, text: str, bias_types: List[str]) -> List[str]:
        """Generate suggestions for further improvement"""
        suggestions = []
        
        if 'occupation_gap' in bias_types:
            suggestions.append("Consider adding specific career achievements or professional goals")
        
        if 'agency_gap' in bias_types:
            suggestions.append("Show character making independent decisions and taking initiative")
        
        if 'appearance_focus' in bias_types:
            suggestions.append("Focus more on character's skills, personality, and achievements")
        
        if 'relationship_defining' in bias_types:
            suggestions.append("Develop character's individual identity beyond family relationships")
        
        # General suggestions
        suggestions.append("Ensure equal dialogue and screen time for all genders")
        suggestions.append("Include diverse professional backgrounds for all characters")
        
        return suggestions

# Example usage
if __name__ == "__main__":
    rewriter = LLMBiasRewriter()
    
    test_text = "Priya, daughter of Mr. Sharma, is beautiful and waits for her father's decision."
    bias_types = ['occupation_gap', 'agency_gap', 'appearance_focus']
    
    # Single rewrite
    result = rewriter.rewrite_text_rule_based(test_text, bias_types)
    print(f"Original: {result.original_text}")
    print(f"Rewritten: {result.rewritten_text}")
    print(f"Quality: {result.quality_score}/100")
    print(f"Bias Reduction: {result.bias_reduction}%")
    
    # Multiple alternatives
    alternatives = rewriter.generate_multiple_rewrites(test_text, bias_types, 3)
    print(f"\nGenerated {len(alternatives)} alternatives:")
    for i, alt in enumerate(alternatives, 1):
        print(f"{i}. {alt.rewritten_text} (Quality: {alt.quality_score:.1f})")
