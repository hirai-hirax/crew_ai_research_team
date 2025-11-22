"""Test script for Google Maps tools."""

import os
from tools.google_maps_tool import GoogleMapsDirectionsTool, GoogleMapsDistanceMatrixTool


def test_distance_matrix():
    """Test the Distance Matrix tool."""
    print("=" * 60)
    print("Testing Google Maps Distance Matrix Tool")
    print("=" * 60)
    
    tool = GoogleMapsDistanceMatrixTool()
    result = tool._run(
        origin="東京駅",
        destination="横浜駅",
        departure_time="now"
    )
    print(result)
    print()


def test_directions_transit():
    """Test the Directions tool with public transit."""
    print("=" * 60)
    print("Testing Google Maps Directions Tool - Public Transit")
    print("=" * 60)
    
    tool = GoogleMapsDirectionsTool()
    result = tool._run(
        origin="東京駅",
        destination="横浜駅",
        mode="transit",
        departure_time="now"
    )
    print(result)
    print()


def test_directions_driving():
    """Test the Directions tool with driving."""
    print("=" * 60)
    print("Testing Google Maps Directions Tool - Driving")
    print("=" * 60)
    
    tool = GoogleMapsDirectionsTool()
    result = tool._run(
        origin="東京駅",
        destination="横浜駅",
        mode="driving",
        departure_time="now"
    )
    print(result)
    print()


if __name__ == "__main__":
    # Check if API key is set
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("⚠️  GOOGLE_MAPS_API_KEY環境変数が設定されていません。")
        print("    .envファイルにAPIキーを設定してから実行してください。")
        exit(1)
    
    print("✓ Google Maps API Key detected")
    print()
    
    # Run tests
    try:
        test_distance_matrix()
        test_directions_transit()
        test_directions_driving()
        
        print("=" * 60)
        print("✓ All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print("=" * 60)
        print(f"✗ Error occurred: {str(e)}")
        print("=" * 60)
        exit(1)
