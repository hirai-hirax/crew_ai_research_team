"""Google Maps API tools for accurate travel time and route information."""

import os
from datetime import datetime
from typing import Optional, Type

import googlemaps
from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class GoogleMapsDirectionsInput(BaseModel):
    """Input schema for GoogleMapsDirectionsTool."""
    
    origin: str = Field(
        ...,
        description="出発地点の住所または地名（例: '東京駅', '渋谷区恵比寿1-1-1'）"
    )
    destination: str = Field(
        ...,
        description="目的地の住所または地名（例: '横浜駅', '品川区大井1-2-3'）"
    )
    mode: str = Field(
        default="transit",
        description="移動手段: 'driving'(自動車), 'transit'(公共交通機関), 'walking'(徒歩), 'bicycling'(自転車)"
    )
    departure_time: Optional[str] = Field(
        default=None,
        description="出発時刻（ISO形式: '2025-11-23T09:00:00' または 'now'）。指定しない場合は現在時刻"
    )


class GoogleMapsDistanceMatrixInput(BaseModel):
    """Input schema for GoogleMapsDistanceMatrixTool."""
    
    origin: str = Field(
        ...,
        description="出発地点の住所または地名"
    )
    destination: str = Field(
        ...,
        description="目的地の住所または地名"
    )
    departure_time: Optional[str] = Field(
        default=None,
        description="出発時刻（ISO形式 または 'now'）"
    )


class GoogleMapsDirectionsTool(BaseTool):
    """
    Google Maps Directions APIを使用して、詳細な経路情報を取得するツール。
    
    自動車、公共交通機関、徒歩、自転車の経路を検索し、
    所要時間、距離、詳細なステップバイステップの案内、
    公共交通機関の場合は乗り換え情報や運賃も取得します。
    """
    
    name: str = "Google Maps経路検索"
    description: str = (
        "出発地から目的地までの詳細な経路情報を取得します。"
        "自動車、公共交通機関、徒歩、自転車の移動手段をサポートします。"
        "所要時間、距離、乗り換え情報、運賃情報を含む詳細な経路を返します。"
    )
    args_schema: Type[BaseModel] = GoogleMapsDirectionsInput
    
    def _run(
        self,
        origin: str,
        destination: str,
        mode: str = "transit",
        departure_time: Optional[str] = None,
    ) -> str:
        """
        経路情報を取得して整形された文字列として返します。
        
        Args:
            origin: 出発地点
            destination: 目的地
            mode: 移動手段
            departure_time: 出発時刻
            
        Returns:
            整形された経路情報の文字列
        """
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            return "エラー: GOOGLE_MAPS_API_KEY環境変数が設定されていません。"
        
        try:
            gmaps = googlemaps.Client(key=api_key)
            
            # 出発時刻の処理
            if departure_time:
                if departure_time.lower() == "now":
                    dep_time = datetime.now()
                else:
                    dep_time = datetime.fromisoformat(departure_time)
            else:
                dep_time = datetime.now()
            
            # Directions APIを呼び出し
            directions = gmaps.directions(
                origin=origin,
                destination=destination,
                mode=mode,
                departure_time=dep_time,
                language="ja",
                alternatives=True,  # 代替ルートも取得
            )
            
            if not directions:
                return f"エラー: {origin}から{destination}への経路が見つかりませんでした。"
            
            # 結果を整形
            result_text = f"# {origin} → {destination} の経路情報\n\n"
            result_text += f"**移動手段**: {self._get_mode_name(mode)}\n"
            result_text += f"**出発時刻**: {dep_time.strftime('%Y年%m月%d日 %H:%M')}\n\n"
            
            # 各ルートを処理（最大3つ）
            for idx, route in enumerate(directions[:3], 1):
                leg = route['legs'][0]
                
                result_text += f"## ルート {idx}\n\n"
                result_text += f"- **所要時間**: {leg['duration']['text']}\n"
                result_text += f"- **距離**: {leg['distance']['text']}\n"
                
                # 渋滞を考慮した時間（自動車の場合）
                if mode == "driving" and 'duration_in_traffic' in leg:
                    result_text += f"- **渋滞時の所要時間**: {leg['duration_in_traffic']['text']}\n"
                
                # 公共交通機関の場合の詳細情報
                if mode == "transit":
                    result_text += f"\n### 乗り換え詳細\n\n"
                    
                    total_fare = 0
                    for step_idx, step in enumerate(leg['steps'], 1):
                        if step['travel_mode'] == 'TRANSIT':
                            transit = step['transit_details']
                            line = transit['line']
                            
                            result_text += f"{step_idx}. **{line['vehicle']['name']}** "
                            result_text += f"({line.get('short_name', line['name'])})\n"
                            result_text += f"   - 乗車: {transit['departure_stop']['name']}\n"
                            result_text += f"   - 下車: {transit['arrival_stop']['name']}\n"
                            result_text += f"   - 停車駅数: {transit['num_stops']}駅\n"
                            
                            # 運賃情報
                            if 'fare' in step:
                                fare = step['fare']['value']
                                total_fare += fare
                                result_text += f"   - 運賃: {fare}円\n"
                            
                            result_text += "\n"
                        elif step['travel_mode'] == 'WALKING':
                            result_text += f"{step_idx}. 徒歩: {step['duration']['text']} ({step['distance']['text']})\n\n"
                    
                    if total_fare > 0:
                        result_text += f"**合計運賃**: 約{total_fare}円\n"
                
                result_text += "\n"
            
            return result_text
            
        except googlemaps.exceptions.ApiError as e:
            return f"Google Maps APIエラー: {str(e)}"
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"
    
    def _get_mode_name(self, mode: str) -> str:
        """移動手段の日本語名を取得"""
        mode_names = {
            "driving": "自動車",
            "transit": "公共交通機関",
            "walking": "徒歩",
            "bicycling": "自転車",
        }
        return mode_names.get(mode, mode)


class GoogleMapsDistanceMatrixTool(BaseTool):
    """
    Google Maps Distance Matrix APIを使用して、
    複数の移動手段を一度に比較するツール。
    """
    
    name: str = "Google Maps複数手段比較"
    description: str = (
        "出発地から目的地までの所要時間と距離を、"
        "複数の移動手段（自動車、公共交通機関、徒歩）で一度に比較します。"
        "最適な移動手段を選択するのに役立ちます。"
    )
    args_schema: Type[BaseModel] = GoogleMapsDistanceMatrixInput
    
    def _run(
        self,
        origin: str,
        destination: str,
        departure_time: Optional[str] = None,
    ) -> str:
        """
        複数の移動手段の所要時間を比較して返します。
        
        Args:
            origin: 出発地点
            destination: 目的地
            departure_time: 出発時刻
            
        Returns:
            整形された比較表
        """
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            return "エラー: GOOGLE_MAPS_API_KEY環境変数が設定されていません。"
        
        try:
            gmaps = googlemaps.Client(key=api_key)
            
            # 出発時刻の処理
            if departure_time:
                if departure_time.lower() == "now":
                    dep_time = datetime.now()
                else:
                    dep_time = datetime.fromisoformat(departure_time)
            else:
                dep_time = datetime.now()
            
            result_text = f"# {origin} → {destination} の移動手段比較\n\n"
            result_text += f"**出発時刻**: {dep_time.strftime('%Y年%m月%d日 %H:%M')}\n\n"
            result_text += "| 移動手段 | 所要時間 | 距離 | 備考 |\n"
            result_text += "|---------|---------|------|------|\n"
            
            # 各移動手段で取得
            modes = [
                ("driving", "自動車"),
                ("transit", "公共交通機関"),
                ("walking", "徒歩"),
            ]
            
            for mode, mode_name in modes:
                try:
                    matrix = gmaps.distance_matrix(
                        origins=[origin],
                        destinations=[destination],
                        mode=mode,
                        departure_time=dep_time,
                        language="ja",
                    )
                    
                    if matrix['rows'][0]['elements'][0]['status'] == 'OK':
                        element = matrix['rows'][0]['elements'][0]
                        duration = element['duration']['text']
                        distance = element['distance']['text']
                        
                        # 自動車の場合は渋滞情報も
                        note = ""
                        if mode == "driving" and 'duration_in_traffic' in element:
                            traffic_duration = element['duration_in_traffic']['text']
                            note = f"渋滞時: {traffic_duration}"
                        
                        result_text += f"| {mode_name} | {duration} | {distance} | {note} |\n"
                    else:
                        result_text += f"| {mode_name} | 利用不可 | - | - |\n"
                        
                except Exception as e:
                    result_text += f"| {mode_name} | エラー | - | {str(e)} |\n"
            
            result_text += "\n**推奨**: より詳細な情報が必要な場合は、Google Maps経路検索ツールを使用してください。\n"
            
            return result_text
            
        except googlemaps.exceptions.ApiError as e:
            return f"Google Maps APIエラー: {str(e)}"
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"
