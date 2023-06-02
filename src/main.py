from fastapi import FastAPI, Depends
import uvicorn
import http
import models
import schema
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from crud import upsert_event
import requests
from pydantic import ValidationError
from datetime import datetime, timedelta
import time

models.Base.metadata.create_all(bind=engine)

# poolo-data-driven:us-central1:hook
app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post('/get_insights/', status_code=http.HTTPStatus.ACCEPTED)
def get_insights(account_id: str, token: str, db: Session = Depends(get_db)):

    """"Gets the insights of the previous day from the Facebook API and inserts them into the database.
       
        Parameters
        ----------
            account_id: string
                Facebook account id 

            token: string
                Facebook token to validate the access

            db: sqlalchemy.orm.Session
                Database session
                   
        Returns
        -------
            None
       """
    
    insights_list = None

    url = "https://graph.facebook.com/v16.0/act_" +account_id +"/insights?level=ad&time_increment=1&date_preset=yesterday&action_attribution_windows=%5B%221d_view%22%2C%227d_click%22%5D&fields=account_name%2Caccount_id%2Ccampaign_name%2Ccampaign_id%2Cadset_name%2Cadset_id%2Cad_name%2Cad_id%2Creach%2Cimpressions%2Cclicks%2Cctr%2Cspend%2Cconversions%2Ccpc%2Ccpm%2Cvideo_p50_watched_actions%2Cvideo_p95_watched_actions%2Cfrequency%2Cactions&limit=500&access_token="+token
    
    
    while insights_list is None: # deals with API errors and timeouts
        try:
            response = requests.get(url).json()
            
            insights_list = response["data"]
            
        except Exception as e:
            
            print(e)
            
            time.sleep(30)
        
        
    while len(insights_list) == 500: # deals with pagination
    
        new_url = response["paging"]["next"]
        
        response = requests.get(new_url).json()

        while response["data"] is None: # deals with API errors and timeouts
            try:
                response = requests.get(url).json()
                
            except Exception as e:
                
                print(e)
                
                time.sleep(30)
    
        insights_list = insights_list + response["data"]
    
    try: # validates the schema brought by the API
        schema.DataVal(df_dict=insights_list)

    except ValidationError as e:
        print(e)

    for insight in insights_list: # inserts the data into the database, one insight at a time
        
        try:
            upsert_event(schema=schema.Data.parse_obj(insight), db=db)
            
        except Exception as e:
            
            print(e)

    return print('Done')


@app.post('/get_all_insights/', status_code=http.HTTPStatus.ACCEPTED)
def get_all_insights(account_id: str, token: str, start_date: str = "2021-04-25", stop_date: str = datetime.now().strftime("%Y-%m-%d"), db: Session = Depends(get_db)):

    """"Gets all the insights of the previous day from the Facebook API and inserts them into the database.
    
    Parameters
    ----------
        account_id: string
            Facebook account id 
        
        token: string
                Facebook token to validate the access

        start_date: string (format: YYYY-MM-DD)
            Start date of the period to be analyzed
            default: 2021-04-25

        stop_date: string (format: YYYY-MM-DD)
            Stop date of the period to be analyzed
            default: today's date

        db: sqlalchemy.orm.Session
            Database session
                
    Returns
    -------
        None
    """
    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    stop_date = datetime.strptime(stop_date, "%Y-%m-%d")
    
    days = (stop_date - start_date).days
    
    for day in range(days):
        
        date = (stop_date - timedelta(days=day)).strftime("%Y-%m-%d")
        
        print("Fazendo upload dos dados do dia: ", date, "\n")
        
        url = "https://graph.facebook.com/v16.0/act_"+account_id+"/insights?level=ad&time_increment=1&time_range=%7B%22since%22%3A%22"
        start = date
        url2 = "%22%2C%22until%22%3A%22"
        stop = date
        url3 = "%22%7D&action_attribution_windows=%5B%221d_view%22%2C%227d_click%22%5D&fields=account_name%2Caccount_id%2Ccampaign_name%2Ccampaign_id%2Cadset_name%2Cadset_id%2Cad_name%2Cad_id%2Creach%2Cimpressions%2Cclicks%2Cctr%2Cspend%2Cconversions%2Ccpc%2Ccpm%2Cvideo_p50_watched_actions%2Cvideo_p95_watched_actions%2Cobjective%2Cfrequency%2Cactions&limit=500&access_token="+token
        # token expira 03/07

        final_url = url + start + url2 + stop + url3
        
        insights_list = None
        
        while insights_list is None: # deals with API errors and timeouts
            try:
                response = requests.get(final_url).json()
                
                insights_list = response["data"]
                
            except Exception as e:
                
                print(e)
                
                time.sleep(30)
        
        while len(insights_list) == 500: # deals with pagination
        
            new_url = response["paging"]["next"]
            
            response = requests.get(new_url).json()
        
            insights_list = response["data"]
        
        try: # validates the schema brought by the API
            schema.DataVal(df_dict=insights_list)
    
        except ValidationError as e:
            
            print(e)
            
        for insight in insights_list: # inserts the data into the database, one insight at a time
            
            try:
                upsert_event(schema=schema.Data.parse_obj(insight), db=db)
                
            except Exception as e:
                
                print(e)
        

    return print('Done')


if __name__ == '__main__':
    uvicorn.run(app)
    
    
