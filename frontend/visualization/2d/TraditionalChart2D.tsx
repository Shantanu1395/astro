// Traditional 2D Vedic Chart Component

import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import type { ChartData } from '@/types/astrology';

interface TraditionalChart2DProps {
  chartData: ChartData;
  highlightedElements: string[];
}

const TraditionalChart2D: React.FC<TraditionalChart2DProps> = ({
  chartData,
  highlightedElements,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);

  useEffect(() => {
    if (!svgRef.current || !chartData) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove(); // Clear previous content

    const width = 600;
    const height = 600;
    const centerX = width / 2;
    const centerY = height / 2;
    const radius = 250;

    svg.attr('width', width).attr('height', height);

    // Create main group
    const g = svg.append('g')
      .attr('transform', `translate(${centerX}, ${centerY})`);

    // Draw outer circle
    g.append('circle')
      .attr('r', radius)
      .attr('fill', 'none')
      .attr('stroke', '#e5e7eb')
      .attr('stroke-width', 2);

    // Draw house divisions (12 houses)
    for (let i = 0; i < 12; i++) {
      const angle = (i * 30 - 90) * (Math.PI / 180); // Start from top
      const x1 = 0;
      const y1 = 0;
      const x2 = Math.cos(angle) * radius;
      const y2 = Math.sin(angle) * radius;

      g.append('line')
        .attr('x1', x1)
        .attr('y1', y1)
        .attr('x2', x2)
        .attr('y2', y2)
        .attr('stroke', '#666666')
        .attr('stroke-width', 1)
        .attr('opacity', 0.5);
    }

    // Draw house numbers
    for (let i = 0; i < 12; i++) {
      const angle = (i * 30 + 15 - 90) * (Math.PI / 180); // Center of each house
      const x = Math.cos(angle) * (radius - 30);
      const y = Math.sin(angle) * (radius - 30);

      g.append('text')
        .attr('x', x)
        .attr('y', y)
        .attr('text-anchor', 'middle')
        .attr('dominant-baseline', 'middle')
        .attr('fill', '#9ca3af')
        .attr('font-size', '14px')
        .attr('font-weight', 'bold')
        .text(i + 1);
    }

    // Draw zodiac signs (rashis)
    if (chartData.rashis) {
      chartData.rashis.forEach((rashi, index) => {
        const angle = (index * 30 + 15 - 90) * (Math.PI / 180);
        const x = Math.cos(angle) * (radius + 40);
        const y = Math.sin(angle) * (radius + 40);

        const isHighlighted = highlightedElements.includes(rashi.name);

        g.append('circle')
          .attr('cx', x)
          .attr('cy', y)
          .attr('r', 20)
          .attr('fill', rashi.color || '#ff9500')
          .attr('opacity', isHighlighted ? 0.8 : 0.4)
          .attr('stroke', isHighlighted ? '#ffffff' : 'none')
          .attr('stroke-width', 2);

        g.append('text')
          .attr('x', x)
          .attr('y', y)
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('fill', '#ffffff')
          .attr('font-size', '16px')
          .attr('font-weight', 'bold')
          .text(rashi.symbol);

        // Rashi name
        g.append('text')
          .attr('x', x)
          .attr('y', y + 35)
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('fill', '#e5e7eb')
          .attr('font-size', '10px')
          .text(rashi.name);
      });
    }

    // Draw planets
    if (chartData.planets) {
      Object.entries(chartData.planets).forEach(([key, planet]) => {
        const houseAngle = ((planet.position.house - 1) * 30 + 15 - 90) * (Math.PI / 180);
        
        // Position planets within their houses
        const planetRadius = radius - 80;
        const x = Math.cos(houseAngle) * planetRadius;
        const y = Math.sin(houseAngle) * planetRadius;

        const isHighlighted = highlightedElements.includes(planet.name);

        // Planet circle
        g.append('circle')
          .attr('cx', x)
          .attr('cy', y)
          .attr('r', planet.size ? planet.size / 2 : 12)
          .attr('fill', planet.color || '#ffffff')
          .attr('opacity', isHighlighted ? 0.9 : 0.7)
          .attr('stroke', isHighlighted ? '#fbbf24' : '#ffffff')
          .attr('stroke-width', isHighlighted ? 3 : 1);

        // Planet symbol/name
        g.append('text')
          .attr('x', x)
          .attr('y', y)
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('fill', key === 'sun' ? '#000000' : '#ffffff')
          .attr('font-size', '10px')
          .attr('font-weight', 'bold')
          .text(planet.name.substring(0, 2).toUpperCase());

        // Retrograde indicator
        if (planet.position.retrograde) {
          g.append('text')
            .attr('x', x + 15)
            .attr('y', y - 15)
            .attr('text-anchor', 'middle')
            .attr('dominant-baseline', 'middle')
            .attr('fill', '#ff6464')
            .attr('font-size', '12px')
            .attr('font-weight', 'bold')
            .text('R');
        }
      });
    }

    // Chart title
    g.append('text')
      .attr('x', 0)
      .attr('y', -radius - 60)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('fill', '#e5e7eb')
      .attr('font-size', '18px')
      .attr('font-weight', 'bold')
      .text('Vedic Birth Chart (Rasi)');

    // Chart info
    if (chartData.chartSummary) {
      const info = [
        `Ascendant: ${chartData.chartSummary.ascendant}`,
        `Moon Sign: ${chartData.chartSummary.moonSign}`,
        `Sun Sign: ${chartData.chartSummary.sunSign}`,
      ];

      info.forEach((text, index) => {
        g.append('text')
          .attr('x', 0)
          .attr('y', radius + 40 + (index * 20))
          .attr('text-anchor', 'middle')
          .attr('dominant-baseline', 'middle')
          .attr('fill', '#9ca3af')
          .attr('font-size', '12px')
          .text(text);
      });
    }

  }, [chartData, highlightedElements]);

  return (
    <div className="w-full h-full flex items-center justify-center bg-cosmic-dark">
      <svg
        ref={svgRef}
        className="max-w-full max-h-full"
        style={{ filter: 'drop-shadow(0 0 10px rgba(59, 130, 246, 0.3))' }}
      />
    </div>
  );
};

export default TraditionalChart2D;
