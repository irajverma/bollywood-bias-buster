"""
Sample inputs for testing the Bollywood Bias Buster system
"""

# Sample movie data for testing
SAMPLE_MOVIES = [
    {
        'metadata': {
            'title': 'Dilwale Dulhania Le Jayenge',
            'year': 1995,
            'director': 'Aditya Chopra',
            'genre': 'Romance',
            'imdb_id': 'tt0112870'
        },
        'combined_content': """
        Raj Malhotra is a young man living in London with his father. He is carefree and enjoys life.
        Simran Singh is the daughter of Baldev Singh, a strict Punjabi father. Simran is beautiful and obedient.
        Raj meets Simran during a trip to Europe. Raj is charming and pursues Simran actively.
        Simran, though attracted to Raj, waits for her father's approval for marriage.
        Baldev Singh decides that Simran will marry his friend's son in Punjab.
        Raj follows Simran to India and works to win over her family.
        Simran's mother, Lajjo, supports her daughter but cannot oppose her husband.
        Raj proves his worth through various actions and eventually wins Baldev's respect.
        In the end, Baldev allows Simran to choose her own husband.
        """,
        'content_sources': ['plot_summary', 'character_descriptions'],
        'total_content_length': 756
    },
    {
        'metadata': {
            'title': 'Queen',
            'year': 2013,
            'director': 'Vikas Bahl',
            'genre': 'Comedy-Drama',
            'imdb_id': 'tt3322420'
        },
        'combined_content': """
        Rani Mehra is a shy Delhi girl whose wedding is called off by her fiancé Vijay.
        Rani decides to go on her honeymoon alone to Paris and Amsterdam.
        Vijay is a businessman who breaks up with Rani because she doesn't fit his modern lifestyle.
        In Paris, Rani meets Vijayalakshmi, a free-spirited French-Indian woman who becomes her friend.
        Rani discovers her independence and learns to make her own decisions.
        She meets various people who help her grow as a person.
        Rani transforms from a dependent girl to a confident woman.
        When Vijay realizes his mistake and wants her back, Rani chooses her newfound independence.
        Rani's grandmother supports her throughout her journey.
        The story shows Rani's evolution from a traditional girl to an empowered woman.
        """,
        'content_sources': ['plot_summary', 'character_descriptions'],
        'total_content_length': 823
    },
    {
        'metadata': {
            'title': 'Dangal',
            'year': 2016,
            'director': 'Nitesh Tiwari',
            'genre': 'Sports Drama',
            'imdb_id': 'tt5074352'
        },
        'combined_content': """
        Mahavir Singh Phogat is a former wrestler who dreams of winning a gold medal for India.
        Geeta Phogat and Babita Phogat are his daughters who he trains to become wrestlers.
        Mahavir decides to train his daughters when he realizes they have fighting potential.
        Geeta becomes the first Indian female wrestler to qualify for the Olympics.
        Babita also becomes a successful wrestler following her sister's path.
        Their mother, Daya Kaur, initially opposes the training but later supports her daughters.
        Geeta faces challenges at the national academy where coaches try to change her technique.
        Mahavir fights against societal norms to train his daughters in a male-dominated sport.
        Both daughters achieve international success in wrestling competitions.
        The story celebrates female empowerment in sports and breaking gender barriers.
        """,
        'content_sources': ['plot_summary', 'character_descriptions'],
        'total_content_length': 891
    }
]

# Test cases for bias detection
BIAS_TEST_CASES = [
    {
        'text': "Priya Sharma, daughter of businessman Mr. Sharma, is beautiful and waits for her father's decision about her marriage.",
        'expected_bias_level': 'high',
        'expected_biases': ['occupation_gap', 'relationship_defining', 'appearance_focus', 'agency_gap']
    },
    {
        'text': "Gorgeous Meera belongs to a wealthy family and hopes her husband will allow her to work.",
        'expected_bias_level': 'high',
        'expected_biases': ['appearance_focus', 'agency_gap', 'relationship_defining']
    },
    {
        'text': "Rohit is an engineer who leads the project. Sonia, his girlfriend, is pretty and supports him.",
        'expected_bias_level': 'medium',
        'expected_biases': ['occupation_gap', 'agency_gap', 'appearance_focus']
    },
    {
        'text': "Dr. Kavya Sharma runs her own hospital. She makes important medical decisions daily.",
        'expected_bias_level': 'low',
        'expected_biases': []
    },
    {
        'text': "Arjun and Priya are both software engineers. They collaborate on building innovative solutions.",
        'expected_bias_level': 'low',
        'expected_biases': []
    }
]

# Test cases for rewriting
REWRITE_TEST_CASES = [
    {
        'original': "Sonia Saxena, daughter of Mr Saxena, is beautiful and comes from a wealthy family.",
        'bias_types': ['occupation_gap', 'appearance_focus', 'relationship_defining'],
        'expected_improvements': ['professional_identity', 'reduced_appearance_focus']
    },
    {
        'original': "Pretty Meera waits for her father's decision about her career.",
        'bias_types': ['agency_gap', 'appearance_focus'],
        'expected_improvements': ['increased_agency', 'reduced_appearance_focus']
    },
    {
        'original': "Handsome Raj is a doctor. His wife Priya is gorgeous and takes care of the house.",
        'bias_types': ['occupation_gap', 'appearance_focus'],
        'expected_improvements': ['professional_identity_for_female', 'balanced_descriptions']
    }
]

# Expected character extraction results
EXPECTED_CHARACTER_RESULTS = {
    'test_case_1': {
        'characters': ['Priya Sharma', 'Mr. Sharma'],
        'genders': {'Priya Sharma': 'female', 'Mr. Sharma': 'male'},
        'professions': {'Priya Sharma': [], 'Mr. Sharma': ['businessman']},
        'relationships': {'Priya Sharma': ['daughter of businessman Mr. Sharma']}
    },
    'test_case_2': {
        'characters': ['Meera'],
        'genders': {'Meera': 'female'},
        'professions': {'Meera': []},
        'relationships': {'Meera': ['belongs to a wealthy family', 'her husband']}
    }
}
