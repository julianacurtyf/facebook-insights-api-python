from sqlalchemy.orm import Session
from sqlalchemy import update

import models
import schema
import uuid

def get_account(db: Session, account_id: str):
    """ Get the account from the database
    
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session
            
            account_id: str
                account id

        Returns
        -------
            models.Accounts
    """

    return db.query(models.Accounts).filter(models.Accounts.id == account_id).first()

def get_campaign(db: Session, campaign_id: str):
    """ Get the campaign from the database
    
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session
            
            campaign_id: str
                campaign id
                
        Returns
        -------
            models.Campaings
    """

    return db.query(models.Campaings).filter(models.Campaings.id == campaign_id).first()

def get_adset(db: Session, adset_id: str):
    """ Get the adset from the database
        
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session
            
            adset_id: str
                adset id
                
        Returns
        -------
            models.Adsets
    """
    return db.query(models.Adsets).filter(models.Adsets.id == adset_id).first()

def get_ad(db: Session, ad_id: str):
    """ Get the ad from the database
        
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session
            
            ad_id: str
                ad id
                
        Returns
        -------
            models.Ads
    """
    return db.query(models.Ads).filter(models.Ads.id == ad_id).first()

def get_data(db: Session, data_id: str):
    """ Get the data from the database
            
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session
            
            data_id: str
                data id
                
        Returns
        -------
            models.Data
    """
    return db.query(models.Data).filter(models.Data.id == data_id).first()

def create_account(db: Session, schema: schema.Data):
    """ Create the a new account in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
    
    new_account = models.Accounts(
        account_id = schema.account_id,
        name = schema.account_name)

    db.add(new_account)
    db.commit()

def create_campaign(db: Session, schema: schema.Data):
    """ Create the a new campaign in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
    new_campaign = models.Campaings(
        campaign_id = schema.campaign_id,
        name = schema.campaign_name,
        account_id = schema.account_id,
        objective = schema.objective,
        )

    db.add(new_campaign)
    db.commit()

def create_adset(db: Session, schema: schema.Data):
    """ Create the a new adset in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
        
    new_adset = models.AdSets(
        adset_id = schema.adset_id,
        name = schema.adset_name,
        campaign_id = schema.campaign_id,
        )

    db.add(new_adset)
    db.commit()

def create_ad(db: Session, schema: schema.Data):
    """ Create the a new ad in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
    
    list_actions = schema.actions 
    
    cpl = 0
    leads = 0
    
    if schema.objective == "OUTCOME_LEADS" or schema.objective=="CONVERSIONS": # check the objective of the campaign and calculate the cpl and leads
        if list_actions:
            for action in list_actions:
                if action.action_type == "lead":
                    cpl = float(schema.spend)/float(action.value)
                    leads = action.value
        if cpl == 0:
            cpl = schema.spend


    new_ad = models.Ads(
        id = uuid.uuid4(),
        ad_id = schema.ad_id,
        name = schema.ad_name,
        ad_sets_id = schema.adset_id,
        start_time = schema.date_start,
        stop_time = schema.date_stop,
        created_time = schema.created_time,
        updated_time = schema.updated_time,
        reach = schema.reach,
        impressions = schema.impressions,
        cpm = schema.cpm,
        cpc = schema.cpc,
        clicks = schema.clicks,
        frequency = schema.frequency,
        ctr = schema.ctr,
        conversions = schema.conversions,
        insight_id = schema.insight_id,
        spend = schema.spend,
        cpl = cpl,
        leads=leads)


    db.add(new_ad)
    db.commit()

def create_action(db: Session, schema: schema.Data):
    """ Create the a new action in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
    
    list_actions = schema.actions 
    
    if list_actions: # check if the list of actions is not empty
        for action in list_actions: # iterate over the list of actions
        
            new_action = models.Actions(
                id = uuid.uuid4(),
                ad_id = schema.ad_id,
                action_type = action.action_type,
                value = action.value,
                _1d_view = action._1d_view,
                _7d_click = action._7d_click,
                insight_id = schema.insight_id
            )
        
            db.add(new_action)
            
        db.commit()

def create_action_v50(db: Session, schema: schema.Data):
    """ Create the a new action "video_p50_watched_actions" in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
    
    action = schema.video_p50_watched_actions
    
    if action: # check if the action is not empty
        new_action = models.Actions(
            id = uuid.uuid4(),
            ad_id = schema.ad_id,
            action_type = "video_p50_watched_actions",
            value = action.value,
            _1d_view = action._1d_view,
            _7d_click = action._7d_click,
            insight_id = schema.insight_id)
    
        db.add(new_action)
        db.commit()

def create_action_v75(db: Session, schema: schema.Data):

    """ Create the a new action "video_p75_watched_actions" in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
    
    action = schema.video_p75_watched_actions
    
    if action: # check if the action is not empty
        new_action = models.Actions(
            id = uuid.uuid4(),
            ad_id = schema.ad_id,
            action_type = "video_p75_watched_actions",
            value = action.value,
            _1d_view = action._1d_view,
            _7d_click = action._7d_click,
            insight_id = schema.insight_id)
    
        db.add(new_action)
        db.commit()

def create_action_v95(db: Session, schema: schema.Data):

    """ Create the a new action "video_p95_watched_actions" in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
    
    action = schema.video_p95_watched_actions
    
    if action: # check if the action is not empty
        new_action = models.Actions(
            id = uuid.uuid4(),
            ad_id = schema.ad_id,
            action_type =  "video_p95_watched_actions",
            value = action.value,
            _1d_view = action._1d_view,
            _7d_click = action._7d_click,
            insight_id = schema.insight_id)
    
        db.add(new_action)
        db.commit()

def update_ad_and_actions(db: Session, schema: schema.Data):
    """ Update the ad and actions in the database
   
    
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """

    db.execute(update(models.Ads).where((models.Ads.ad_id == schema.ad_id) & (models.Ads.start_time == schema.date_start) & (models.Ads.stop_time == schema.date_stop)).values( 
                            updated_time = schema.updated_time,
                            reach = schema.reach,
                            impressions = schema.impressions,
                            cpm = schema.cpm,
                            cpc = schema.cpc,
                            clicks = schema.clicks,
                            frequency = schema.frequency,
                            ctr = schema.ctr,
                            conversions = schema.conversions
                            ))
                      
    list_actions = schema.actions # get the list of actions
        
    if list_actions: # check if the list of actions is not empty
        for action in list_actions: # iterate over the list of actions
            db.execute(update(models.Actions).where((models.Actions.ad_id == schema.ad_id) & (models.Actions.insight_id == schema.insight_id) & (models.Actions.action_type == action.action_type)).values(
                value = action.value,
                _1d_view = action._1d_view,
                _7d_click = action._7d_click
                ))
    
    action50 = schema.video_p50_watched_actions # get the action video_p50_watched_actions
    
    if action50: # check if the action is not empty
        db.execute(update(models.Actions).where((models.Actions.ad_id == schema.ad_id) & (models.Actions.insight_id == schema.insight_id) & (models.Actions.action_type == "video_p50_watched_actions")).values(
                value = action50.value,
                _1d_view = action50._1d_view,
                _7d_click = action50._7d_click
                ))
        
    action75 = schema.video_p75_watched_actions # get the action video_p75_watched_actions
    
    if action75: # check if the action is not empty
        db.execute(update(models.Actions).where((models.Actions.ad_id == schema.ad_id) & (models.Actions.insight_id == schema.insight_id) & (models.Actions.action_type == "video_p75_watched_actions")).values(
                value = action75.value,
                _1d_view = action75._1d_view,
                _7d_click = action75._7d_click
                ))
        
    action95 = schema.video_p95_watched_actions # get the action video_p95_watched_actions
    
    if action95: # check if the action is not empty
        db.execute(update(models.Actions).where((models.Actions.ad_id == schema.ad_id) & (models.Actions.insight_id == schema.insight_id) & (models.Actions.action_type == "video_p95_watched_actions")).values(
                    value = action95.value,
                    _1d_view = action95._1d_view,
                    _7d_click = action95._7d_click
                    ))

    db.commit()

def create_ad_and_actions(db: Session, schema: schema.Data):
    """ Create the a new ad and actions in the database
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """

    create_ad(db, schema)
    create_action(db, schema)
    create_action_v50(db, schema)
    create_action_v75(db, schema)
    create_action_v95(db, schema)

def upsert_event(db: Session, schema: schema.Data):
    """ Upsert the event in the database.
        1. Check if the event exists
        2. If the event exists, update the insight values and the actions
        3. If the event does not exist, creates a new event using the one of the functions to create events. Namely, create_ad, 
        create_action, create_action_v50, create_action_v75, create_action_v95, create_campaign, create_adset, create_account.
   
        Parameters
        ----------
            db: sqlalchemy.orm.Session
                database session  
            schema: models.Data
                schema of the data
    
    """
    
    try:
        ad  = db.query(models.Ads).filter((models.Ads.ad_id == schema.ad_id) & (models.Ads.start_time == schema.date_start) & (models.Ads.stop_time == schema.date_stop)).first()
        campaign = db.query(models.Campaings).filter(models.Campaings.campaign_id == schema.campaign_id).first()
        adset = db.query(models.AdSets).filter(models.AdSets.adset_id == schema.adset_id).first()
        account = db.query(models.Accounts).filter(models.Accounts.account_id == schema.account_id).first()


        if account: # se a conta já existe, vê se a campanha existe
            if campaign: # se a campanha já existe, vê se o adset existe
                if adset: # se o adset já existe, vê se o ad existe
                    if ad: # se o ad já existe, atualiza os valores
                        
                        update_ad_and_actions(db, schema)
                        return print(f'Ad: {schema.ad_id} already exists on this date.')
                        
                    else: # se o ad não existe, cria o ad e as actions
                        create_ad_and_actions(db, schema)
                        return print(f'Ad: {schema.ad_id} created.')
                    
                else: # se o adset não existe, cria o adset, o ad e as actions
                    create_adset(db, schema)
                    create_ad_and_actions(db, schema)
                    return print(f'Adset: {schema.adset_id} created.')

            else: # se a campanha não existe, cria a campanha, o adset, o ad e as actions
                create_campaign(db, schema)
                create_adset(db, schema)
                create_ad_and_actions(db, schema)
                return print(f'Campaign: {schema.campaign_id} created.')

        else: # se a conta não existe, cria a conta, a campanha, o adset, o ad e as actions
            create_account(db, schema)
            create_campaign(db, schema)
            create_adset(db, schema)
            create_ad_and_actions(db, schema)

            return print(f'Account: {schema.account_id} created.')

       
    
    except Exception as e:
        return print(e)
    
    finally:
        db.close()
            