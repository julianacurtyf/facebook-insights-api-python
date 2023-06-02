from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship



from database import Base

class Accounts(Base):
    """Modelo da tabela de contas com os dados do facebook. \n
    """

    __tablename__ = "accounts"
    account_id = Column(String(191), primary_key=True)
    name = Column(String(191))

    
class Campaings(Base):
    """Modelo da tabela de campanhas com os dados do facebook. \n """

    __tablename__ = "campaign"
    campaign_id = Column(String(191), primary_key=True)
    name = Column(String(191))
    account_id = Column(String(191))
    objective = Column(String(191))

class AdSets(Base):
    """Modelo da tabela de conjuntos de anúncios com os dados do facebook. \n """

    __tablename__ = "adsets" 
    adset_id = Column(String(191), primary_key=True)
    name = Column(String(191))
    campaign_id = Column(String(191))


class Ads(Base):
    """Modelo da tabela de anúncios com os dados do facebook. \n """

    __tablename__ = "ads"
    id = Column(String(191), primary_key=True)
    insight_id = Column(String(191))
    ad_id = Column(String(191))
    name = Column(String(191))
    ad_sets_id = Column(String(191))
    created_time = Column(DateTime)
    updated_time = Column(DateTime)
    start_time = Column(DateTime)
    stop_time = Column(DateTime)
    reach = Column(Integer)
    impressions = Column(Integer)
    cpm = Column(Float)
    cpc = Column(Float)
    clicks = Column(Integer)
    frequency = Column(Float)
    ctr = Column(Float)
    conversions = Column(Integer)  
    spend = Column(Float)
    cpl = Column(Float)
    leads = Column(Integer) 


class Actions(Base):
    """Modelo da tabela de actions com os dados do facebook. \n """

    __tablename__ = "actions"
    id = Column(String(191), primary_key=True)
    action_type = Column(String(191))
    value = Column(Integer)
    _1d_view = Column(Integer)
    _7d_click = Column(Integer)
    ad_id = Column(String(191))
    insight_id = Column(String(191))

