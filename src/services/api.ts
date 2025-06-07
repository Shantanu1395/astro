// API Service for Vedic Astrology Data Integration

import axios from 'axios';
import type { PredictResponse, BirthData, ChartData, PredictionData } from '@/types/astrology';

// Configure axios instance
const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('❌ API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`✅ API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('❌ API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export interface PredictRequest {
  birth_date: string;
  birth_time: string;
  birth_location: string;
  latitude?: number;
  longitude?: number;
  timezone?: string;
}

export class AstrologyAPI {
  /**
   * Get comprehensive Vedic astrology prediction and chart data
   */
  static async getPrediction(birthData: BirthData): Promise<PredictResponse> {
    try {
      const request: PredictRequest = {
        birth_date: birthData.date,
        birth_time: birthData.time,
        birth_location: birthData.location.name,
        latitude: birthData.location.latitude,
        longitude: birthData.location.longitude,
        timezone: birthData.location.timezone,
      };

      const response = await api.post<PredictResponse>('/predict', request);
      
      if (!response.data.success) {
        throw new Error(response.data.error || 'Prediction failed');
      }

      return response.data;
    } catch (error) {
      console.error('Failed to get prediction:', error);
      throw new Error(
        error instanceof Error ? error.message : 'Failed to fetch astrological data'
      );
    }
  }

  /**
   * Get current planetary positions for transit analysis
   */
  static async getCurrentTransits(): Promise<any> {
    try {
      const response = await api.get('/transits/current');
      return response.data;
    } catch (error) {
      console.error('Failed to get current transits:', error);
      throw error;
    }
  }

  /**
   * Get upcoming transits for a specific period
   */
  static async getUpcomingTransits(
    startDate: string,
    endDate: string
  ): Promise<any> {
    try {
      const response = await api.get('/transits/upcoming', {
        params: { start_date: startDate, end_date: endDate },
      });
      return response.data;
    } catch (error) {
      console.error('Failed to get upcoming transits:', error);
      throw error;
    }
  }

  /**
   * Get detailed dasha periods
   */
  static async getDashaPeriods(birthData: BirthData): Promise<any> {
    try {
      const response = await api.post('/dasha', {
        birth_date: birthData.date,
        birth_time: birthData.time,
        birth_location: birthData.location.name,
      });
      return response.data;
    } catch (error) {
      console.error('Failed to get dasha periods:', error);
      throw error;
    }
  }
}

// Mock data for development and fallback
export const mockChartData: ChartData = {
  birthData: {
    date: '1990-01-15',
    time: '14:30:00',
    location: {
      name: 'New Delhi, India',
      latitude: 28.6139,
      longitude: 77.2090,
      timezone: 'Asia/Kolkata',
    },
  },
  planets: {
    sun: {
      name: 'Surya',
      sanskrit: 'सूर्य',
      english: 'Sun',
      position: {
        longitude: 300.5,
        latitude: 0.0,
        speed: 1.0,
        retrograde: false,
        sign: 'Capricorn',
        nakshatra: 'Uttara Ashadha',
        house: 10,
        degree: 0,
        minute: 30,
        second: 0,
      },
      strength: 85,
      dignity: 'neutral',
      color: '#fbbf24',
      size: 35,
      significance: 'Soul, Father, Authority, Government, Health',
      description: 'The Sun represents your core self, ego, and life purpose.',
      remedies: ['Surya Namaskara', 'Ruby gemstone', 'Sunday fasting'],
    },
    moon: {
      name: 'Chandra',
      sanskrit: 'चन्द्र',
      english: 'Moon',
      position: {
        longitude: 45.2,
        latitude: 0.0,
        speed: 13.2,
        retrograde: false,
        sign: 'Taurus',
        nakshatra: 'Rohini',
        house: 2,
        degree: 15,
        minute: 12,
        second: 0,
      },
      strength: 92,
      dignity: 'exalted',
      color: '#e5e7eb',
      size: 25,
      significance: 'Mind, Mother, Emotions, Public, Intuition',
      description: 'The Moon governs your emotional nature and subconscious mind.',
      remedies: ['Chandra mantra', 'Pearl gemstone', 'Monday fasting'],
    },
    // Add more planets...
  },
  rashis: [
    {
      name: 'Mesha',
      sanskrit: 'मेष',
      english: 'Aries',
      symbol: '♈',
      number: 1,
      element: 'fire',
      quality: 'cardinal',
      ruler: 'Mars',
      traits: 'Leadership, Initiative, Courage, Impulsiveness',
      color: '#dc2626',
      angle: 0,
    },
    // Add all 12 rashis...
  ],
  nakshatras: [
    {
      name: 'Ashwini',
      sanskrit: 'अश्विनी',
      number: 1,
      deity: 'Ashwini Kumaras',
      symbol: 'Horse head',
      traits: 'Healing, Speed, Initiative',
      pada: 1,
      startDegree: 0,
      endDegree: 13.33,
      ruler: 'Ketu',
      color: '#ff6b6b',
    },
    // Add all 27 nakshatras...
  ],
  houses: [
    {
      number: 1,
      name: 'Lagna',
      sanskrit: 'लग्न',
      english: 'Ascendant',
      significance: 'Self, Personality, Physical body, First impressions',
      planets: ['Mars'],
      sign: 'Aries',
      lord: 'Mars',
      strength: 78,
      angle: 90,
    },
    // Add all 12 houses...
  ],
  yogas: [
    {
      name: 'Gaja Kesari Yoga',
      sanskrit: 'गजकेसरी योग',
      type: 'raja',
      description: 'Moon and Jupiter in mutual kendras',
      effects: 'Wisdom, prosperity, leadership qualities',
      strength: 85,
      planets: ['Moon', 'Jupiter'],
      houses: [1, 4],
      isActive: true,
    },
    // Add more yogas...
  ],
  currentDasha: {
    planet: 'Jupiter',
    startDate: '2023-01-01',
    endDate: '2039-01-01',
    duration: 16,
    subPeriods: [
      {
        planet: 'Jupiter',
        startDate: '2023-01-01',
        endDate: '2025-05-01',
        duration: 2.33,
      },
    ],
    effects: 'Period of wisdom, growth, and spiritual development',
    predictions: [
      'Favorable for education and teaching',
      'Good for spiritual practices',
      'Possible expansion in career',
    ],
  },
  upcomingTransits: [],
  chartSummary: {
    ascendant: 'Aries',
    moonSign: 'Taurus',
    sunSign: 'Capricorn',
    birthNakshatra: 'Rohini',
    lunarMonth: 'Magha',
    tithi: 'Panchami',
    karana: 'Bava',
    yogaOfDay: 'Siddha',
  },
};

export default AstrologyAPI;
