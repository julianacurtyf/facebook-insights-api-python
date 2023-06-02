from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class ormbase(BaseModel):
    class Config:
        orm_model = True

class Actions(ormbase):
    action_type: str
    value: Optional[str] = "0"
    _1d_view: Optional[str] = "0"
    _7d_click: Optional[str] = "0"

class VideoP50(ormbase):
    action_type: str = Field("video_p50_watched_actions")
    value: Optional[str] = "0"
    _1d_view: Optional[str] = "0"
    _7d_click: Optional[str] = "0"

class VideoP75(ormbase):
    action_type: str = Field("video_p75_watched_actions")
    value: Optional[str] = "0"
    _1d_view: Optional[str] = "0"
    _7d_click: Optional[str] = "0"

class VideoP95(ormbase):
    action_type: str = Field("video_p95_watched_actions")
    value: Optional[str] = "0"
    _1d_view: Optional[str] = "0"
    _7d_click: Optional[str] = "0"

class Data(ormbase):
    account_name: str
    account_id: str
    campaign_name: str
    campaign_id: str
    adset_name: str
    adset_id: str
    ad_name: str
    ad_id: str
    reach: Optional[str] = "0"
    impressions: Optional[str] = "0"
    clicks: Optional[str] = "0"
    ctr: Optional[str] = "0"
    cpc: Optional[str] = "0"
    spend: Optional[str] = "0"
    cpm: Optional[str] = "0"
    conversions: Optional[str] = "0"
    video_p50_watched_actions: Optional[VideoP50] = None
    video_p75_watched_actions: Optional[VideoP75] = None
    video_p95_watched_actions: Optional[VideoP95] = None
    frequency: Optional[str] = "0"
    actions: Optional[List[Actions]]
    date_start: str
    date_stop: str
    objective:  Optional[str] = ""
    updated_time: Optional[datetime] = Field(datetime.now())
    created_time: Optional[datetime] = Field(datetime.now())
    insight_id:  Optional[str] = Field(uuid.uuid4())


class DataVal(ormbase):
    
    df_dict: List[Data]

