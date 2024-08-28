# data.py

planetary_energies = {
    "Sun": {
        "core_energy": {
            "core identity": {
                "Aries": {
                    "1st House": {
                        "manifestation": [
                            "Pioneering spirit, assertiveness, and courage.",
                            "Focus on independence and initiating action.",
                            "Strong leadership presence from an early age."
                        ],
                        "challenges": [
                            "Impatience, impulsiveness, and a tendency to act without considering consequences.",
                            "Struggles with balancing assertiveness and aggression."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Strong will to build personal resources.",
                            "Focus on financial independence and self-worth.",
                            "Dynamic approach to managing personal assets."
                        ],
                        "challenges": [
                            "Impulsiveness in spending and financial decisions.",
                            "Struggles with managing resources sustainably."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Energetic communication and quick thinking.",
                            "Focus on assertive and direct expression.",
                            "Dynamic approach to learning and sharing ideas."
                        ],
                        "challenges": [
                            "Impatience in communication, easily frustrated by slow responses.",
                            "Struggles with listening to others."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Strong desire to assert control over home and family.",
                            "Focus on creating a dynamic and energetic home environment.",
                            "Manifests as a protective and proactive approach to family matters."
                        ],
                        "challenges": [
                            "Tendency to be overly controlling in the domestic sphere.",
                            "Struggles with balancing independence with family responsibilities."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creative expression is bold, direct, and spontaneous.",
                            "Focus on pursuing personal passions and leadership in creative endeavors.",
                            "Manifests as a dynamic and enthusiastic approach to romance and hobbies."
                        ],
                        "challenges": [
                            "Impulsiveness in romantic relationships.",
                            "Struggles with balancing self-expression with consideration for others."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Energetic and proactive approach to work and daily routines.",
                            "Focus on taking initiative in health and fitness.",
                            "Manifests as a strong desire to lead in the workplace."
                        ],
                        "challenges": [
                            "Impatience with routine tasks.",
                            "Struggles with maintaining long-term health and work habits."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Direct and assertive approach to partnerships.",
                            "Focus on equality and independence within relationships.",
                            "Manifests as a strong presence in partnerships, with a desire to lead."
                        ],
                        "challenges": [
                            "Tendency to dominate relationships.",
                            "Struggles with compromise and balancing personal needs with partnership."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Intense and direct approach to transformation and shared resources.",
                            "Focus on exploring deep, often taboo subjects.",
                            "Manifests as a fearless approach to confronting personal fears and power dynamics."
                        ],
                        "challenges": [
                            "Tendency towards control in shared resources and emotional intensity.",
                            "Struggles with letting go of power and control."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Adventurous and bold approach to exploration and learning.",
                            "Focus on direct and assertive pursuit of knowledge and philosophy.",
                            "Manifests as a strong desire to lead in educational or philosophical endeavors."
                        ],
                        "challenges": [
                            "Impulsiveness in beliefs and tendency to be dogmatic.",
                            "Struggles with accepting different viewpoints."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Ambitious and driven approach to career and public life.",
                            "Focus on leadership and pioneering in professional pursuits.",
                            "Manifests as a dynamic and assertive presence in the public eye."
                        ],
                        "challenges": [
                            "Over-identification with career success.",
                            "Struggles with work-life balance."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Dynamic and assertive approach to friendships and social causes.",
                            "Focus on leading and initiating group activities.",
                            "Manifests as a strong presence in social networks and communities."
                        ],
                        "challenges": [
                            "Tendency to dominate social groups.",
                            "Struggles with collaboration and valuing others' contributions."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Direct and fearless exploration of the subconscious.",
                            "Focus on confronting hidden fears and secrets.",
                            "Manifests as a strong drive for personal transformation through introspection."
                        ],
                        "challenges": [
                            "Struggles with confronting deep-seated fears.",
                            "Tendency to repress emotions and avoid vulnerability."
                        ]
                    }
                },
                "Taurus": {
                    "1st House": {
                        "manifestation": [
                            "Stable, grounded, and practical self-expression.",
                            "Focus on personal comfort and physical well-being.",
                            "Patient and reliable demeanor."
                        ],
                        "challenges": [
                            "Stubbornness and resistance to change.",
                            "Overemphasis on material security."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Strong focus on accumulating wealth and possessions.",
                            "Manifests as a deep attachment to personal values and material comfort.",
                            "Tendency to seek stability through financial security."
                        ],
                        "challenges": [
                            "Possessiveness and difficulty in letting go of material goods.",
                            "Struggles with adapting to financial instability."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Practical and deliberate communication style.",
                            "Focus on stability in thoughts and ideas.",
                            "Patient and thorough approach to learning."
                        ],
                        "challenges": [
                            "Resistance to new ideas, preference for traditional views.",
                            "Struggles with adapting to rapid changes in communication."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Desire for a stable and comfortable home environment.",
                            "Focus on creating a secure and nurturing family life.",
                            "Manifests as a strong attachment to home and family."
                        ],
                        "challenges": [
                            "Overattachment to home and resistance to change in domestic life.",
                            "Struggles with letting go of the past."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creativity expressed through stable and tangible forms.",
                            "Focus on enjoying life's pleasures in a steady and consistent manner.",
                            "Manifests as a love for art, music, and the finer things in life."
                        ],
                        "challenges": [
                            "Tendency to become overly indulgent in pleasures.",
                            "Struggles with finding excitement in routine activities."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Practical and methodical approach to work and health.",
                            "Focus on consistency and reliability in daily routines.",
                            "Manifests as a strong work ethic and dedication to tasks."
                        ],
                        "challenges": [
                            "Resistance to change in work habits.",
                            "Struggles with balancing work and personal life."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Desire for stability and security in relationships.",
                            "Focus on building lasting partnerships based on mutual values.",
                            "Manifests as a loyal and reliable partner."
                        ],
                        "challenges": [
                            "Possessiveness and resistance to change in relationships.",
                            "Struggles with adapting to the needs of others."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Stable approach to shared resources and transformation.",
                            "Focus on creating security through joint ventures.",
                            "Manifests as a deep commitment to transformational processes."
                        ],
                        "challenges": [
                            "Fear of change and difficulty in letting go of control.",
                            "Struggles with embracing the unknown."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Practical approach to philosophy and higher learning.",
                            "Focus on applying knowledge in a tangible and useful way.",
                            "Manifests as a steady pursuit of truth and understanding."
                        ],
                        "challenges": [
                            "Resistance to new ideas and perspectives.",
                            "Struggles with being overly cautious in exploring new beliefs."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Steady and determined approach to career and public life.",
                            "Focus on building a solid reputation and achieving long-term goals.",
                            "Manifests as a reliable and respected figure in the public eye."
                        ],
                        "challenges": [
                            "Overattachment to career and public image.",
                            "Struggles with adapting to changes in professional life."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Stable and consistent approach to friendships and social causes.",
                            "Focus on building lasting connections based on shared values.",
                            "Manifests as a loyal and dependable friend and community member."
                        ],
                        "challenges": [
                            "Resistance to new social ideas and changes in group dynamics.",
                            "Struggles with embracing diversity in social settings."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Stable and grounded approach to exploring the subconscious.",
                            "Focus on creating security through spiritual practices and inner reflection.",
                            "Manifests as a deep and steady commitment to personal growth."
                        ],
                        "challenges": [
                            "Fear of the unknown and resistance to spiritual transformation.",
                            "Struggles with letting go of material attachments."
                        ]
                    }
                },
                "Gemini": {
                    "1st House": {
                        "manifestation": [
                            "Adaptable, curious, and communicative self-expression.",
                            "Focus on versatility and intellectual engagement.",
                            "Manifests as a lively and inquisitive personality."
                        ],
                        "challenges": [
                            "Scattered focus and difficulty in maintaining long-term commitments.",
                            "Tendency to be superficial or inconsistent in personal expression."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Diverse sources of income and value systems.",
                            "Focus on intellectual assets and communication skills as resources.",
                            "Adaptable approach to financial management."
                        ],
                        "challenges": [
                            "Inconsistency in financial planning.",
                            "Struggles with maintaining a steady income stream."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Curiosity drives a love for learning and communication.",
                            "Focus on a variety of subjects and interests.",
                            "Dynamic and adaptable communication style."
                        ],
                        "challenges": [
                            "Difficulty in focusing on one topic, easily distracted.",
                            "Struggles with superficial understanding of subjects."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Restless and curious approach to home and family life.",
                            "Focus on maintaining intellectual stimulation at home.",
                            "Manifests as a desire to explore new ideas within the family structure."
                        ],
                        "challenges": [
                            "Tendency to be inconsistent in family responsibilities.",
                            "Struggles with establishing a stable and consistent home environment."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creative expression through a variety of interests.",
                            "Focus on exploring multiple hobbies and passions.",
                            "Manifests as a lively and versatile approach to romance and leisure."
                        ],
                        "challenges": [
                            "Difficulty in committing to one creative project.",
                            "Tendency to be inconsistent in romantic relationships."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Adaptable and versatile approach to work and daily routines.",
                            "Focus on mental stimulation and variety in the workplace.",
                            "Manifests as a dynamic and flexible work style."
                        ],
                        "challenges": [
                            "Tendency to become easily bored with routine tasks.",
                            "Struggles with maintaining consistency in daily habits."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Communicative and curious approach to partnerships.",
                            "Focus on intellectual connection and mental stimulation in relationships.",
                            "Manifests as a lively and engaging partner."
                        ],
                        "challenges": [
                            "Inconsistency in commitment within relationships.",
                            "Struggles with balancing personal freedom with partnership stability."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Curiosity about the deeper aspects of life and shared resources.",
                            "Focus on exploring taboo subjects and intellectualizing emotions.",
                            "Manifests as a desire to understand and communicate about transformation and power dynamics."
                        ],
                        "challenges": [
                            "Tendency to intellectualize emotions, avoiding deeper emotional connections.",
                            "Struggles with consistency in managing shared resources."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Love for learning and exploring diverse philosophies and cultures.",
                            "Focus on intellectual exploration and expanding knowledge.",
                            "Manifests as a desire to travel and engage with different perspectives."
                        ],
                        "challenges": [
                            "Difficulty in committing to one belief system or philosophy.",
                            "Tendency to be superficial in understanding complex ideas."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Versatile and communicative approach to career and public life.",
                            "Focus on adaptability and intellectual engagement in professional pursuits.",
                            "Manifests as a dynamic and flexible presence in the public eye."
                        ],
                        "challenges": [
                            "Inconsistency in career goals and professional identity.",
                            "Struggles with maintaining a long-term career path."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Curious and communicative approach to friendships and social causes.",
                            "Focus on intellectual connection and diverse social networks.",
                            "Manifests as a lively and engaging presence in group activities."
                        ],
                        "challenges": [
                            "Tendency to be inconsistent in social commitments.",
                            "Struggles with maintaining long-term friendships."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Curiosity about the subconscious and spiritual exploration.",
                            "Focus on intellectualizing spiritual experiences and inner reflection.",
                            "Manifests as a desire to understand the mysteries of life through a mental lens."
                        ],
                        "challenges": [
                            "Difficulty in quieting the mind for deeper spiritual experiences.",
                            "Struggles with consistent spiritual practices."
                        ]
                    }
                },
                "Cancer": {
                    "1st House": {
                        "manifestation": [
                            "Emotionally sensitive and nurturing self-expression.",
                            "Focus on home, family, and emotional security.",
                            "Manifests as a caring and protective personality."
                        ],
                        "challenges": [
                            "Overemphasis on emotional security can lead to clinginess.",
                            "Difficulty in separating personal identity from family roles."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Focus on financial security to protect loved ones.",
                            "Manifests as an emotional attachment to personal resources.",
                            "Nurturing approach to managing assets."
                        ],
                        "challenges": [
                            "Overprotectiveness of resources.",
                            "Struggles with sharing or delegating financial responsibilities."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Emotionally driven communication style.",
                            "Focus on nurturing close relationships through communication.",
                            "Manifests as a caring and empathetic listener."
                        ],
                        "challenges": [
                            "Overly emotional reactions in communication.",
                            "Struggles with objective thinking."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Deep connection to home and family life.",
                            "Focus on creating a nurturing and secure domestic environment.",
                            "Manifests as a strong sense of responsibility towards family."
                        ],
                        "challenges": [
                            "Overattachment to family and home can lead to excessive worry.",
                            "Difficulty in letting go of past family issues."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creative expression is deeply emotional and nurturing.",
                            "Focus on caring for others through creative or recreational activities.",
                            "Manifests as a protective and loving approach to children and romantic partners."
                        ],
                        "challenges": [
                            "Tendency to be overprotective in romantic relationships.",
                            "Struggles with balancing emotional involvement in creative projects."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Caring and supportive approach to work and daily routines.",
                            "Focus on nurturing colleagues and creating a harmonious work environment.",
                            "Manifests as a strong desire to help others in the workplace."
                        ],
                        "challenges": [
                            "Overinvolvement in the emotional well-being of coworkers.",
                            "Struggles with setting boundaries in the workplace."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Deep emotional connection and nurturing approach to partnerships.",
                            "Focus on creating security and stability in relationships.",
                            "Manifests as a loyal and protective partner."
                        ],
                        "challenges": [
                            "Tendency to be overly dependent on relationships for emotional security.",
                            "Struggles with balancing personal needs with partnership dynamics."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Emotionally intense approach to shared resources and transformation.",
                            "Focus on creating deep emotional bonds through shared experiences.",
                            "Manifests as a strong desire to nurture through transformative processes."
                        ],
                        "challenges": [
                            "Tendency to become overly possessive in emotional bonds.",
                            "Struggles with letting go of control in shared resources."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Emotionally invested in exploring cultural and philosophical ideas.",
                            "Focus on nurturing a deeper understanding of the world.",
                            "Manifests as a caring and empathetic approach to different beliefs and cultures."
                        ],
                        "challenges": [
                            "Overattachment to personal beliefs can lead to close-mindedness.",
                            "Struggles with accepting differing viewpoints."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Protective and nurturing approach to career and public life.",
                            "Focus on creating a secure and stable professional environment.",
                            "Manifests as a strong desire to care for others in leadership roles."
                        ],
                        "challenges": [
                            "Overattachment to professional reputation and public image.",
                            "Struggles with balancing career and family responsibilities."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Nurturing and supportive approach to friendships and social causes.",
                            "Focus on creating emotionally secure and caring social networks.",
                            "Manifests as a strong desire to help and protect friends and community members."
                        ],
                        "challenges": [
                            "Tendency to become overly involved in the emotional lives of friends.",
                            "Struggles with maintaining emotional boundaries in social groups."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Deep emotional connection to spirituality and the subconscious.",
                            "Focus on nurturing inner peace and emotional healing.",
                            "Manifests as a strong desire to care for others through spiritual practices."
                        ],
                        "challenges": [
                            "Tendency to become emotionally overwhelmed by subconscious fears.",
                            "Struggles with letting go of past emotional wounds."
                        ]
                    }
                },
                "Leo": {
                    "1st House": {
                        "manifestation": [
                            "Strong sense of self, confidence, and leadership.",
                            "Charismatic personality that draws attention.",
                            "Focus on self-expression and creativity.",
                            "Desire to be recognized and admired."
                        ],
                        "challenges": [
                            "Pride and arrogance can lead to conflicts.",
                            "Struggles with accepting criticism or failure.",
                            "Tendency to dominate conversations and situations.",
                            "Overemphasis on personal recognition can hinder teamwork."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Desire to achieve financial success as a means of self-validation.",
                            "Generosity with resources, often sharing wealth.",
                            "Focus on luxury and enjoying the finer things in life.",
                            "Creativity in generating income and managing resources."
                        ],
                        "challenges": [
                            "Overindulgence in luxury and materialism.",
                            "Tendency to equate self-worth with financial status.",
                            "Impulsive spending can lead to financial instability.",
                            "Struggles with balancing generosity and personal financial security."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Confident and expressive communication style.",
                            "Natural ability to inspire and motivate others with words.",
                            "Focus on creative expression through writing, speaking, or teaching.",
                            "Charismatic presence in social and intellectual circles."
                        ],
                        "challenges": [
                            "Tendency to dominate conversations and seek constant validation.",
                            "Struggles with listening to others and valuing their input.",
                            "Overconfidence in one's ideas can lead to conflicts.",
                            "Difficulty in accepting criticism or alternative viewpoints."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Strong attachment to home and family as sources of pride.",
                            "Desire to create a home environment that reflects personal success.",
                            "Leadership role within the family, often seen as a central figure.",
                            "Focus on creating a warm, inviting, and aesthetically pleasing home."
                        ],
                        "challenges": [
                            "Tendency to be overly controlling within the family.",
                            "Struggles with balancing personal needs with those of family members.",
                            "Overidentification with the family can lead to ego conflicts.",
                            "Difficulty in accepting family members' independence."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creativity and self-expression are central to identity.",
                            "Focus on enjoying life, romance, and personal passions.",
                            "Natural performer, with a flair for drama and entertainment.",
                            "Strong desire to be the center of attention in social settings."
                        ],
                        "challenges": [
                            "Tendency towards vanity and seeking constant admiration.",
                            "Struggles with handling rejection or lack of attention.",
                            "Overindulgence in pleasure and leisure can lead to irresponsibility.",
                            "Difficulty in sharing the spotlight with others."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Strong work ethic and desire to be recognized for efforts.",
                            "Focus on leadership roles within the workplace.",
                            "Creative approach to problem-solving and improving efficiency.",
                            "Desire to maintain a positive and energetic work environment."
                        ],
                        "challenges": [
                            "Overworking to prove self-worth can lead to burnout.",
                            "Struggles with accepting subordinate roles or criticism at work.",
                            "Tendency to take on too much responsibility.",
                            "Difficulty in delegating tasks and trusting others' capabilities."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Desire for a partner who reflects personal ideals of success and charisma.",
                            "Focus on equality in relationships, but often seeks to lead.",
                            "Charismatic and engaging presence in partnerships.",
                            "Strong need for admiration and validation from partners."
                        ],
                        "challenges": [
                            "Tendency to dominate relationships and overshadow partners.",
                            "Struggles with balancing personal needs with those of a partner.",
                            "Difficulty in accepting criticism from a partner.",
                            "Overemphasis on public image within the relationship."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Intense and dramatic approach to transformation and shared resources.",
                            "Focus on personal power and control in joint ventures.",
                            "Strong desire to uncover truths and hidden aspects of life.",
                            "Leadership in managing shared resources and finances."
                        ],
                        "challenges": [
                            "Tendency to be overly controlling in financial matters.",
                            "Struggles with sharing power and resources.",
                            "Fear of vulnerability can hinder deep emotional connections.",
                            "Difficulty in accepting change and loss of control."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Passionate about learning, philosophy, and exploring new ideas.",
                            "Focus on leadership roles in educational or spiritual communities.",
                            "Natural ability to inspire others with expansive ideas.",
                            "Desire to be recognized as an authority in intellectual pursuits."
                        ],
                        "challenges": [
                            "Tendency towards dogmatism and believing one's views are superior.",
                            "Struggles with accepting different cultural or philosophical perspectives.",
                            "Overconfidence in knowledge can lead to conflicts.",
                            "Difficulty in admitting mistakes or gaps in understanding."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Ambitious and driven to achieve public recognition and success.",
                            "Focus on leadership roles and career advancement.",
                            "Desire to leave a lasting legacy in the professional sphere.",
                            "Natural ability to inspire others and take charge in public roles."
                        ],
                        "challenges": [
                            "Tendency to overidentify with career success.",
                            "Struggles with work-life balance due to focus on public image.",
                            "Fear of failure or criticism can lead to overwork or stress.",
                            "Difficulty in accepting positions that do not offer recognition."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Leadership and charisma in social groups and causes.",
                            "Focus on contributing to society and making a positive impact.",
                            "Desire to be seen as a leader within community or social circles.",
                            "Strong network of friends and allies who share similar ideals."
                        ],
                        "challenges": [
                            "Tendency to dominate group dynamics and overshadow others.",
                            "Struggles with valuing others' contributions in social settings.",
                            "Overemphasis on personal recognition within social causes.",
                            "Difficulty in accepting shared leadership or collaborative efforts."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Deep connection to spirituality and the inner self.",
                            "Focus on using creative and leadership abilities for personal growth.",
                            "Desire to uncover hidden aspects of the self and the subconscious.",
                            "Leadership in spiritual or charitable endeavors, often behind the scenes."
                        ],
                        "challenges": [
                            "Tendency to struggle with feelings of inadequacy or self-doubt.",
                            "Fear of losing control in spiritual or psychological explorations.",
                            "Difficulty in balancing ego with humility in spiritual pursuits.",
                            "Struggles with letting go of the need for recognition in selfless acts."
                        ]
                    }
                },
                "Virgo": {
                    "1st House": {
                        "manifestation": [
                            "Practical, analytical, and detail-oriented self-expression.",
                            "Focus on self-improvement and personal efficiency.",
                            "Manifests as a humble and service-oriented personality.",
                            "Emphasis on health, wellness, and personal hygiene."
                        ],
                        "challenges": [
                            "Overcritical and perfectionistic tendencies.",
                            "Struggles with self-acceptance and overly high standards.",
                            "Tendency to worry excessively about minor details.",
                            "Difficulty in relaxing or letting go of control."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Practical and careful approach to financial management.",
                            "Focus on accumulating resources through hard work and efficiency.",
                            "Manifests as a deep connection between self-worth and productivity.",
                            "Emphasis on valuing modesty and simplicity in material possessions."
                        ],
                        "challenges": [
                            "Overattachment to financial security and material possessions.",
                            "Struggles with anxiety about financial stability.",
                            "Tendency to be frugal to the point of denying oneself pleasure.",
                            "Difficulty in spending money on non-essentials."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Analytical and precise communication style.",
                            "Focus on clear, concise, and practical exchanges of information.",
                            "Manifests as a logical and methodical thinker.",
                            "Emphasis on learning through observation and detailed analysis."
                        ],
                        "challenges": [
                            "Overcritical in communication, focusing on flaws or mistakes.",
                            "Struggles with expressing emotions or abstract ideas.",
                            "Tendency to get lost in details and miss the bigger picture.",
                            "Difficulty in accepting less-than-perfect work or ideas."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Orderly and efficient approach to home and family life.",
                            "Focus on creating a clean, organized, and functional domestic environment.",
                            "Manifests as a nurturing figure who provides practical support.",
                            "Emphasis on health and wellness within the family."
                        ],
                        "challenges": [
                            "Overemphasis on order can lead to rigidity in family dynamics.",
                            "Struggles with perfectionism in domestic matters.",
                            "Tendency to worry excessively about the well-being of family members.",
                            "Difficulty in relaxing and enjoying family life."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creativity expressed through practical, detailed, and useful projects.",
                            "Focus on hobbies that involve precision, such as crafts or writing.",
                            "Manifests as a love for organizing and improving creative processes.",
                            "Emphasis on modesty and humility in creative self-expression."
                        ],
                        "challenges": [
                            "Tendency to be overly critical of one's own creative efforts.",
                            "Struggles with embracing spontaneity and fun in creative activities.",
                            "Difficulty in expressing emotions through creative work.",
                            "Perfectionism can stifle creative freedom and joy."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Strong focus on work, health, and daily routines.",
                            "Manifests as a highly organized and efficient worker.",
                            "Emphasis on service to others and attention to detail.",
                            "Passion for improving processes and systems in the workplace."
                        ],
                        "challenges": [
                            "Overattachment to work and daily routines can lead to burnout.",
                            "Struggles with delegating tasks and trusting others.",
                            "Tendency to worry excessively about health and minor ailments.",
                            "Difficulty in relaxing and taking time off."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Practical and service-oriented approach to relationships.",
                            "Focus on partnership as a means of mutual support and improvement.",
                            "Manifests as a reliable and detail-oriented partner.",
                            "Emphasis on communication and problem-solving in relationships."
                        ],
                        "challenges": [
                            "Tendency to be overly critical of partners.",
                            "Struggles with balancing work and relationship commitments.",
                            "Difficulty in accepting imperfections in relationships.",
                            "Worrying too much about the stability of the partnership."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Analytical and practical approach to transformation and shared resources.",
                            "Focus on managing joint finances and emotional intimacy with care.",
                            "Manifests as a strong desire to understand the deeper aspects of life.",
                            "Emphasis on maintaining order and clarity in shared resources."
                        ],
                        "challenges": [
                            "Tendency to overanalyze emotional issues, avoiding deeper connections.",
                            "Struggles with trusting others in joint financial ventures.",
                            "Difficulty in letting go of control in transformative experiences.",
                            "Worrying excessively about the security of shared resources."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Practical and analytical approach to philosophy and higher learning.",
                            "Focus on applying knowledge in a useful and organized manner.",
                            "Manifests as a methodical and detail-oriented learner.",
                            "Emphasis on critical thinking and skepticism in exploring new ideas."
                        ],
                        "challenges": [
                            "Tendency to be overly skeptical or critical of new ideas.",
                            "Struggles with embracing abstract or spiritual concepts.",
                            "Difficulty in broadening perspectives beyond practical concerns.",
                            "Worrying about the practical applications of philosophical beliefs."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Methodical and organized approach to career and public life.",
                            "Focus on achieving recognition through hard work and attention to detail.",
                            "Manifests as a reliable and diligent professional.",
                            "Emphasis on service, efficiency, and perfection in professional endeavors."
                        ],
                        "challenges": [
                            "Overattachment to career success can lead to workaholism.",
                            "Struggles with accepting less-than-perfect outcomes in professional life.",
                            "Tendency to worry excessively about public image and reputation.",
                            "Difficulty in delegating responsibilities and trusting colleagues."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Analytical and practical approach to friendships and social causes.",
                            "Focus on contributing to society through service and practical solutions.",
                            "Manifests as a reliable and detail-oriented friend.",
                            "Emphasis on improving social systems and group dynamics."
                        ],
                        "challenges": [
                            "Tendency to be overly critical in social settings.",
                            "Struggles with accepting differing viewpoints within groups.",
                            "Difficulty in relaxing and enjoying social interactions.",
                            "Worrying excessively about the outcomes of social projects."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Practical and methodical approach to spirituality and introspection.",
                            "Focus on self-improvement through inner reflection and analysis.",
                            "Manifests as a deep desire to understand the subconscious mind.",
                            "Emphasis on bringing order and clarity to spiritual practices."
                        ],
                        "challenges": [
                            "Tendency to overanalyze spiritual experiences, missing their essence.",
                            "Struggles with letting go of control in spiritual matters.",
                            "Difficulty in embracing uncertainty and the unknown.",
                            "Worrying excessively about inner peace and spiritual progress."
                        ]
                    }
                },
                "Libra": {
                    "1st House": {
                        "manifestation": [
                            "Charming, diplomatic, and socially aware self-expression.",
                            "Focus on balance, harmony, and fairness in interactions.",
                            "Manifests as a cooperative and graceful personality.",
                            "Emphasis on forming relationships and social connections."
                        ],
                        "challenges": [
                            "Tendency towards indecisiveness and people-pleasing.",
                            "Struggles with asserting personal needs over maintaining harmony.",
                            "Difficulty in making decisions without external validation.",
                            "Overreliance on others for a sense of self-worth."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Desire for financial stability and fairness in resource management.",
                            "Focus on accumulating wealth through partnerships and collaborations.",
                            "Manifests as a balanced approach to material possessions and self-worth.",
                            "Emphasis on aesthetic and luxury items as symbols of status."
                        ],
                        "challenges": [
                            "Tendency to be overly concerned with material wealth and social status.",
                            "Struggles with balancing personal finances and shared resources.",
                            "Difficulty in making financial decisions independently.",
                            "Overattachment to luxury items and external appearances."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Diplomatic and tactful communication style.",
                            "Focus on creating harmony in conversations and social interactions.",
                            "Manifests as a skilled mediator and peacemaker.",
                            "Emphasis on fairness and balance in sharing ideas."
                        ],
                        "challenges": [
                            "Tendency to avoid conflict, leading to superficial conversations.",
                            "Struggles with asserting personal opinions in group settings.",
                            "Difficulty in making decisions and taking a firm stance.",
                            "Overreliance on others' opinions and validation."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Desire for a harmonious and aesthetically pleasing home environment.",
                            "Focus on creating balance and fairness in family dynamics.",
                            "Manifests as a nurturing and supportive family member.",
                            "Emphasis on maintaining peace and avoiding conflict at home."
                        ],
                        "challenges": [
                            "Tendency to prioritize harmony over addressing underlying issues.",
                            "Struggles with asserting personal needs within the family.",
                            "Difficulty in handling family conflicts and disagreements.",
                            "Overreliance on external appearances rather than emotional depth."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creativity expressed through beauty, art, and social engagement.",
                            "Focus on forming balanced and harmonious romantic relationships.",
                            "Manifests as a love for socializing and enjoying life's pleasures.",
                            "Emphasis on fairness and equality in romantic and creative endeavors."
                        ],
                        "challenges": [
                            "Tendency to be indecisive in romantic relationships.",
                            "Struggles with expressing individual creativity without external validation.",
                            "Difficulty in maintaining balance between personal and shared interests.",
                            "Overreliance on partners for creative inspiration and self-expression."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Desire for balance and harmony in the workplace.",
                            "Focus on creating fair and equitable work environments.",
                            "Manifests as a cooperative and diplomatic colleague.",
                            "Emphasis on maintaining physical and mental health through balanced routines."
                        ],
                        "challenges": [
                            "Tendency to avoid conflict in the workplace, leading to unresolved issues.",
                            "Struggles with asserting personal needs in professional settings.",
                            "Difficulty in making decisions related to work and health.",
                            "Overreliance on others' opinions in workplace matters."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Core identity expressed through partnerships and relationships.",
                            "Focus on balance, harmony, and equality in relationships.",
                            "Manifests as a strong desire for companionship and collaboration.",
                            "Emphasis on fairness and mutual respect in all partnerships."
                        ],
                        "challenges": [
                            "Tendency to lose personal identity in relationships.",
                            "Struggles with making decisions independently of a partner.",
                            "Difficulty in maintaining personal boundaries in relationships.",
                            "Overreliance on partnerships for a sense of self-worth."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Desire for balance and fairness in shared resources and intimacy.",
                            "Focus on creating equitable financial arrangements in joint ventures.",
                            "Manifests as a diplomatic and fair-minded approach to transformation.",
                            "Emphasis on maintaining harmony in deep emotional connections."
                        ],
                        "challenges": [
                            "Tendency to avoid addressing deep emotional issues to maintain peace.",
                            "Struggles with asserting personal needs in intimate relationships.",
                            "Difficulty in handling power dynamics and control in shared resources.",
                            "Overreliance on others in managing joint finances."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Balanced and fair approach to philosophy and higher learning.",
                            "Focus on exploring different cultural perspectives and ideas.",
                            "Manifests as a love for travel, education, and expanding horizons.",
                            "Emphasis on fairness, equality, and justice in beliefs and values."
                        ],
                        "challenges": [
                            "Tendency to be indecisive in adopting new beliefs or philosophies.",
                            "Struggles with asserting personal beliefs in the face of opposition.",
                            "Difficulty in committing to a single philosophical or spiritual path.",
                            "Overreliance on external validation in shaping personal beliefs."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Core identity expressed through career and public life.",
                            "Focus on achieving recognition through fairness, diplomacy, and cooperation.",
                            "Manifests as a strong desire to be seen as a leader in social justice or equality.",
                            "Emphasis on maintaining balance between personal and professional life."
                        ],
                        "challenges": [
                            "Tendency to avoid taking risks in career to maintain harmony.",
                            "Struggles with asserting leadership in professional settings.",
                            "Difficulty in making decisive career moves.",
                            "Overreliance on public approval and external recognition."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Desire for balanced and harmonious social networks.",
                            "Focus on forming fair and equal friendships.",
                            "Manifests as a cooperative and diplomatic presence in group activities.",
                            "Emphasis on contributing to social causes that promote equality and justice."
                        ],
                        "challenges": [
                            "Tendency to avoid addressing conflicts within social groups.",
                            "Struggles with asserting personal ideas in group settings.",
                            "Difficulty in maintaining balance between personal and group interests.",
                            "Overreliance on social approval for a sense of belonging."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Desire for inner peace and balance in the spiritual realm.",
                            "Focus on achieving harmony through introspection and spiritual practices.",
                            "Manifests as a deep connection to the subconscious mind and inner self.",
                            "Emphasis on finding peace through forgiveness and compassion."
                        ],
                        "challenges": [
                            "Tendency to avoid confronting personal fears and inner conflicts.",
                            "Struggles with asserting personal needs in spiritual practices.",
                            "Difficulty in balancing solitude with social interactions.",
                            "Overreliance on external validation in spiritual matters."
                        ]
                    }
                },
                "Scorpio": {
                    "1st House": {
                        "manifestation": [
                            "Intense, passionate, and transformative self-expression.",
                            "Focus on personal power and emotional depth.",
                            "Manifests as a magnetic and mysterious personality.",
                            "Strong desire to uncover truths and explore hidden aspects of life."
                        ],
                        "challenges": [
                            "Tendency towards secrecy, control, and manipulation.",
                            "Struggles with trust and vulnerability in relationships.",
                            "Difficulty in letting go of grudges or past hurts.",
                            "Prone to obsessive behaviors and power struggles."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Intense focus on financial security and material power.",
                            "Desire to transform personal resources into lasting wealth.",
                            "Manifests as a strong attachment to possessions that hold deep emotional significance.",
                            "Emphasis on building wealth through strategic and secretive means."
                        ],
                        "challenges": [
                            "Tendency towards possessiveness and fear of loss.",
                            "Struggles with financial secrecy and control issues.",
                            "Difficulty in trusting others with shared resources.",
                            "Prone to obsessing over financial security and material possessions."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Intense and probing communication style.",
                            "Focus on uncovering hidden truths through dialogue and investigation.",
                            "Manifests as a sharp, perceptive mind that seeks to understand the deeper meaning behind words.",
                            "Strong interest in psychology, research, and detective work."
                        ],
                        "challenges": [
                            "Tendency to be secretive and distrustful in communication.",
                            "Struggles with expressing emotions openly.",
                            "Difficulty in accepting superficial or light-hearted conversations.",
                            "Prone to obsessive thinking and mental control games."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Intense emotional connection to home and family.",
                            "Focus on creating a secure, private, and transformative domestic environment.",
                            "Manifests as a deep commitment to family legacy and emotional roots.",
                            "Strong desire to protect and control the home environment."
                        ],
                        "challenges": [
                            "Tendency towards emotional manipulation within the family.",
                            "Struggles with letting go of past family traumas.",
                            "Difficulty in allowing family members personal freedom.",
                            "Prone to secrecy and emotional intensity in domestic matters."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creative expression is intense, passionate, and transformative.",
                            "Focus on deep emotional connections in romantic relationships.",
                            "Manifests as a powerful and magnetic presence in creative and romantic pursuits.",
                            "Strong desire to explore taboo or hidden aspects of self-expression."
                        ],
                        "challenges": [
                            "Tendency towards jealousy and possessiveness in romance.",
                            "Struggles with controlling creative processes or partners.",
                            "Difficulty in embracing light-hearted or casual relationships.",
                            "Prone to dramatic and all-consuming romantic entanglements."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Intense focus on work, health, and daily routines.",
                            "Desire to transform and improve efficiency in the workplace.",
                            "Manifests as a strong commitment to service, often involving deep emotional investment.",
                            "Emphasis on psychological and emotional well-being in daily life."
                        ],
                        "challenges": [
                            "Tendency towards workaholism and obsessive perfectionism.",
                            "Struggles with maintaining work-life balance.",
                            "Difficulty in delegating tasks and trusting colleagues.",
                            "Prone to health issues related to stress and emotional repression."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Intense and passionate approach to partnerships.",
                            "Focus on deep emotional bonds and transformative relationships.",
                            "Manifests as a powerful and magnetic partner.",
                            "Strong desire for loyalty, trust, and emotional depth in relationships."
                        ],
                        "challenges": [
                            "Tendency towards possessiveness, jealousy, and control in relationships.",
                            "Struggles with trust and vulnerability.",
                            "Difficulty in maintaining balance and equality in partnerships.",
                            "Prone to intense power struggles and emotional manipulation."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Core identity is deeply connected to transformation, power, and shared resources.",
                            "Focus on exploring the mysteries of life, death, and rebirth.",
                            "Manifests as a strong desire to control and manage joint finances and resources.",
                            "Emphasis on psychological and emotional depth in all interactions."
                        ],
                        "challenges": [
                            "Tendency towards secrecy, control, and manipulation in financial matters.",
                            "Struggles with letting go and embracing change.",
                            "Difficulty in trusting others with shared resources.",
                            "Prone to obsession with power and control in intimate relationships."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Intense and passionate pursuit of knowledge and truth.",
                            "Focus on exploring deep philosophical and spiritual questions.",
                            "Manifests as a strong desire to uncover hidden truths in religion, philosophy, and culture.",
                            "Emphasis on transformative experiences through travel and higher learning."
                        ],
                        "challenges": [
                            "Tendency towards dogmatism and obsession with personal beliefs.",
                            "Struggles with accepting differing philosophical or spiritual viewpoints.",
                            "Difficulty in balancing deep inquiry with openness to new ideas.",
                            "Prone to intense and all-consuming quests for meaning."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Intense focus on career, power, and public recognition.",
                            "Desire to achieve a position of authority and control in professional life.",
                            "Manifests as a strong, magnetic presence in the public sphere.",
                            "Emphasis on transforming the world through career achievements."
                        ],
                        "challenges": [
                            "Tendency towards workaholism and obsession with career success.",
                            "Struggles with balancing personal life with professional ambitions.",
                            "Difficulty in sharing power or delegating authority.",
                            "Prone to intense power struggles and control issues in the workplace."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Intense and transformative approach to friendships and social causes.",
                            "Focus on forming deep, emotionally connected social networks.",
                            "Manifests as a powerful leader in social movements and group dynamics.",
                            "Strong desire to create meaningful change through collective efforts."
                        ],
                        "challenges": [
                            "Tendency towards controlling social dynamics and group decisions.",
                            "Struggles with balancing personal power with collective goals.",
                            "Difficulty in maintaining trust and openness in friendships.",
                            "Prone to power struggles and emotional intensity in social settings."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Core identity is deeply connected to the subconscious and spiritual transformation.",
                            "Focus on exploring hidden aspects of the self through introspection and spiritual practices.",
                            "Manifests as a strong desire for emotional and psychological healing.",
                            "Emphasis on transformative spiritual experiences and exploring the mysteries of the unconscious mind."
                        ],
                        "challenges": [
                            "Tendency towards secrecy, repression, and self-isolation.",
                            "Struggles with confronting deep-seated fears and emotional wounds.",
                            "Difficulty in letting go of past traumas and embracing spiritual growth.",
                            "Prone to obsessive thoughts and emotional intensity in solitude."
                        ]
                    }
                },
                "Sagittarius": {
                    "1st House": {
                        "manifestation": [
                            "Adventurous, optimistic, and philosophical self-expression.",
                            "Focus on freedom, exploration, and broadening horizons.",
                            "Manifests as a charismatic and outgoing personality.",
                            "Strong desire to share knowledge and inspire others."
                        ],
                        "challenges": [
                            "Tendency towards restlessness and impatience.",
                            "Struggles with commitment and following through on plans.",
                            "Difficulty in accepting limitations or routine.",
                            "Prone to overconfidence and taking unnecessary risks."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Desire to accumulate wealth through exploration and broadening knowledge.",
                            "Focus on financial independence and freedom.",
                            "Manifests as a generous and optimistic approach to material resources.",
                            "Emphasis on using resources to fund adventures and learning."
                        ],
                        "challenges": [
                            "Tendency towards impulsive spending and financial instability.",
                            "Struggles with maintaining long-term financial security.",
                            "Difficulty in valuing material possessions over experiences.",
                            "Prone to taking financial risks that may not be sustainable."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Expansive and philosophical communication style.",
                            "Focus on sharing knowledge, ideas, and experiences.",
                            "Manifests as a natural teacher and storyteller.",
                            "Strong interest in exploring different cultures and perspectives."
                        ],
                        "challenges": [
                            "Tendency to be overly opinionated or preachy in communication.",
                            "Struggles with focusing on details or mundane topics.",
                            "Difficulty in listening to others' viewpoints without judgment.",
                            "Prone to overextending oneself in social and intellectual pursuits."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Desire for a home that reflects cultural diversity and exploration.",
                            "Focus on creating a warm, welcoming, and expansive domestic environment.",
                            "Manifests as a strong connection to family traditions and heritage.",
                            "Emphasis on educating and inspiring family members."
                        ],
                        "challenges": [
                            "Tendency towards restlessness and a desire for change in the home.",
                            "Struggles with establishing a stable and consistent domestic life.",
                            "Difficulty in staying rooted in one place or maintaining long-term family commitments.",
                            "Prone to seeking freedom at the expense of family stability."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creativity expressed through exploration, travel, and learning.",
                            "Focus on enjoying life, romance, and personal passions with a sense of adventure.",
                            "Manifests as a love for spontaneity and taking risks in creative pursuits.",
                            "Emphasis on inspiring others through creative and playful expression."
                        ],
                        "challenges": [
                            "Tendency towards irresponsibility in romantic and creative endeavors.",
                            "Struggles with maintaining long-term commitments in love and hobbies.",
                            "Difficulty in balancing personal freedom with responsibilities.",
                            "Prone to overindulgence in pleasures and thrill-seeking."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Adventurous approach to work, health, and daily routines.",
                            "Focus on seeking variety and intellectual stimulation in the workplace.",
                            "Manifests as a desire to improve efficiency through broad perspectives.",
                            "Emphasis on maintaining health through an active and exploratory lifestyle."
                        ],
                        "challenges": [
                            "Tendency towards inconsistency and lack of discipline in daily routines.",
                            "Struggles with sticking to long-term health and work habits.",
                            "Difficulty in accepting routine tasks or responsibilities.",
                            "Prone to taking on too many projects or overextending oneself."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Desire for a partnership that values freedom, adventure, and exploration.",
                            "Focus on equality and shared growth in relationships.",
                            "Manifests as a charismatic and inspiring partner.",
                            "Strong interest in forming connections with people from different cultures or backgrounds."
                        ],
                        "challenges": [
                            "Tendency to prioritize personal freedom over relationship stability.",
                            "Struggles with maintaining long-term commitments in partnerships.",
                            "Difficulty in balancing independence with emotional intimacy.",
                            "Prone to seeking excitement and novelty at the expense of relationship depth."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Desire to explore the mysteries of life, death, and transformation.",
                            "Focus on sharing resources and power through trust and mutual growth.",
                            "Manifests as a philosophical approach to dealing with loss and change.",
                            "Emphasis on using shared resources to fund exploration and transformation."
                        ],
                        "challenges": [
                            "Tendency towards risk-taking and reckless behavior with shared resources.",
                            "Struggles with confronting the deeper, darker aspects of life.",
                            "Difficulty in maintaining financial stability in joint ventures.",
                            "Prone to seeking escape through philosophy or spirituality without addressing practical realities."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Core identity expressed through exploration, learning, and philosophy.",
                            "Focus on expanding horizons through travel, education, and spiritual growth.",
                            "Manifests as a strong desire to inspire and teach others.",
                            "Emphasis on freedom, truth-seeking, and broadening cultural understanding."
                        ],
                        "challenges": [
                            "Tendency towards dogmatism and overconfidence in personal beliefs.",
                            "Struggles with balancing intellectual pursuits with practical responsibilities.",
                            "Difficulty in accepting limitations or differing viewpoints.",
                            "Prone to overextending oneself in pursuit of knowledge or experiences."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Desire for a career that allows freedom, exploration, and growth.",
                            "Focus on achieving recognition through education, travel, or philosophical endeavors.",
                            "Manifests as a strong presence in public life, often as a teacher or leader.",
                            "Emphasis on inspiring others through professional achievements."
                        ],
                        "challenges": [
                            "Tendency towards restlessness and dissatisfaction with career limitations.",
                            "Struggles with maintaining long-term focus and discipline in professional life.",
                            "Difficulty in balancing personal freedom with public responsibilities.",
                            "Prone to overcommitment and spreading oneself too thin in career pursuits."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Adventurous and optimistic approach to friendships and social causes.",
                            "Focus on forming connections with like-minded individuals who value exploration and growth.",
                            "Manifests as a charismatic and inspiring presence in social groups.",
                            "Emphasis on contributing to social causes that promote freedom and education."
                        ],
                        "challenges": [
                            "Tendency towards inconsistency and lack of commitment in social relationships.",
                            "Struggles with balancing personal goals with collective responsibilities.",
                            "Difficulty in maintaining long-term friendships or social engagements.",
                            "Prone to seeking novelty and excitement at the expense of deeper connections."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Core identity is deeply connected to spiritual exploration and philosophical introspection.",
                            "Focus on seeking inner truth and understanding through meditation, study, or travel.",
                            "Manifests as a deep desire for spiritual growth and enlightenment.",
                            "Emphasis on using philosophy and spirituality to navigate the subconscious and hidden aspects of life."
                        ],
                        "challenges": [
                            "Tendency towards escapism and avoidance of practical responsibilities.",
                            "Struggles with confronting the deeper aspects of the subconscious mind.",
                            "Difficulty in balancing spiritual pursuits with everyday life.",
                            "Prone to overindulgence in philosophical or spiritual ideas without practical application."
                        ]
                    }
                },
                "Capricorn": {
                    "1st House": {
                        "manifestation": [
                            "Serious, disciplined, and responsible self-expression.",
                            "Focus on achieving long-term goals and building a strong personal foundation.",
                            "Manifests as a mature and reserved personality.",
                            "Emphasis on self-control, patience, and perseverance."
                        ],
                        "challenges": [
                            "Tendency towards pessimism, rigidity, and excessive seriousness.",
                            "Struggles with expressing emotions or allowing spontaneity.",
                            "Difficulty in accepting help or delegating responsibilities.",
                            "Prone to workaholism and neglecting personal relationships."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Strong focus on financial security and material success.",
                            "Desire to build wealth through hard work, discipline, and careful planning.",
                            "Manifests as a pragmatic approach to managing resources and valuing material stability.",
                            "Emphasis on long-term financial planning and investment."
                        ],
                        "challenges": [
                            "Tendency towards materialism and an overemphasis on financial success.",
                            "Struggles with balancing work and personal life due to financial goals.",
                            "Difficulty in spending money on leisure or non-essential items.",
                            "Prone to anxiety about financial stability and the future."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Practical and methodical communication style.",
                            "Focus on clear, concise, and purposeful exchanges of information.",
                            "Manifests as a logical and structured thinker.",
                            "Emphasis on careful planning and long-term goals in learning and communication."
                        ],
                        "challenges": [
                            "Tendency to be overly cautious or conservative in communication.",
                            "Struggles with expressing emotions or creativity in conversations.",
                            "Difficulty in embracing spontaneity or flexibility in thought.",
                            "Prone to skepticism or reluctance to accept new ideas."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Strong attachment to family traditions, heritage, and building a secure home.",
                            "Focus on creating a stable and well-structured domestic environment.",
                            "Manifests as a responsible and protective family member.",
                            "Emphasis on long-term family goals and generational legacy."
                        ],
                        "challenges": [
                            "Tendency towards being overly controlling or authoritarian within the family.",
                            "Struggles with expressing warmth and affection in domestic relationships.",
                            "Difficulty in accepting change or spontaneity within the home.",
                            "Prone to placing heavy expectations on family members."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creativity expressed through disciplined and purposeful efforts.",
                            "Focus on building long-lasting, meaningful romantic relationships.",
                            "Manifests as a structured and responsible approach to hobbies and leisure activities.",
                            "Emphasis on achieving recognition and success in creative pursuits."
                        ],
                        "challenges": [
                            "Tendency to be overly serious or rigid in romantic and creative expressions.",
                            "Struggles with allowing spontaneity and playfulness in life.",
                            "Difficulty in relaxing or enjoying leisure without feeling guilty.",
                            "Prone to placing high expectations on romantic partners and creative projects."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Disciplined and methodical approach to work, health, and daily routines.",
                            "Focus on achieving success through hard work, perseverance, and attention to detail.",
                            "Manifests as a strong sense of duty and responsibility in the workplace.",
                            "Emphasis on maintaining health through structured routines and self-discipline."
                        ],
                        "challenges": [
                            "Tendency towards workaholism and overemphasis on productivity.",
                            "Struggles with balancing work and personal life.",
                            "Difficulty in delegating tasks or relying on others.",
                            "Prone to stress-related health issues due to excessive responsibilities."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Desire for a stable, committed, and long-lasting partnership.",
                            "Focus on building a relationship based on mutual respect, responsibility, and shared goals.",
                            "Manifests as a loyal and reliable partner.",
                            "Emphasis on achieving success and stability through partnership."
                        ],
                        "challenges": [
                            "Tendency to be overly serious or controlling in relationships.",
                            "Struggles with expressing emotions or vulnerability with a partner.",
                            "Difficulty in balancing personal needs with relationship demands.",
                            "Prone to placing high expectations on the partner, leading to tension."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Strong focus on financial security and control in shared resources.",
                            "Desire to build wealth through joint ventures, investments, and strategic planning.",
                            "Manifests as a practical and disciplined approach to transformation and power dynamics.",
                            "Emphasis on managing emotional and psychological resources with control and discipline."
                        ],
                        "challenges": [
                            "Tendency towards control issues and fear of vulnerability in intimate relationships.",
                            "Struggles with letting go of control in shared resources or joint finances.",
                            "Difficulty in embracing emotional depth or spiritual transformation.",
                            "Prone to obsessing over financial security and power dynamics."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Practical and disciplined approach to philosophy, higher learning, and travel.",
                            "Focus on achieving success through structured education and careful planning.",
                            "Manifests as a deep respect for tradition, culture, and established beliefs.",
                            "Emphasis on building knowledge and experience through long-term efforts."
                        ],
                        "challenges": [
                            "Tendency towards conservatism or rigidity in beliefs.",
                            "Struggles with embracing new ideas or cultural perspectives.",
                            "Difficulty in balancing practical responsibilities with philosophical exploration.",
                            "Prone to skepticism or reluctance to take risks in intellectual pursuits."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Strong focus on career success, public recognition, and long-term goals.",
                            "Desire to achieve leadership positions through discipline, hard work, and perseverance.",
                            "Manifests as a powerful and authoritative presence in the professional sphere.",
                            "Emphasis on building a lasting legacy and achieving high status."
                        ],
                        "challenges": [
                            "Tendency towards workaholism and overidentification with career success.",
                            "Struggles with balancing personal life with professional ambitions.",
                            "Difficulty in delegating authority or sharing power in the workplace.",
                            "Prone to placing excessive pressure on oneself to achieve success."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Disciplined and strategic approach to friendships and social causes.",
                            "Focus on building long-lasting, meaningful connections with like-minded individuals.",
                            "Manifests as a responsible and reliable presence in social groups.",
                            "Emphasis on contributing to society through structured and well-planned efforts."
                        ],
                        "challenges": [
                            "Tendency towards conservatism or rigidity in social interactions.",
                            "Struggles with embracing spontaneity or flexibility in friendships.",
                            "Difficulty in balancing personal goals with collective responsibilities.",
                            "Prone to placing high expectations on social connections and group efforts."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Core identity is deeply connected to self-discipline and spiritual maturity.",
                            "Focus on achieving inner peace and understanding through structured spiritual practices.",
                            "Manifests as a strong desire to overcome personal limitations and fears.",
                            "Emphasis on using discipline and perseverance to navigate the subconscious mind."
                        ],
                        "challenges": [
                            "Tendency towards self-criticism, guilt, and fear of failure.",
                            "Struggles with letting go of control and embracing vulnerability in spiritual matters.",
                            "Difficulty in balancing spiritual pursuits with practical responsibilities.",
                            "Prone to repressing emotions and avoiding introspection."
                        ]
                    }
                },
                "Aquarius": {
                    "1st House": {
                        "manifestation": [
                            "Independent, innovative, and forward-thinking self-expression.",
                            "Focus on individuality, originality, and breaking away from conventions.",
                            "Manifests as a socially conscious and intellectually driven personality.",
                            "Strong desire to challenge the status quo and promote progressive ideas."
                        ],
                        "challenges": [
                            "Tendency towards aloofness, detachment, and unpredictability.",
                            "Struggles with emotional intimacy and connecting on a personal level.",
                            "Difficulty in accepting traditional norms or authority.",
                            "Prone to being overly rebellious or contrarian for the sake of it."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Unconventional approach to financial management and material resources.",
                            "Focus on achieving financial independence through innovative means.",
                            "Manifests as a unique set of values that prioritize intellectual and humanitarian pursuits.",
                            "Emphasis on using resources to support social causes or technological advancements."
                        ],
                        "challenges": [
                            "Tendency towards unpredictability in financial matters.",
                            "Struggles with maintaining long-term financial stability.",
                            "Difficulty in valuing traditional forms of wealth or material security.",
                            "Prone to taking financial risks on unconventional or untested ideas."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Innovative and unconventional communication style.",
                            "Focus on sharing progressive ideas and challenging established thought.",
                            "Manifests as a visionary thinker with a focus on future possibilities.",
                            "Strong interest in technology, science, and intellectual exploration."
                        ],
                        "challenges": [
                            "Tendency to be overly abstract or detached in communication.",
                            "Struggles with relating to others on an emotional level.",
                            "Difficulty in sticking to traditional learning or communication methods.",
                            "Prone to appearing aloof or intellectually superior in conversations."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Desire for a home environment that reflects individuality and progressive values.",
                            "Focus on creating a family dynamic that values freedom and non-conformity.",
                            "Manifests as a unique and possibly unconventional family life.",
                            "Emphasis on nurturing intellectual growth and social consciousness within the family."
                        ],
                        "challenges": [
                            "Tendency towards emotional detachment within the family.",
                            "Struggles with balancing personal freedom with family responsibilities.",
                            "Difficulty in establishing a stable and consistent domestic life.",
                            "Prone to rebellion against traditional family roles or expectations."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creativity expressed through unconventional, innovative, and futuristic ideas.",
                            "Focus on exploring new forms of art, technology, and self-expression.",
                            "Manifests as a love for experimental and avant-garde pursuits.",
                            "Emphasis on promoting social change or intellectual enlightenment through creative endeavors."
                        ],
                        "challenges": [
                            "Tendency towards detachment or lack of emotional depth in romantic relationships.",
                            "Struggles with maintaining consistency in creative or romantic pursuits.",
                            "Difficulty in adhering to traditional forms of self-expression.",
                            "Prone to taking creative risks that may not always be understood or appreciated."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Innovative approach to work, health, and daily routines.",
                            "Focus on improving efficiency and productivity through technology or unconventional methods.",
                            "Manifests as a strong desire to work in fields that promote social progress or intellectual growth.",
                            "Emphasis on maintaining health through unique or alternative practices."
                        ],
                        "challenges": [
                            "Tendency towards unpredictability and inconsistency in daily routines.",
                            "Struggles with accepting traditional workplace structures or hierarchies.",
                            "Difficulty in finding satisfaction in routine tasks or conventional jobs.",
                            "Prone to neglecting personal health in pursuit of intellectual or social goals."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Desire for a partnership that values freedom, equality, and intellectual connection.",
                            "Focus on forming relationships that are progressive, unconventional, or non-traditional.",
                            "Manifests as a strong commitment to equality and mutual respect in partnerships.",
                            "Emphasis on maintaining individuality and independence within relationships."
                        ],
                        "challenges": [
                            "Tendency towards detachment or aloofness in close relationships.",
                            "Struggles with emotional intimacy and vulnerability.",
                            "Difficulty in maintaining long-term commitments due to a desire for freedom.",
                            "Prone to seeking unconventional or non-committal relationships."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Innovative and unconventional approach to transformation, power, and shared resources.",
                            "Focus on exploring new and progressive ideas about life, death, and rebirth.",
                            "Manifests as a strong interest in psychology, technology, and futuristic concepts related to transformation.",
                            "Emphasis on using shared resources to promote social change or intellectual growth."
                        ],
                        "challenges": [
                            "Tendency towards emotional detachment in matters of intimacy and shared resources.",
                            "Struggles with trusting others and allowing emotional vulnerability.",
                            "Difficulty in accepting traditional power dynamics or control in relationships.",
                            "Prone to taking risks in shared financial ventures that may be unconventional or untested."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Core identity expressed through exploration, learning, and promoting progressive ideas.",
                            "Focus on expanding knowledge through travel, education, and social reform.",
                            "Manifests as a visionary thinker with a strong interest in humanitarian and intellectual pursuits.",
                            "Emphasis on challenging traditional beliefs and promoting global awareness."
                        ],
                        "challenges": [
                            "Tendency towards dogmatism or an overly intellectual approach to beliefs.",
                            "Struggles with accepting traditional cultural or philosophical perspectives.",
                            "Difficulty in balancing intellectual exploration with practical responsibilities.",
                            "Prone to seeking out unusual or unconventional experiences that may be difficult to integrate."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Desire for a career that allows freedom, innovation, and social impact.",
                            "Focus on achieving recognition through promoting progressive ideas or working in unconventional fields.",
                            "Manifests as a visionary leader in technology, social reform, or intellectual pursuits.",
                            "Emphasis on creating a lasting legacy that challenges the status quo."
                        ],
                        "challenges": [
                            "Tendency towards restlessness or dissatisfaction with traditional career paths.",
                            "Struggles with balancing personal freedom with professional responsibilities.",
                            "Difficulty in committing to long-term career goals or following traditional paths to success.",
                            "Prone to taking unconventional or risky career moves that may not always be sustainable."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Strong focus on social causes, friendships, and group dynamics that promote progress and innovation.",
                            "Manifests as a charismatic leader in social or intellectual movements.",
                            "Emphasis on creating change through collective efforts and promoting equality and freedom.",
                            "Strong desire to connect with like-minded individuals who share a vision for the future."
                        ],
                        "challenges": [
                            "Tendency towards aloofness or detachment in social interactions.",
                            "Struggles with maintaining long-term friendships due to a focus on intellectual connection over emotional intimacy.",
                            "Difficulty in balancing personal goals with collective responsibilities.",
                            "Prone to being overly idealistic or disconnected from practical realities in social causes."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Core identity is deeply connected to exploring the subconscious and promoting spiritual or intellectual growth.",
                            "Focus on using unconventional or innovative methods to explore the inner self and spiritual realities.",
                            "Manifests as a strong desire to break free from traditional spiritual practices and explore new frontiers.",
                            "Emphasis on integrating intellectual and spiritual insights into everyday life."
                        ],
                        "challenges": [
                            "Tendency towards escapism or avoidance of emotional depth in spiritual matters.",
                            "Struggles with balancing intellectual pursuits with emotional or spiritual growth.",
                            "Difficulty in accepting traditional spiritual or psychological frameworks.",
                            "Prone to becoming disconnected from practical realities in pursuit of intellectual or spiritual ideals."
                        ]
                    }
                },
                "Pisces": {
                    "1st House": {
                        "manifestation": [
                            "Empathetic, sensitive, and intuitive self-expression.",
                            "Focus on compassion, spirituality, and connecting with others on an emotional level.",
                            "Manifests as a dreamy, imaginative, and artistic personality.",
                            "Strong desire to help others and heal emotional wounds."
                        ],
                        "challenges": [
                            "Tendency towards escapism, indecisiveness, and lack of boundaries.",
                            "Struggles with assertiveness and standing up for oneself.",
                            "Difficulty in distinguishing between reality and fantasy.",
                            "Prone to absorbing others' emotions, leading to emotional overwhelm."
                        ]
                    },
                    "2nd House": {
                        "manifestation": [
                            "Spiritual and compassionate approach to material resources.",
                            "Focus on using wealth to help others and support spiritual or artistic pursuits.",
                            "Manifests as a tendency to value experiences and emotional fulfillment over material possessions.",
                            "Emphasis on finding financial stability through creative or healing professions."
                        ],
                        "challenges": [
                            "Tendency towards financial impracticality and lack of focus.",
                            "Struggles with setting financial boundaries or saving for the future.",
                            "Difficulty in managing resources due to idealism or lack of discipline.",
                            "Prone to being overly generous, leading to financial instability."
                        ]
                    },
                    "3rd House": {
                        "manifestation": [
                            "Imaginative and intuitive communication style.",
                            "Focus on expressing emotions, dreams, and creative ideas.",
                            "Manifests as a poetic, artistic, and deeply empathetic way of sharing thoughts.",
                            "Strong interest in spirituality, mysticism, and the arts."
                        ],
                        "challenges": [
                            "Tendency to be vague or unclear in communication.",
                            "Struggles with focusing on practical or mundane topics.",
                            "Difficulty in setting boundaries in communication, leading to misunderstandings.",
                            "Prone to escapism through daydreaming or fantasy."
                        ]
                    },
                    "4th House": {
                        "manifestation": [
                            "Desire for a home environment that is peaceful, nurturing, and spiritually uplifting.",
                            "Focus on creating a sanctuary for emotional healing and spiritual growth.",
                            "Manifests as a deep connection to family and a desire to care for loved ones.",
                            "Emphasis on bringing artistic and imaginative elements into the home."
                        ],
                        "challenges": [
                            "Tendency towards emotional dependency within the family.",
                            "Struggles with maintaining clear boundaries in domestic relationships.",
                            "Difficulty in facing practical domestic responsibilities.",
                            "Prone to escapism through fantasy or avoiding family conflicts."
                        ]
                    },
                    "5th House": {
                        "manifestation": [
                            "Creativity expressed through art, music, and spiritual pursuits.",
                            "Focus on romantic relationships that are deeply emotional and spiritually connected.",
                            "Manifests as a love for artistic expression and creating beauty in the world.",
                            "Emphasis on nurturing the imagination and enjoying life's simple pleasures."
                        ],
                        "challenges": [
                            "Tendency towards idealism and unrealistic expectations in romance.",
                            "Struggles with maintaining practical boundaries in creative or romantic endeavors.",
                            "Difficulty in balancing fantasy with reality in personal expression.",
                            "Prone to escapism through romantic fantasies or artistic pursuits."
                        ]
                    },
                    "6th House": {
                        "manifestation": [
                            "Compassionate and intuitive approach to work, health, and daily routines.",
                            "Focus on serving others through healing, creative, or spiritual work.",
                            "Manifests as a strong desire to help others in the workplace and create a harmonious environment.",
                            "Emphasis on maintaining emotional and spiritual well-being in daily life."
                        ],
                        "challenges": [
                            "Tendency towards disorganization and lack of structure in daily routines.",
                            "Struggles with maintaining physical health due to emotional sensitivity.",
                            "Difficulty in setting boundaries in the workplace, leading to burnout.",
                            "Prone to escapism through avoidance of daily responsibilities."
                        ]
                    },
                    "7th House": {
                        "manifestation": [
                            "Desire for a partnership that is emotionally deep, spiritually connected, and compassionate.",
                            "Focus on forming relationships that provide mutual support and understanding.",
                            "Manifests as a deeply empathetic and caring partner.",
                            "Emphasis on creating a harmonious and spiritually fulfilling relationship."
                        ],
                        "challenges": [
                            "Tendency towards codependency or losing oneself in relationships.",
                            "Struggles with setting boundaries and maintaining individuality in partnerships.",
                            "Difficulty in facing the realities of relationships, leading to idealization.",
                            "Prone to escapism through romantic fantasies or avoiding relationship conflicts."
                        ]
                    },
                    "8th House": {
                        "manifestation": [
                            "Spiritual and transformative approach to shared resources, intimacy, and power.",
                            "Focus on emotional and spiritual healing through deep connections with others.",
                            "Manifests as a strong interest in the mysteries of life, death, and the subconscious.",
                            "Emphasis on using shared resources for creative or healing purposes."
                        ],
                        "challenges": [
                            "Tendency towards emotional entanglement and difficulty in setting boundaries in intimate relationships.",
                            "Struggles with managing shared resources due to idealism or lack of practicality.",
                            "Difficulty in facing deep emotional or psychological issues, leading to escapism.",
                            "Prone to absorbing others' emotions, leading to emotional overwhelm."
                        ]
                    },
                    "9th House": {
                        "manifestation": [
                            "Core identity expressed through spiritual exploration, creativity, and compassion.",
                            "Focus on broadening horizons through travel, education, and mystical experiences.",
                            "Manifests as a deep interest in philosophy, religion, and the arts.",
                            "Emphasis on finding meaning and connection through spiritual and creative pursuits."
                        ],
                        "challenges": [
                            "Tendency towards escapism through spiritual or philosophical fantasies.",
                            "Struggles with grounding spiritual beliefs in practical reality.",
                            "Difficulty in maintaining focus on long-term educational or travel goals.",
                            "Prone to idealizing spiritual or philosophical paths without fully integrating them."
                        ]
                    },
                    "10th House": {
                        "manifestation": [
                            "Desire for a career that is spiritually fulfilling, creative, and compassionate.",
                            "Focus on achieving recognition through healing, artistic, or spiritual work.",
                            "Manifests as a strong presence in professions that serve others or promote empathy.",
                            "Emphasis on creating a legacy that reflects spiritual values and compassion."
                        ],
                        "challenges": [
                            "Tendency towards lack of direction or focus in career pursuits.",
                            "Struggles with balancing professional responsibilities with emotional or spiritual needs.",
                            "Difficulty in setting clear career goals or maintaining long-term focus.",
                            "Prone to escapism through avoiding career challenges or responsibilities."
                        ]
                    },
                    "11th House": {
                        "manifestation": [
                            "Compassionate and idealistic approach to friendships and social causes.",
                            "Focus on forming connections with like-minded individuals who share spiritual or creative values.",
                            "Manifests as a deeply empathetic and supportive presence in social groups.",
                            "Emphasis on contributing to social causes that promote compassion, healing, and creativity."
                        ],
                        "challenges": [
                            "Tendency towards idealism or unrealistic expectations in friendships.",
                            "Struggles with maintaining personal boundaries in social interactions.",
                            "Difficulty in balancing personal needs with collective responsibilities.",
                            "Prone to escapism through avoiding social conflicts or responsibilities."
                        ]
                    },
                    "12th House": {
                        "manifestation": [
                            "Core identity is deeply connected to spirituality, intuition, and the subconscious.",
                            "Focus on exploring the inner self and finding peace through meditation, dreams, or artistic expression.",
                            "Manifests as a strong desire to connect with the divine or explore mystical experiences.",
                            "Emphasis on healing past wounds and finding emotional and spiritual fulfillment."
                        ],
                        "challenges": [
                            "Tendency towards escapism, self-sacrifice, and emotional overwhelm.",
                            "Struggles with facing deep-seated fears or emotional wounds.",
                            "Difficulty in maintaining clear boundaries between the self and the collective unconscious.",
                            "Prone to absorbing others' emotions, leading to spiritual and emotional burnout."
                        ]
                    }
                }
            }
        }
    }
    # Extend this structure for other planets and core energies as needed.
}
