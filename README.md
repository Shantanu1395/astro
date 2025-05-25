# Vedic Astrology Prediction System

A modern web application that generates personalized Vedic astrology predictions using birth data and AI-powered interpretations.

## Features

- **Vedic Birth Chart Calculation**: Accurate sidereal calculations using Swiss Ephemeris
- **Dasha System**: Vimshottari Dasha periods and current planetary influences
- **AI-Powered Predictions**: LLM-generated interpretations based on chart data
- **Nakshatra Analysis**: Detailed lunar mansion calculations
- **Modern Web Interface**: Clean, responsive design with intuitive user experience

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SacredTextRag
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Install Swiss Ephemeris data** (optional, for more accurate calculations):
   ```bash
   # On macOS with Homebrew:
   brew install swisseph
   
   # On Ubuntu/Debian:
   sudo apt-get install libswe-dev
   ```

## Usage

1. **Start the application**:
   ```bash
   python main.py
   ```

2. **Open your browser** and navigate to `http://localhost:8000`

3. **Enter birth details**:
   - Full name
   - Birth date
   - Birth time (as accurate as possible)
   - Birth location (city, country)

4. **Get your prediction** with detailed Vedic analysis

## API Endpoints

- `GET /` - Main application interface
- `POST /predict` - Generate prediction from birth data
- `GET /health` - Health check endpoint

## Technologies Used

- **FastAPI** - Modern Python web framework
- **Swiss Ephemeris** - Astronomical calculations
- **Kerykeion** - Astrology library
- **OpenAI GPT** - AI-powered interpretations
- **Jinja2** - Template engine
- **Geopy** - Location geocoding

## Vedic Astrology Features

### Implemented:
- Sidereal zodiac calculations
- Vimshottari Dasha system
- Nakshatra (lunar mansions) analysis
- Planetary positions and house placements
- Current period analysis

### Future Enhancements:
- Divisional charts (D9, D10, etc.)
- Transit analysis
- Ashtakavarga system
- Remedial measures
- Multiple astrological systems (Western, Chinese, Mayan)

## Configuration

The application can be configured through environment variables:

- `OPENAI_API_KEY` - Required for AI predictions
- `DEBUG` - Enable debug mode
- `AYANAMSA` - Ayanamsa system (default: Lahiri)

## Contributing

This is a proof of concept for Vedic astrology calculations. Contributions are welcome for:

- Additional astrological systems
- Enhanced prediction algorithms
- UI/UX improvements
- API enhancements

## Disclaimer

This application is for educational and entertainment purposes. For serious astrological consultation, please consult with qualified Vedic astrologers.

## License

MIT License - see LICENSE file for details.
