"""
Expected results for validation - use these to check if your system is working correctly
"""

EXPECTED_RESULTS = {
    
    # Expected results for DDLJ analysis
    'ddlj_expected': {
        'characters': {
            'total': 4,  # Raj, Simran, Dharamvir, Baldev
            'male': 2,   # Raj, Dharamvir, Baldev
            'female': 2, # Simran, Lajwanti
            'expected_names': ['Raj', 'Simran', 'Dharamvir', 'Baldev', 'Lajwanti']
        },
        'bias_scores': {
            'occupation_gap': 60-80,      # High - Simran has no profession
            'agency_gap': 70-90,          # High - Simran waits and follows
            'appearance_focus': 40-60,    # Medium - Simran described as beautiful
            'relationship_defining': 80-95, # High - Simran defined by family
            'overall': 60-80              # High overall bias
        },
        'bias_examples_count': 3-5
    },
    
    # Expected results for Queen analysis
    'queen_expected': {
        'characters': {
            'total': 3,  # Rani, Vijay, Vijayalakshmi
            'male': 1,   # Vijay
            'female': 2, # Rani, Vijayalakshmi
            'expected_names': ['Rani', 'Vijay', 'Vijayalakshmi']
        },
        'bias_scores': {
            'occupation_gap': 20-40,      # Low-Medium - Rani works, starts business
            'agency_gap': 10-30,          # Low - Rani makes decisions, becomes independent
            'appearance_focus': 10-30,    # Low - Focus on character growth
            'relationship_defining': 30-50, # Medium - Initially defined by engagement
            'overall': 20-40              # Low-Medium overall bias
        },
        'bias_examples_count': 1-3
    },
    
    # Expected results for Dangal analysis
    'dangal_expected': {
        'characters': {
            'total': 4,  # Mahavir, Geeta, Babita, Pramod
            'male': 2,   # Mahavir, Pramod
            'female': 2, # Geeta, Babita
            'expected_names': ['Mahavir', 'Geeta', 'Babita', 'Pramod']
        },
        'bias_scores': {
            'occupation_gap': 10-30,      # Low - Both daughters are professional wrestlers
            'agency_gap': 20-40,          # Low-Medium - Daughters make career decisions
            'appearance_focus': 5-20,     # Very Low - Focus on athletic ability
            'relationship_defining': 15-35, # Low - Defined by sport, not just family
            'overall': 15-35              # Low overall bias
        },
        'bias_examples_count': 0-2
    },
    
    # Expected rewrite results
    'rewrite_expected': {
        'original': "Sonia Saxena, daughter of Mr Saxena, is beautiful and waits for her father's decision.",
        'expected_improvements': [
            'Add professional identity',
            'Increase character agency', 
            'Reduce appearance focus',
            'Add independent identity'
        ],
        'quality_score_range': (70, 95),  # Should be 70-95/100
        'bias_reduction_range': (60, 90), # Should reduce bias by 60-90%
        'expected_rewrite_elements': [
            'profession mentioned',
            'active verb instead of "waits"',
            'trait instead of "beautiful"',
            'independence alongside relationship'
        ]
    },
    
    # Performance benchmarks
    'performance_benchmarks': {
        'f1_score_target': 0.85,
        'quality_score_target': 4.0,  # out of 5
        'character_detection_accuracy': 0.80,
        'gender_detection_accuracy': 0.85,
        'processing_time_per_movie': 30,  # seconds
        'bias_detection_confidence': 0.75
    },
    
    # Test validation criteria
    'validation_criteria': {
        'character_extraction': {
            'min_characters_detected': 2,
            'gender_detection_rate': 0.8,
            'profession_detection_rate': 0.7
        },
        'bias_scoring': {
            'score_range': (0, 100),
            'consistency_threshold': 0.1,  # Scores should be consistent within 10%
            'category_coverage': 6  # All 6 bias categories should be scored
        },
        'rewriting': {
            'min_quality_score': 60,
            'min_bias_reduction': 40,
            'text_length_ratio': (0.8, 1.5),  # Rewritten text should be 80-150% of original
            'name_preservation_rate': 0.9
        },
        'reporting': {
            'pdf_generation_success': True,
            'html_generation_success': True,
            'report_completeness': 0.9  # 90% of expected sections present
        }
    }
}

def validate_results(actual_results, expected_key):
    """Validate actual results against expected results"""
    expected = EXPECTED_RESULTS.get(expected_key, {})
    validation_report = {
        'passed': [],
        'failed': [],
        'warnings': []
    }
    
    # Add validation logic here based on the expected results
    # This is a framework for validation - implement specific checks as needed
    
    return validation_report

def print_expected_results():
    """Print expected results for reference"""
    print("📋 EXPECTED RESULTS REFERENCE")
    print("=" * 50)
    
    for key, expected in EXPECTED_RESULTS.items():
        print(f"\n🎯 {key.upper()}:")
        if isinstance(expected, dict):
            for subkey, value in expected.items():
                print(f"  • {subkey}: {value}")
        else:
            print(f"  • {expected}")

if __name__ == "__main__":
    print_expected_results()
