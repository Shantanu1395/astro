# data.py

def get_zodiac_sign(position):
    # Determine the zodiac sign based on the position in degrees
    if 0 <= position < 30:
        return "Aries"
    elif 30 <= position < 60:
        return "Taurus"
    elif 60 <= position < 90:
        return "Gemini"
    elif 90 <= position < 120:
        return "Cancer"
    elif 120 <= position < 150:
        return "Leo"
    elif 150 <= position < 180:
        return "Virgo"
    elif 180 <= position < 210:
        return "Libra"
    elif 210 <= position < 240:
        return "Scorpio"
    elif 240 <= position < 270:
        return "Sagittarius"
    elif 270 <= position < 300:
        return "Capricorn"
    elif 300 <= position < 330:
        return "Aquarius"
    elif 330 <= position < 360:
        return "Pisces"


planet_interpretations = {
    "Sun": {
        "Aries": "Your Sun is in Aries: You are energetic, enthusiastic, and a natural leader.",
        "Taurus": "Your Sun is in Taurus: You are practical, reliable, and have a strong sense of values.",
        "Gemini": "Your Sun is in Gemini: You are adaptable, curious, and a good communicator.",
        "Cancer": "Your Sun is in Cancer: You are nurturing, sensitive, and value family and home.",
        "Leo": "Your Sun is in Leo: You are confident, creative, and love to be in the spotlight.",
        "Virgo": "Your Sun is in Virgo: You are analytical, detail-oriented, and practical.",
        "Libra": "Your Sun is in Libra: You are diplomatic, charming, and value harmony and relationships.",
        "Scorpio": "Your Sun is in Scorpio: You are intense, passionate, and deeply emotional.",
        "Sagittarius": "Your Sun is in Sagittarius: You are adventurous, optimistic, and love to explore new ideas.",
        "Capricorn": "Your Sun is in Capricorn: You are disciplined, ambitious, and value hard work.",
        "Aquarius": "Your Sun is in Aquarius: You are independent, innovative, and value individuality.",
        "Pisces": "Your Sun is in Pisces: You are compassionate, imaginative, and sensitive."
    },
    "Moon": {
        "Aries": "Your Moon is in Aries: You are emotionally strong, assertive, and quick to act.",
        "Taurus": "Your Moon is in Taurus: You are emotionally stable, patient, and value security.",
        "Gemini": "Your Moon is in Gemini: You are emotionally curious, adaptable, and communicative.",
        "Cancer": "Your Moon is in Cancer: You are emotionally sensitive, nurturing, and family-oriented.",
        "Leo": "Your Moon is in Leo: You are emotionally expressive, confident, and enjoy attention.",
        "Virgo": "Your Moon is in Virgo: You are emotionally practical, detail-oriented, and value order.",
        "Libra": "Your Moon is in Libra: You are emotionally balanced, diplomatic, and seek harmony in relationships.",
        "Scorpio": "Your Moon is in Scorpio: You are emotionally intense, passionate, and value depth in relationships.",
        "Sagittarius": "Your Moon is in Sagittarius: You are emotionally adventurous, optimistic, and value freedom.",
        "Capricorn": "Your Moon is in Capricorn: You are emotionally disciplined, responsible, and value achievement.",
        "Aquarius": "Your Moon is in Aquarius: You are emotionally independent, innovative, and value individuality.",
        "Pisces": "Your Moon is in Pisces: You are emotionally compassionate, imaginative, and sensitive."
    },
    "Mercury": {
        "Aries": "Your Mercury is in Aries: You think quickly, speak directly, and are decisive.",
        "Taurus": "Your Mercury is in Taurus: You are practical, grounded, and deliberate in communication.",
        "Gemini": "Your Mercury is in Gemini: You are curious, adaptable, and a good communicator.",
        "Cancer": "Your Mercury is in Cancer: You think with your emotions and are intuitive.",
        "Leo": "Your Mercury is in Leo: You communicate with confidence, creativity, and flair.",
        "Virgo": "Your Mercury is in Virgo: You are analytical, detail-oriented, and precise in communication.",
        "Libra": "Your Mercury is in Libra: You are diplomatic, fair, and seek balance in communication.",
        "Scorpio": "Your Mercury is in Scorpio: You think deeply, communicate passionately, and value truth.",
        "Sagittarius": "Your Mercury is in Sagittarius: You are philosophical, optimistic, and direct in communication.",
        "Capricorn": "Your Mercury is in Capricorn: You are disciplined, serious, and strategic in your thinking.",
        "Aquarius": "Your Mercury is in Aquarius: You are innovative, independent, and think outside the box.",
        "Pisces": "Your Mercury is in Pisces: You are imaginative, intuitive, and empathetic in communication."
    },
    "Venus": {
        "Aries": "Your Venus is in Aries: You love passionately, are adventurous in relationships, and value excitement.",
        "Taurus": "Your Venus is in Taurus: You are sensual, value stability, and seek comfort in relationships.",
        "Gemini": "Your Venus is in Gemini: You value communication, variety, and intellectual connection in love.",
        "Cancer": "Your Venus is in Cancer: You are nurturing, sensitive, and value emotional security in love.",
        "Leo": "Your Venus is in Leo: You are warm-hearted, expressive, and seek admiration in relationships.",
        "Virgo": "Your Venus is in Virgo: You are practical, loyal, and value subtlety in relationships.",
        "Libra": "Your Venus is in Libra: You value harmony, balance, and beauty in relationships.",
        "Scorpio": "Your Venus is in Scorpio: You love intensely, value loyalty, and seek deep emotional connections.",
        "Sagittarius": "Your Venus is in Sagittarius: You are adventurous, optimistic, and value freedom in love.",
        "Capricorn": "Your Venus is in Capricorn: You are disciplined, value tradition, and seek long-term commitment in love.",
        "Aquarius": "Your Venus is in Aquarius: You are independent, innovative, and value unconventional relationships.",
        "Pisces": "Your Venus is in Pisces: You are compassionate, empathetic, and value spiritual connection in love."
    },
    "Mars": {
        "Aries": "Your Mars is in Aries: You are assertive, energetic, and take direct action.",
        "Taurus": "Your Mars is in Taurus: You are determined, patient, and persistent in pursuing goals.",
        "Gemini": "Your Mars is in Gemini: You are energetic, curious, and take quick, flexible actions.",
        "Cancer": "Your Mars is in Cancer: You are protective, emotionally driven, and take action to secure your home and loved ones.",
        "Leo": "Your Mars is in Leo: You are confident, passionate, and take creative, dramatic actions.",
        "Virgo": "Your Mars is in Virgo: You are precise, methodical, and take practical actions.",
        "Libra": "Your Mars is in Libra: You are diplomatic, balanced, and take actions that promote harmony.",
        "Scorpio": "Your Mars is in Scorpio: You are intense, determined, and take transformative actions.",
        "Sagittarius": "Your Mars is in Sagittarius: You are adventurous, optimistic, and take bold, expansive actions.",
        "Capricorn": "Your Mars is in Capricorn: You are disciplined, ambitious, and take strategic, long-term actions.",
        "Aquarius": "Your Mars is in Aquarius: You are independent, innovative, and take unconventional actions.",
        "Pisces": "Your Mars is in Pisces: You are compassionate, intuitive, and take empathetic, imaginative actions."
    },
    "Jupiter": {
        "Aries": "Your Jupiter is in Aries: You are confident, optimistic, and take bold actions to expand your horizons.",
        "Taurus": "Your Jupiter is in Taurus: You value stability, security, and take practical actions to expand wealth and comfort.",
        "Gemini": "Your Jupiter is in Gemini: You are curious, adaptable, and seek to expand your knowledge and communication skills.",
        "Cancer": "Your Jupiter is in Cancer: You are nurturing, emotionally expansive, and seek to grow your home and family.",
        "Leo": "Your Jupiter is in Leo: You are confident, creative, and seek to expand your influence and recognition.",
        "Virgo": "Your Jupiter is in Virgo: You are practical, detail-oriented, and seek to expand your skills and knowledge through service.",
        "Libra": "Your Jupiter is in Libra: You value harmony, balance, and seek to expand relationships and social connections.",
        "Scorpio": "Your Jupiter is in Scorpio: You are intense, transformative, and seek to expand your understanding of deep, hidden truths.",
        "Sagittarius": "Your Jupiter is in Sagittarius: You are adventurous, optimistic, and seek to expand your understanding of the world through exploration.",
        "Capricorn": "Your Jupiter is in Capricorn: You are disciplined, ambitious, and seek to expand your success and achievements through hard work.",
        "Aquarius": "Your Jupiter is in Aquarius: You are innovative, independent, and seek to expand your understanding through unconventional means.",
        "Pisces": "Your Jupiter is in Pisces: You are compassionate, imaginative, and seek to expand your understanding through spiritual and emotional experiences."
    },
    "Saturn": {
        "Aries": "Your Saturn is in Aries: You are disciplined, responsible, and take a serious approach to leadership and independence.",
        "Taurus": "Your Saturn is in Taurus: You are practical, patient, and take a disciplined approach to building stability and security.",
        "Gemini": "Your Saturn is in Gemini: You are serious, disciplined, and take a methodical approach to communication and learning.",
        "Cancer": "Your Saturn is in Cancer: You are responsible, nurturing, and take a serious approach to home and family.",
        "Leo": "Your Saturn is in Leo: You are disciplined, ambitious, and take a serious approach to creativity and self-expression.",
        "Virgo": "Your Saturn is in Virgo: You are practical, disciplined, and take a serious approach to health, service, and daily routines.",
        "Libra": "Your Saturn is in Libra: You are responsible, fair, and take a serious approach to relationships and partnerships.",
        "Scorpio": "Your Saturn is in Scorpio: You are intense, disciplined, and take a serious approach to transformation and deep emotional work.",
        "Sagittarius": "Your Saturn is in Sagittarius: You are disciplined, serious, and take a methodical approach to exploration, philosophy, and higher learning.",
        "Capricorn": "Your Saturn is in Capricorn: You are disciplined, ambitious, and take a serious approach to success and achievement.",
        "Aquarius": "Your Saturn is in Aquarius: You are innovative, disciplined, and take a serious approach to social change and unconventional ideas.",
        "Pisces": "Your Saturn is in Pisces: You are compassionate, disciplined, and take a serious approach to spiritual growth and emotional responsibility."
    },
    "Uranus": {
        "Aries": "Your Uranus is in Aries: You are innovative, independent, and seek to break new ground in leadership and individuality.",
        "Taurus": "Your Uranus is in Taurus: You are innovative, practical, and seek to revolutionize your approach to stability and security.",
        "Gemini": "Your Uranus is in Gemini: You are curious, independent, and seek to revolutionize communication and learning.",
        "Cancer": "Your Uranus is in Cancer: You are emotionally independent, innovative, and seek to break new ground in home and family matters.",
        "Leo": "Your Uranus is in Leo: You are creative, independent, and seek to revolutionize self-expression and creativity.",
        "Virgo": "Your Uranus is in Virgo: You are practical, innovative, and seek to revolutionize health, service, and daily routines.",
        "Libra": "Your Uranus is in Libra: You are independent, innovative, and seek to revolutionize relationships and partnerships.",
        "Scorpio": "Your Uranus is in Scorpio: You are intense, independent, and seek to revolutionize transformation and deep emotional work.",
        "Sagittarius": "Your Uranus is in Sagittarius: You are adventurous, independent, and seek to revolutionize exploration, philosophy, and higher learning.",
        "Capricorn": "Your Uranus is in Capricorn: You are disciplined, independent, and seek to revolutionize success and achievement.",
        "Aquarius": "Your Uranus is in Aquarius: You are innovative, independent, and seek to revolutionize social change and unconventional ideas.",
        "Pisces": "Your Uranus is in Pisces: You are compassionate, independent, and seek to revolutionize spiritual growth and emotional understanding."
    },
    "Neptune": {
        "Aries": "Your Neptune is in Aries: You are imaginative, spiritual, and seek to pioneer new paths in spirituality and creativity.",
        "Taurus": "Your Neptune is in Taurus: You are imaginative, grounded, and seek to bring spirituality into material reality.",
        "Gemini": "Your Neptune is in Gemini: You are imaginative, communicative, and seek to explore spirituality through learning and communication.",
        "Cancer": "Your Neptune is in Cancer: You are nurturing, imaginative, and seek to bring spiritual awareness into home and family life.",
        "Leo": "Your Neptune is in Leo: You are creative, imaginative, and seek to express spirituality through creativity and self-expression.",
        "Virgo": "Your Neptune is in Virgo: You are practical, imaginative, and seek to bring spirituality into daily routines and service.",
        "Libra": "Your Neptune is in Libra: You are imaginative, diplomatic, and seek to bring spirituality into relationships and partnerships.",
        "Scorpio": "Your Neptune is in Scorpio: You are intense, imaginative, and seek to explore spirituality through deep emotional transformation.",
        "Sagittarius": "Your Neptune is in Sagittarius: You are adventurous, imaginative, and seek to explore spirituality through philosophy and higher learning.",
        "Capricorn": "Your Neptune is in Capricorn: You are disciplined, imaginative, and seek to bring spirituality into success and achievement.",
        "Aquarius": "Your Neptune is in Aquarius: You are innovative, imaginative, and seek to bring spirituality into social change and unconventional ideas.",
        "Pisces": "Your Neptune is in Pisces: You are compassionate, imaginative, and seek to explore spirituality through empathy and emotional understanding."
    },
    "Pluto": {
        "Aries": "Your Pluto is in Aries: You are intense, transformative, and seek to pioneer new paths in leadership and individuality.",
        "Taurus": "Your Pluto is in Taurus: You are intense, determined, and seek to transform your approach to stability and security.",
        "Gemini": "Your Pluto is in Gemini: You are curious, intense, and seek to transform communication and learning.",
        "Cancer": "Your Pluto is in Cancer: You are emotionally intense, transformative, and seek to bring deep emotional awareness into home and family life.",
        "Leo": "Your Pluto is in Leo: You are creative, intense, and seek to transform self-expression and creativity.",
        "Virgo": "Your Pluto is in Virgo: You are practical, intense, and seek to transform health, service, and daily routines.",
        "Libra": "Your Pluto is in Libra: You are intense, transformative, and seek to bring deep emotional awareness into relationships and partnerships.",
        "Scorpio": "Your Pluto is in Scorpio: You are intense, transformative, and seek to explore deep emotional transformation and rebirth.",
        "Sagittarius": "Your Pluto is in Sagittarius: You are adventurous, intense, and seek to transform your understanding of philosophy, religion, and higher learning.",
        "Capricorn": "Your Pluto is in Capricorn: You are disciplined, intense, and seek to transform your approach to success and achievement.",
        "Aquarius": "Your Pluto is in Aquarius: You are innovative, intense, and seek to transform social structures and unconventional ideas.",
        "Pisces": "Your Pluto is in Pisces: You are compassionate, intense, and seek to explore deep emotional transformation through spirituality and empathy."
    }
}
