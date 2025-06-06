#!/usr/bin/env python3
"""
Simple load testing script for the astrology API.
Use this to determine when you need to scale workers.
"""

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict

async def make_request(session: aiohttp.ClientSession, url: str) -> Dict:
    """Make a single API request and measure response time."""
    start_time = time.time()
    try:
        async with session.get(url) as response:
            await response.text()  # Read the response
            end_time = time.time()
            return {
                'status': response.status,
                'response_time': end_time - start_time,
                'success': response.status == 200
            }
    except Exception as e:
        end_time = time.time()
        return {
            'status': 0,
            'response_time': end_time - start_time,
            'success': False,
            'error': str(e)
        }

async def load_test(url: str, concurrent_requests: int, total_requests: int):
    """Run load test with specified concurrency."""
    print(f"🚀 Starting load test:")
    print(f"   URL: {url}")
    print(f"   Concurrent requests: {concurrent_requests}")
    print(f"   Total requests: {total_requests}")
    print(f"   Expected batches: {total_requests // concurrent_requests}")
    print()
    
    results = []
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        # Run requests in batches
        for batch in range(0, total_requests, concurrent_requests):
            batch_size = min(concurrent_requests, total_requests - batch)
            print(f"📊 Running batch {batch // concurrent_requests + 1} with {batch_size} requests...")
            
            # Create tasks for this batch
            tasks = [make_request(session, url) for _ in range(batch_size)]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            
            # Brief pause between batches
            await asyncio.sleep(0.1)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Analyze results
    successful_requests = [r for r in results if r['success']]
    failed_requests = [r for r in results if not r['success']]
    response_times = [r['response_time'] for r in successful_requests]
    
    print(f"\n📈 Load Test Results:")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Total requests: {len(results)}")
    print(f"   Successful: {len(successful_requests)}")
    print(f"   Failed: {len(failed_requests)}")
    print(f"   Success rate: {len(successful_requests)/len(results)*100:.1f}%")
    print(f"   Requests per second: {len(results)/total_time:.2f}")
    
    if response_times:
        print(f"\n⏱️  Response Time Statistics:")
        print(f"   Average: {statistics.mean(response_times):.2f}s")
        print(f"   Median: {statistics.median(response_times):.2f}s")
        print(f"   Min: {min(response_times):.2f}s")
        print(f"   Max: {max(response_times):.2f}s")
        print(f"   95th percentile: {sorted(response_times)[int(len(response_times)*0.95)]:.2f}s")
    
    # Scaling recommendations
    avg_response_time = statistics.mean(response_times) if response_times else float('inf')
    requests_per_second = len(results) / total_time
    
    print(f"\n🎯 Scaling Recommendations:")
    if avg_response_time > 10:
        print("   ⚠️  High response times detected - consider scaling up workers")
    elif len(failed_requests) > 0:
        print("   ❌ Failed requests detected - definitely need more workers")
    elif requests_per_second < 1:
        print("   🐌 Low throughput - consider scaling up workers")
    else:
        print("   ✅ Performance looks good for current load")
    
    return {
        'total_time': total_time,
        'successful_requests': len(successful_requests),
        'failed_requests': len(failed_requests),
        'avg_response_time': avg_response_time,
        'requests_per_second': requests_per_second
    }

async def main():
    """Run different load test scenarios."""
    base_url = "http://localhost:8000/api/test/shantanu"
    
    scenarios = [
        {"name": "Light Load", "concurrent": 1, "total": 5},
        {"name": "Medium Load", "concurrent": 3, "total": 15},
        {"name": "Heavy Load", "concurrent": 5, "total": 25},
        {"name": "Stress Test", "concurrent": 10, "total": 50},
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"🧪 {scenario['name']} Test")
        print('='*60)
        
        await load_test(
            url=base_url,
            concurrent_requests=scenario['concurrent'],
            total_requests=scenario['total']
        )
        
        print(f"\n⏸️  Waiting 5 seconds before next test...")
        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
