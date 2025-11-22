"""
Open-Meteo API Tool for CrewAI
Provides weather forecast data for specified locations and dates.
No API key required - completely free!
"""

from datetime import datetime, timedelta
from typing import Optional, Type
import requests
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class OpenMeteoToolInput(BaseModel):
    """Input schema for OpenMeteoTool."""
    location: str = Field(..., description="Location name (e.g., '東京', 'Tokyo', '渋谷区')")
    date: Optional[str] = Field(None, description="Date for forecast in YYYY-MM-DD format. If not provided, uses current date.")


class OpenMeteoTool(BaseTool):
    name: str = "天気予報取得"
    description: str = (
        "Open-Meteo APIを使用して、指定された場所の天気予報を取得します。"
        "現在の天気、7日間の予報、気温、湿度、風速、降水確率などの詳細情報を提供します。"
        "APIキー不要で完全無料です。"
    )
    args_schema: Type[BaseModel] = OpenMeteoToolInput

    def _get_weather_description(self, weather_code: int) -> str:
        """
        Convert WMO Weather interpretation codes to Japanese description.
        
        Args:
            weather_code: WMO weather code (0-99)
            
        Returns:
            Japanese weather description
        """
        weather_codes = {
            0: "快晴",
            1: "晴れ",
            2: "一部曇り",
            3: "曇り",
            45: "霧",
            48: "霧氷",
            51: "小雨",
            53: "雨",
            55: "強い雨",
            56: "凍雨（弱）",
            57: "凍雨（強）",
            61: "弱い雨",
            63: "雨",
            65: "強い雨",
            66: "凍った雨（弱）",
            67: "凍った雨（強）",
            71: "弱い雪",
            73: "雪",
            75: "強い雪",
            77: "みぞれ",
            80: "にわか雨（弱）",
            81: "にわか雨",
            82: "にわか雨（強）",
            85: "にわか雪（弱）",
            86: "にわか雪（強）",
            95: "雷雨",
            96: "雷雨と雹（弱）",
            99: "雷雨と雹（強）"
        }
        return weather_codes.get(weather_code, f"不明({weather_code})")

    def _run(self, location: str, date: Optional[str] = None) -> str:
        """
        Get weather forecast for a specified location and date.
        
        Args:
            location: Location name (e.g., '東京', 'Tokyo')
            date: Target date in YYYY-MM-DD format (optional)
            
        Returns:
            Formatted weather forecast information
        """
        try:
            # Get coordinates for the location using Open-Meteo Geocoding API
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_params = {
                "name": location,
                "count": 1,
                "language": "ja",
                "format": "json"
            }
            
            geo_response = requests.get(geo_url, params=geo_params, timeout=10)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if not geo_data.get("results"):
                return f"エラー: '{location}'の位置情報が見つかりませんでした。別の地名をお試しください。"
            
            result = geo_data["results"][0]
            lat = result["latitude"]
            lon = result["longitude"]
            location_name = result.get("name", location)
            country = result.get("country", "")
            admin1 = result.get("admin1", "")
            
            # Format location name with region info
            display_location = location_name
            if admin1 and admin1 != location_name:
                display_location = f"{location_name}（{admin1}）"
            if country:
                display_location = f"{display_location}, {country}"
            
            # Parse target date
            if date:
                try:
                    target_date = datetime.strptime(date, "%Y-%m-%d").date()
                except ValueError:
                    target_date = datetime.now().date()
            else:
                target_date = datetime.now().date()
            
            # Get weather forecast from Open-Meteo
            forecast_url = "https://api.open-meteo.com/v1/forecast"
            forecast_params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,weather_code",
                "timezone": "Asia/Tokyo",
                "forecast_days": 7
            }
            
            forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            # Find data for target date
            daily_data = forecast_data.get("daily", {})
            daily_times = daily_data.get("time", [])
            
            target_date_str = target_date.strftime("%Y-%m-%d")
            
            if target_date_str not in daily_times:
                return f"エラー: {target_date}の予報データが見つかりませんでした（予報は7日先までです）。"
            
            day_index = daily_times.index(target_date_str)
            
            # Get daily summary
            max_temp = daily_data.get("temperature_2m_max", [])[day_index]
            min_temp = daily_data.get("temperature_2m_min", [])[day_index]
            rain_prob = daily_data.get("precipitation_probability_max", [])[day_index]
            daily_weather_code = daily_data.get("weather_code", [])[day_index]
            main_weather = self._get_weather_description(daily_weather_code)
            
            # Format the output
            result_text = f"# 天気予報: {display_location}\n"
            result_text += f"**日付:** {target_date.strftime('%Y年%m月%d日')}\n\n"
            
            result_text += f"## 概要\n"
            result_text += f"- **天気:** {main_weather}\n"
            result_text += f"- **最高気温:** {max_temp:.1f}°C\n"
            result_text += f"- **最低気温:** {min_temp:.1f}°C\n"
            result_text += f"- **降水確率:** {rain_prob}%\n\n"
            
            # Get hourly details for target date
            hourly_data = forecast_data.get("hourly", {})
            hourly_times = hourly_data.get("time", [])
            
            result_text += f"## 時間帯別予報\n"
            
            for i, time_str in enumerate(hourly_times):
                forecast_datetime = datetime.fromisoformat(time_str)
                if forecast_datetime.date() == target_date:
                    time_display = forecast_datetime.strftime("%H:%M")
                    temp = hourly_data.get("temperature_2m", [])[i]
                    humidity = hourly_data.get("relative_humidity_2m", [])[i]
                    wind_speed = hourly_data.get("wind_speed_10m", [])[i]
                    weather_code = hourly_data.get("weather_code", [])[i]
                    weather_desc = self._get_weather_description(weather_code)
                    precip_prob = hourly_data.get("precipitation_probability", [])[i]
                    
                    result_text += f"\n### {time_display}\n"
                    result_text += f"- 天気: {weather_desc}\n"
                    result_text += f"- 気温: {temp:.1f}°C\n"
                    result_text += f"- 湿度: {humidity}%\n"
                    result_text += f"- 風速: {wind_speed:.1f} m/s\n"
                    result_text += f"- 降水確率: {precip_prob}%\n"
            
            # Recommendations
            result_text += f"\n## お出かけアドバイス\n"
            
            if rain_prob > 50:
                result_text += "- ⚠️ 降水確率が高いです。傘や雨具を必ず持参してください。\n"
                result_text += "- 屋内施設を中心としたプランをおすすめします。\n"
            elif rain_prob > 20:
                result_text += "- 折りたたみ傘を持参することをおすすめします。\n"
            
            if max_temp > 30:
                result_text += "- 🌡️ 暑い日です。水分補給と熱中症対策をしっかりと。\n"
                result_text += "- 日焼け止め、帽子、サングラスの持参をおすすめします。\n"
            elif max_temp < 10:
                result_text += "- 🧥 寒い日です。暖かい服装で出かけてください。\n"
                result_text += "- カイロやマフラーなどの防寒具があると良いでしょう。\n"
            elif min_temp < 15 and max_temp > 20:
                result_text += "- 👕 寒暖差があります。調整しやすい服装（上着など）がおすすめです。\n"
            
            return result_text
            
        except requests.exceptions.RequestException as e:
            return f"エラー: 天気情報の取得に失敗しました。{str(e)}"
        except Exception as e:
            return f"エラー: {str(e)}"


# For testing
if __name__ == "__main__":
    tool = OpenMeteoTool()
    print(tool._run("東京", "2025-11-22"))
