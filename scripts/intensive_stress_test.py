#!/usr/bin/env python3
"""
Intensive stress test for 3-worker configuration.
Tests higher concurrency levels to find the breaking point.
"""

import asyncio
import aiohttp
import time
import statistics
from typing import List, Dict

async def make_request(session: aiohttp.ClientSession, url: str, request_id: int) -> Dict:
    """Make a single API request and measure response time."""
    start_time = time.time()
    try:
        async with session.get(url) as response:
            await response.text()  # Read the response
            end_time = time.time()
            return {
                'request_id': request_id,
                'status': response.status,
                'response_time': end_time - start_time,
                'success': response.status == 200
            }
    except Exception as e:
        end_time = time.time()
        return {
            'request_id': request_id,
            'status': 0,
            'response_time': end_time - start_time,
            'success': False,
            'error': str(e)
        }

async def intensive_stress_test(url: str, concurrent_requests: int, total_requests: int):
    """Run intensive stress test with high concurrency."""
    print(f"🔥 INTENSIVE STRESS TEST")
    print(f"   URL: {url}")
    print(f"   Concurrent requests: {concurrent_requests}")
    print(f"   Total requests: {total_requests}")
    print(f"   Workers under test: 3")
    print()
    
    results = []
    start_time = time.time()
    
    async with aiohttp.ClientSession(
        timeout=aiohttp.ClientTimeout(total=60),  # 60 second timeout
        connector=aiohttp.TCPConnector(limit=100)  # Allow more connections
    ) as session:
        
        # Create all tasks at once for maximum stress
        print(f"🚀 Launching {total_requests} requests with {concurrent_requests} concurrency...")
        
        # Create batches to avoid overwhelming the system
        batch_size = concurrent_requests
        for batch_start in range(0, total_requests, batch_size):
            batch_end = min(batch_start + batch_size, total_requests)
            batch_requests = batch_end - batch_start
            
            print(f"   📊 Batch {batch_start//batch_size + 1}: {batch_requests} requests")
            
            # Create tasks for this batch
            tasks = [
                make_request(session, url, batch_start + i) 
                for i in range(batch_requests)
            ]
            
            # Execute batch
            batch_start_time = time.time()
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            batch_end_time = time.time()
            
            # Process results
            valid_results = [r for r in batch_results if isinstance(r, dict)]
            results.extend(valid_results)
            
            batch_time = batch_end_time - batch_start_time
            batch_rps = len(valid_results) / batch_time if batch_time > 0 else 0
            
            print(f"      ⏱️  Batch completed in {batch_time:.2f}s ({batch_rps:.2f} RPS)")
            
            # Brief pause between batches to avoid overwhelming
            if batch_end < total_requests:
                await asyncio.sleep(0.5)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Analyze results
    successful_requests = [r for r in results if r.get('success', False)]
    failed_requests = [r for r in results if not r.get('success', False)]
    response_times = [r['response_time'] for r in successful_requests]
    
    print(f"\n🔥 INTENSIVE STRESS TEST RESULTS:")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Total requests: {len(results)}")
    print(f"   Successful: {len(successful_requests)}")
    print(f"   Failed: {len(failed_requests)}")
    print(f"   Success rate: {len(successful_requests)/len(results)*100:.1f}%")
    print(f"   Overall RPS: {len(results)/total_time:.2f}")
    print(f"   Successful RPS: {len(successful_requests)/total_time:.2f}")
    
    if response_times:
        print(f"\n⏱️  Response Time Analysis:")
        print(f"   Average: {statistics.mean(response_times):.2f}s")
        print(f"   Median: {statistics.median(response_times):.2f}s")
        print(f"   Min: {min(response_times):.2f}s")
        print(f"   Max: {max(response_times):.2f}s")
        print(f"   95th percentile: {sorted(response_times)[int(len(response_times)*0.95)]:.2f}s")
        print(f"   99th percentile: {sorted(response_times)[int(len(response_times)*0.99)]:.2f}s")
    
    # Performance analysis
    avg_response_time = statistics.mean(response_times) if response_times else float('inf')
    successful_rps = len(successful_requests) / total_time
    
    print(f"\n🎯 3-Worker Performance Analysis:")
    if len(failed_requests) > 0:
        print(f"   ❌ {len(failed_requests)} failed requests - workers are overloaded!")
        print(f"   🔧 Recommendation: Scale to 5-7 workers")
    elif avg_response_time > 10:
        print(f"   ⚠️  High response times ({avg_response_time:.2f}s avg) - workers struggling")
        print(f"   🔧 Recommendation: Scale to 4-5 workers")
    elif avg_response_time > 5:
        print(f"   ⚠️  Moderate response times ({avg_response_time:.2f}s avg) - approaching limits")
        print(f"   🔧 Recommendation: Consider scaling to 4 workers")
    elif successful_rps < 2:
        print(f"   🐌 Low throughput ({successful_rps:.2f} RPS) - workers at capacity")
        print(f"   🔧 Recommendation: Scale to 4-5 workers for better performance")
    else:
        print(f"   ✅ Good performance! 3 workers handling load well")
        print(f"   📈 Throughput: {successful_rps:.2f} RPS")
    
    return {
        'total_time': total_time,
        'successful_requests': len(successful_requests),
        'failed_requests': len(failed_requests),
        'avg_response_time': avg_response_time,
        'successful_rps': successful_rps
    }

async def main():
    """Run escalating stress tests."""
    base_url = "http://localhost:8000/api/test/shantanu"
    
    stress_scenarios = [
        {"name": "Moderate Stress", "concurrent": 15, "total": 75},
        {"name": "High Stress", "concurrent": 25, "total": 100},
        {"name": "Extreme Stress", "concurrent": 50, "total": 150},
    ]
    
    for scenario in stress_scenarios:
        print(f"\n{'='*70}")
        print(f"🔥 {scenario['name']} - Testing 3 Workers")
        print('='*70)
        
        await intensive_stress_test(
            url=base_url,
            concurrent_requests=scenario['concurrent'],
            total_requests=scenario['total']
        )
        
        print(f"\n⏸️  Cooling down for 10 seconds...")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(main())
