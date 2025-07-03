"""
Step-by-step testing guide with detailed examples
"""

def test_step_1_character_extraction():
    """Step 1: Test character extraction"""
    print("STEP 1: CHARACTER EXTRACTION TEST")
    print("=" * 50)
    
    sample_text = """
    Rohit Mehra is an aspiring singer who works as a salesman. 
    He meets Dr. Priya Sharma when he delivers a car to her clinic. 
    Priya is a cardiologist who runs her own practice. 
    Sonia Saxena, daughter of Mr Saxena, is beautiful and comes from a wealthy family.
    """
    
    print("📝 Input text:")
    print(sample_text.strip())
    
    try:
        from bias_detection_model import ComprehensiveGenderBiasDetector
        detector = ComprehensiveGenderBiasDetector()
        
        characters = detector.extract_characters_advanced(sample_text)
        
        print(f"\n👥 Characters detected: {len(characters)}")
        for char in characters:
            print(f"  • {char.name} ({char.gender})")
            print(f"    - Professions: {len(char.professions)}")
            print(f"    - Relationships: {len(char.relationships)}")
            print(f"    - Dialogue count: {char.dialogue_count}")
            print(f"    - Role type: {char.role_type}")
        
        print("\n✅ Character extraction test completed!")
        return characters
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_step_2_bias_scoring(characters):
    """Step 2: Test bias scoring"""
    print("\n\nSTEP 2: BIAS SCORING TEST")
    print("=" * 50)
    
    if not characters:
        print("❌ No characters to analyze (Step 1 failed)")
        return None
    
    try:
        from bias_detection_model import ComprehensiveGenderBiasDetector
        detector = ComprehensiveGenderBiasDetector()
        
        bias_scores = detector.calculate_comprehensive_bias_scores(characters)
        
        print("📊 Bias Scores:")
        print(f"  • Occupation Gap: {bias_scores.occupation_gap:.1f}/100")
        print(f"  • Agency Gap: {bias_scores.agency_gap:.1f}/100")
        print(f"  • Appearance Focus: {bias_scores.appearance_focus:.1f}/100")
        print(f"  • Relationship Defining: {bias_scores.relationship_defining:.1f}/100")
        print(f"  • Dialogue Imbalance: {bias_scores.dialogue_imbalance:.1f}/100")
        print(f"  • Screen Time Imbalance: {bias_scores.screen_time_imbalance:.1f}/100")
        print(f"  • OVERALL: {bias_scores.overall:.1f}/100")
        
        # Interpret results
        level = "High" if bias_scores.overall > 70 else "Medium" if bias_scores.overall > 40 else "Low"
        print(f"\n🎯 Bias Level: {level}")
        
        print("\n✅ Bias scoring test completed!")
        return bias_scores
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_step_3_rewriting():
    """Step 3: Test rewriting functionality"""
    print("\n\nSTEP 3: REWRITING TEST")
    print("=" * 50)
    
    test_text = "Sonia Saxena, daughter of Mr Saxena, is beautiful and waits for her father's decision."
    bias_types = ['occupation_gap', 'agency_gap', 'appearance_focus', 'relationship_defining']
    
    print("📝 Original text:")
    print(f'"{test_text}"')
    print(f"\n🎯 Bias types to fix: {bias_types}")
    
    try:
        from bias_rewriter import LLMBiasRewriter
        rewriter = LLMBiasRewriter()
        
        # Generate multiple rewrites
        rewrites = rewriter.generate_multiple_rewrites(test_text, bias_types, count=3)
        
        print(f"\n✍️ Generated {len(rewrites)} rewrite options:")
        
        for i, rewrite in enumerate(rewrites):
            print(f"\n--- Option {i+1} ---")
            print(f"Rewritten: \"{rewrite.rewritten_text}\"")
            print(f"Quality Score: {rewrite.quality_score:.1f}/100")
            print(f"Bias Reduction: {rewrite.bias_reduction_score:.1f}%")
            print(f"Improvements: {rewrite.improvements}")
            
            # Quality check
            quality_5_point = (rewrite.quality_score / 100) * 5
            quality_status = "✅ MEETS TARGET" if quality_5_point >= 4.0 else "❌ BELOW TARGET"
            print(f"Quality (5-point): {quality_5_point:.2f}/5 {quality_status}")
        
        print("\n✅ Rewriting test completed!")
        return rewrites
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_step_4_full_movie_analysis():
    """Step 4: Test full movie analysis"""
    print("\n\nSTEP 4: FULL MOVIE ANALYSIS TEST")
    print("=" * 50)
    
    sample_movie = {
        'metadata': {
            'title': 'Test Movie',
            'year': 2023,
            'director': 'Test Director'
        },
        'combined_content': """
        Rohit is an aspiring singer who works as a salesman in a car showroom. 
        One day he meets Sonia Saxena, daughter of Mr Saxena, when he delivers 
        a car to her as a birthday present. Sonia is beautiful and comes from 
        a wealthy family. She waits for her father's decision about marriage. 
        Meanwhile, Dr. Priya works at the local hospital and decides to help 
        Rohit pursue his singing career. Priya leads a team of doctors and 
        creates new treatment protocols.
        """,
        'content_sources': ['script'],
        'total_content_length': 400
    }
    
    print(f"🎬 Analyzing movie: {sample_movie['metadata']['title']}")
    print(f"Content length: {sample_movie['total_content_length']} characters")
    
    try:
        from bias_detection_model import ComprehensiveGenderBiasDetector
        detector = ComprehensiveGenderBiasDetector()
        
        analysis_result = detector.analyze_movie_comprehensive(sample_movie)
        
        if analysis_result:
            print("\n📊 Analysis Results:")
            print(f"  • Total characters: {analysis_result['characters']['total']}")
            print(f"  • Male characters: {analysis_result['characters']['male']}")
            print(f"  • Female characters: {analysis_result['characters']['female']}")
            print(f"  • Overall bias score: {analysis_result['bias_scores']['overall']:.1f}/100")
            print(f"  • Bias examples found: {len(analysis_result['bias_examples'])}")
            
            # Show character details
            print("\n👥 Character Details:")
            for char in analysis_result['characters']['character_details']:
                print(f"  • {char['name']} ({char['gender']})")
                print(f"    - Role: {char['role_type']}")
                print(f"    - Professions: {char['profession_count']}")
                print(f"    - Dialogue: {char['dialogue_count']}")
            
            # Show bias examples
            if analysis_result['bias_examples']:
                print("\n🚨 Bias Examples:")
                for example in analysis_result['bias_examples'][:3]:
                    print(f"  • {example['bias_type']}: {example['character_name']}")
                    print(f"    Issue: \"{example['excerpt']}\"")
                    print(f"    Suggestion: {example['suggestion']}")
            
            print("\n✅ Full movie analysis test completed!")
            return analysis_result
        else:
            print("❌ Analysis failed - no results returned")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_step_5_report_generation(analysis_result):
    """Step 5: Test report generation"""
    print("\n\nSTEP 5: REPORT GENERATION TEST")
    print("=" * 50)
    
    if not analysis_result:
        print("❌ No analysis result to generate report (Step 4 failed)")
        return
    
    try:
        from report_generator import ComprehensiveBiasReportGenerator
        report_gen = ComprehensiveBiasReportGenerator()
        
        print("📊 Generating reports...")
        
        # Generate PDF report
        try:
            pdf_path = report_gen.generate_movie_report(analysis_result)
            print(f"✅ PDF Report: {pdf_path}")
        except Exception as e:
            print(f"⚠️ PDF generation failed: {e}")
        
        # Generate HTML report
        try:
            html_path = report_gen.generate_html_report(analysis_result)
            print(f"✅ HTML Report: {html_path}")
        except Exception as e:
            print(f"⚠️ HTML generation failed: {e}")
        
        print("\n✅ Report generation test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def run_step_by_step_test():
    """Run complete step-by-step test"""
    print("🧪 BOLLYWOOD BIAS BUSTER - STEP-BY-STEP TEST")
    print("=" * 60)
    
    # Step 1: Character extraction
    characters = test_step_1_character_extraction()
    
    # Step 2: Bias scoring
    bias_scores = test_step_2_bias_scoring(characters)
    
    # Step 3: Rewriting
    rewrites = test_step_3_rewriting()
    
    # Step 4: Full movie analysis
    analysis_result = test_step_4_full_movie_analysis()
    
    # Step 5: Report generation
    test_step_5_report_generation(analysis_result)
    
    print("\n" + "=" * 60)
    print("🎯 STEP-BY-STEP TEST COMPLETED")
    print("=" * 60)
    print("Check above for ✅ (success) and ❌ (error) indicators.")
    print("If most steps show ✅, your system is working correctly!")

if __name__ == "__main__":
    run_step_by_step_test()
