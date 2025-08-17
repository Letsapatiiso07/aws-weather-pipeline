import json
import boto3
import urllib.request
import urllib.parse
from datetime import datetime
from decimal import Decimal
import os

def lambda_handler(event, context):
    """
    AWS Lambda function to collect weather data from OpenWeatherMap API
    and store it in both S3 (raw data) and DynamoDB (structured data).
    
    Triggered by EventBridge every 15 minutes to collect real-time weather
    data from major South African cities.
    """
    print("Starting weather data collection...")
    
    try:
        # Initialize AWS clients
        s3 = boto3.client('s3')
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('WeatherData')
        
        # Get configuration from environment variables
        api_key = os.environ.get('WEATHER_API_KEY')
        bucket_name = os.environ.get('S3_BUCKET_NAME')
        
        print(f"API Key exists: {bool(api_key)}")
        print(f"Bucket name: {bucket_name}")
        
        if not api_key:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing WEATHER_API_KEY environment variable'})
            }
        if not bucket_name:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing S3_BUCKET_NAME environment variable'})
            }
        
        # Cities to collect data from (URL encoded for API calls)
        cities = ['Pretoria', 'Cape%20Town', 'Johannesburg', 'Durban']
        city_display = ['Pretoria', 'Cape Town', 'Johannesburg', 'Durban']
        results = []
        
        # Process each city
        for i, city in enumerate(cities):
            try:
                display_name = city_display[i]
                print(f"Processing city: {display_name}")
                
                # Construct API URL
                url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
                
                # Fetch weather data from API
                with urllib.request.urlopen(url) as response:
                    data = json.loads(response.read().decode())
                
                current_temp = data.get('main', {}).get('temp', 'N/A')
                print(f"Got weather data for {display_name}: {current_temp}°C")
                
                # Add metadata
                timestamp = datetime.now().isoformat()
                data['timestamp'] = timestamp
                data['city'] = display_name
                
                # Store raw data in S3
                safe_city = display_name.replace(' ', '_')
                s3_key = f"raw-data/{safe_city}/{datetime.now().strftime('%Y/%m/%d')}/{timestamp}.json"
                
                s3.put_object(
                    Bucket=bucket_name,
                    Key=s3_key,
                    Body=json.dumps(data, indent=2),
                    ContentType='application/json',
                    Metadata={
                        'city': display_name,
                        'collection_time': timestamp,
                        'data_source': 'openweathermap'
                    }
                )
                print(f"Stored in S3: {s3_key}")
                
                # Store structured data in DynamoDB (convert floats to Decimal for DynamoDB)
                table.put_item(
                    Item={
                        'city': display_name,
                        'timestamp': timestamp,
                        'temperature': Decimal(str(data['main']['temp'])),
                        'humidity': Decimal(str(data['main']['humidity'])),
                        'pressure': Decimal(str(data['main']['pressure'])),
                        'weather_condition': data['weather'][0]['main'],
                        'weather_description': data['weather'][0]['description'],
                        'wind_speed': Decimal(str(data['wind']['speed'])),
                        'visibility': Decimal(str(data.get('visibility', 0))),
                        'cloudiness': Decimal(str(data['clouds']['all'])),
                        'country': data['sys']['country'],
                        'sunrise': Decimal(str(data['sys']['sunrise'])),
                        'sunset': Decimal(str(data['sys']['sunset']))
                    }
                )
                print(f"Stored in DynamoDB for {display_name}")
                
                results.append({
                    'city': display_name,
                    'status': 'success',
                    'timestamp': timestamp,
                    'temperature': current_temp
                })
                
            except Exception as e:
                error_msg = str(e)
                print(f"Error processing {display_name}: {error_msg}")
                results.append({
                    'city': display_name,
                    'status': 'error',
                    'error': error_msg
                })
        
        # Calculate success metrics
        successful_cities = [r for r in results if r['status'] == 'success']
        success_rate = len(successful_cities) / len(results) * 100
        
        print(f"Completed processing {len(results)} cities")
        print(f"Success rate: {success_rate:.1f}% ({len(successful_cities)}/{len(results)})")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Weather data collection completed',
                'processed_cities': len(results),
                'successful_cities': len(successful_cities),
                'success_rate': f"{success_rate:.1f}%",
                'execution_time': datetime.now().isoformat(),
                'results': results
            }, indent=2)
        }
        
    except Exception as e:
        error_msg = str(e)
        print(f"Fatal error in weather data collection: {error_msg}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Fatal error in weather data collection',
                'details': error_msg,
                'execution_time': datetime.now().isoformat()
            }, indent=2)
        }


# Test function for local development
if __name__ == "__main__":
    # Mock event for testing
    test_event = {}
    test_context = {}
    
    # Note: Set environment variables for local testing
    # os.environ['WEATHER_API_KEY'] = 'your_api_key_here'
    # os.environ['S3_BUCKET_NAME'] = 'your_bucket_name_here'
    
    result = lambda_handler(test_event, test_context)
    print("Test result:", json.dumps(result, indent=2)) 
